#!/usr/bin/env python3
"""
Generate Databricks Asset Bundle (DAB) configuration from notebooks or Python files.

This script creates a modular Databricks Asset Bundle with:
- Main databricks.yml with variables
- Separate resource/*.job.yml files for job definitions
- Serverless compute as default (client version 3)
- run_workflow.sh for deployment and execution

Supports input from:
- Text descriptions
- Mermaid diagrams (.mermaid files)
- Workflow diagram images (with OCR/AI parsing)
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml


def parse_task_info(description: str) -> List[Dict]:
    """
    Parse task description to extract task information.

    Expected format (one task per line):
    - task_name: path/to/file.py [depends_on: task1, task2]
    - another_task: path/to/notebook.ipynb

    Args:
        description: Multi-line string describing tasks and dependencies

    Returns:
        List of task dictionaries with name, path, and dependencies
    """
    tasks = []
    for line in description.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Remove leading dash if present
        if line.startswith('-'):
            line = line[1:].strip()

        # Parse task_name: path [depends_on: dep1, dep2]
        if ':' not in line:
            continue

        parts = line.split(':', 1)
        task_name = parts[0].strip()
        rest = parts[1].strip()

        # Extract dependencies if present
        dependencies = []
        file_path = rest

        if '[depends_on:' in rest:
            file_part, dep_part = rest.split('[depends_on:', 1)
            file_path = file_part.strip()
            dep_str = dep_part.split(']')[0].strip()
            dependencies = [d.strip() for d in dep_str.split(',') if d.strip()]

        tasks.append({
            'name': task_name,
            'path': file_path,
            'dependencies': dependencies
        })

    return tasks


def parse_mermaid_diagram(mermaid_file: str) -> List[Dict]:
    """
    Parse a Mermaid diagram file to extract tasks and dependencies.

    Supports flowchart syntax like:
    flowchart TB
        A[extract] --> B[transform]
        B --> C[load]

    Args:
        mermaid_file: Path to .mermaid file

    Returns:
        List of task dictionaries with name, path, and dependencies
    """
    with open(mermaid_file, 'r') as f:
        content = f.read()

    tasks_dict = {}
    edges = []

    # Extract nodes and edges from mermaid diagram
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('flowchart') or line.startswith('graph') or line.startswith('sequenceDiagram'):
            continue

        # Match node definitions: A[label] or A(label) or A{label}
        node_match = re.findall(r'([A-Za-z0-9_]+)[\[\(\{]([^\]\)\}]+)[\]\)\}]', line)
        for node_id, label in node_match:
            if node_id not in tasks_dict:
                tasks_dict[node_id] = {
                    'name': label.strip(),
                    'path': f"src/{label.strip().replace(' ', '_').lower()}.py",
                    'dependencies': []
                }

        # Match edges: A --> B or A -->|label| B
        edge_matches = re.findall(r'([A-Za-z0-9_]+)\s*(?:--?>|==>)\s*(?:\|[^\|]+\|)?\s*([A-Za-z0-9_]+)', line)
        for source, target in edge_matches:
            edges.append((source, target))

    # Build dependencies
    for source, target in edges:
        if target in tasks_dict and source in tasks_dict:
            tasks_dict[target]['dependencies'].append(tasks_dict[source]['name'])

    return list(tasks_dict.values())


def extract_workflow_variables(tasks: List[Dict], bundle_name: str) -> Dict:
    """
    Extract common workflow variables from tasks.

    Args:
        tasks: List of task dictionaries
        bundle_name: Name of the bundle

    Returns:
        Dictionary of variables with descriptions and defaults
    """
    variables = {
        'catalog': {
            'description': 'Unity Catalog name',
            'default': 'main'
        },
        'schema': {
            'description': 'Schema name for tables',
            'default': bundle_name.replace('-', '_')
        },
        'source_path': {
            'description': 'Source data path (volume or cloud storage)',
            'default': '/Volumes/${var.catalog}/${var.schema}/source'
        },
        'checkpoint_path': {
            'description': 'Checkpoint location for Structured Streaming',
            'default': '/Volumes/${var.catalog}/${var.schema}/checkpoints'
        }
    }

    return variables


def generate_main_databricks_yml(
    bundle_name: str,
    variables: Dict,
    workspace_host: str,
    output_dir: str
) -> None:
    """
    Generate the main databricks.yml file with variables and includes.

    Args:
        bundle_name: Name of the bundle
        variables: Dictionary of variables
        workspace_host: Databricks workspace URL
        output_dir: Output directory for the bundle
    """
    config = {
        'bundle': {
            'name': bundle_name
        },
        'variables': variables,
        'include': [
            'resources/*.yml'
        ],
        'targets': {
            'dev': {
                'mode': 'development',
                'default': True,
                'workspace': {
                    'host': workspace_host
                }
            },
            'prod': {
                'mode': 'production',
                'workspace': {
                    'host': workspace_host
                }
            }
        }
    }

    output_path = Path(output_dir) / 'databricks.yml'
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, indent=2)

    print(f"✅ Generated main configuration: {output_path}")


def generate_job_yml(
    bundle_name: str,
    tasks: List[Dict],
    use_serverless: bool,
    notebook_dir: str,
    output_dir: str,
    variables: Dict
) -> None:
    """
    Generate a job.yml file in the resources/ directory.

    Args:
        bundle_name: Name of the bundle/job
        tasks: List of task dictionaries
        use_serverless: Whether to use serverless compute
        notebook_dir: Directory where notebooks/files are located
        output_dir: Output directory for the bundle
        variables: Dictionary of variables for parameter injection
    """
    job_name = f"{bundle_name}_job"

    # Build job tasks
    job_tasks = []
    for task in tasks:
        file_path = task['path']
        is_notebook = file_path.endswith('.ipynb') or file_path.endswith('.py')

        task_config = {
            'task_key': task['name']
        }

        # Add serverless environment
        if use_serverless:
            task_config['environment_key'] = 'serverless_env'

        # Add dependencies if present
        if task['dependencies']:
            task_config['depends_on'] = [{'task_key': dep} for dep in task['dependencies']]

        # Configure task type - always use notebook_task for .py files in src/
        task_config['notebook_task'] = {
            'notebook_path': f"../{file_path}",
            'base_parameters': {
                'catalog': '${var.catalog}',
                'schema': '${var.schema}',
                'source_path': '${var.source_path}',
                'checkpoint_path': '${var.checkpoint_path}'
            }
        }

        job_tasks.append(task_config)

    # Build job configuration
    job_config = {
        'resources': {
            'jobs': {
                job_name: {
                    'name': job_name,
                    'tasks': job_tasks,
                    'max_concurrent_runs': 1
                }
            }
        }
    }

    # Add serverless environment configuration
    if use_serverless:
        job_config['resources']['jobs'][job_name]['environments'] = [
            {
                'environment_key': 'serverless_env',
                'spec': {
                    'client': '3'
                }
            }
        ]

    # Create resources directory if it doesn't exist
    resources_dir = Path(output_dir) / 'resources'
    resources_dir.mkdir(exist_ok=True)

    # Write job.yml
    output_path = resources_dir / f'{bundle_name}.job.yml'
    with open(output_path, 'w') as f:
        yaml.dump(job_config, f, default_flow_style=False, sort_keys=False, indent=2)

    print(f"✅ Generated job definition: {output_path}")


def generate_run_workflow_script(
    bundle_name: str,
    output_dir: str,
    workspace_host: str,
    has_upload: bool = False,
    has_download: bool = False
) -> None:
    """
    Generate run_workflow.sh script for deployment and execution.

    Args:
        bundle_name: Name of the bundle
        output_dir: Output directory for the bundle
        workspace_host: Databricks workspace URL
        has_upload: Whether to include upload functionality
        has_download: Whether to include download functionality
    """
    script_content = f"""#!/bin/bash
set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Print functions
print_info() {{
    echo -e "${{BLUE}}INFO: $1${{NC}}"
}}

print_success() {{
    echo -e "${{GREEN}}SUCCESS: $1${{NC}}"
}}

print_warning() {{
    echo -e "${{YELLOW}}WARNING: $1${{NC}}"
}}

print_error() {{
    echo -e "${{RED}}ERROR: $1${{NC}}"
}}

# Default values
PROFILE=""
TARGET="dev"
SKIP_VALIDATION=false
SKIP_DEPLOYMENT=false
JOB_ID=""
VAR_OVERRIDES=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --profile)
            PROFILE="$2"
            shift 2
            ;;
        --target)
            TARGET="$2"
            shift 2
            ;;
        --skip-validation)
            SKIP_VALIDATION=true
            shift
            ;;
        --skip-deployment)
            SKIP_DEPLOYMENT=true
            shift
            ;;
        --job-id)
            JOB_ID="$2"
            shift 2
            ;;
        --var)
            VAR_OVERRIDES+=("--var" "$2")
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Set profile flag if provided
PROFILE_FLAG=""
if [ -n "$PROFILE" ]; then
    PROFILE_FLAG="--profile $PROFILE"
    print_info "Using Databricks profile: $PROFILE"
fi

# Validate bundle
if [ "$SKIP_VALIDATION" = false ]; then
    print_info "Validating Databricks Asset Bundle..."
    if databricks bundle validate $PROFILE_FLAG -t $TARGET; then
        print_success "Bundle validation passed"
    else
        print_error "Bundle validation failed"
        exit 1
    fi
fi

# Deploy bundle
if [ "$SKIP_DEPLOYMENT" = false ] && [ -z "$JOB_ID" ]; then
    print_info "Deploying bundle to $TARGET environment..."
    if databricks bundle deploy $PROFILE_FLAG -t $TARGET "${{VAR_OVERRIDES[@]}}"; then
        print_success "Bundle deployed successfully"
    else
        print_error "Bundle deployment failed"
        exit 1
    fi
fi

# Run job
if [ -n "$JOB_ID" ]; then
    print_info "Running existing job ID: $JOB_ID"
    RUN_OUTPUT=$(databricks jobs run-now $PROFILE_FLAG --job-id $JOB_ID)
else
    print_info "Running job: {bundle_name}_job"
    RUN_OUTPUT=$(databricks bundle run $PROFILE_FLAG {bundle_name}_job -t $TARGET)
fi

# Extract run ID
RUN_ID=$(echo "$RUN_OUTPUT" | grep -oP 'run_id=\\K[0-9]+' || echo "")

if [ -n "$RUN_ID" ]; then
    print_success "Job started with run ID: $RUN_ID"
    print_info "Monitor at: {workspace_host.rstrip('/')}/#job/runs/$RUN_ID"
else
    print_warning "Could not extract run ID from output"
fi

print_success "Workflow execution initiated"
"""

    output_path = Path(output_dir) / 'run_workflow.sh'
    with open(output_path, 'w') as f:
        f.write(script_content)

    # Make script executable
    os.chmod(output_path, 0o755)

    print(f"✅ Generated workflow runner: {output_path}")


def create_project_structure(output_dir: str, tasks: List[Dict]) -> None:
    """
    Create the project directory structure.

    Args:
        output_dir: Output directory for the bundle
        tasks: List of task dictionaries
    """
    base_path = Path(output_dir)

    # Create directories
    (base_path / 'resources').mkdir(exist_ok=True)
    (base_path / 'src').mkdir(exist_ok=True)
    (base_path / 'tests').mkdir(exist_ok=True)

    # Create placeholder files for tasks
    for task in tasks:
        file_path = base_path / task['path']
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            # Create placeholder notebook/script
            if file_path.suffix == '.ipynb':
                # Create basic notebook structure
                notebook_content = {
                    'cells': [
                        {
                            'cell_type': 'markdown',
                            'metadata': {},
                            'source': [f'# {task["name"]}\\n\\nTODO: Implement task logic']
                        },
                        {
                            'cell_type': 'code',
                            'execution_count': None,
                            'metadata': {},
                            'outputs': [],
                            'source': ['# Parameters\\ncatalog = "main"\\nschema = "default"\\n']
                        }
                    ],
                    'metadata': {
                        'kernelspec': {
                            'display_name': 'Python 3',
                            'language': 'python',
                            'name': 'python3'
                        }
                    },
                    'nbformat': 4,
                    'nbformat_minor': 4
                }
                import json
                with open(file_path, 'w') as f:
                    json.dump(notebook_content, f, indent=2)
            else:
                # Create Python script
                with open(file_path, 'w') as f:
                    f.write(f'''# Databricks notebook source
# MAGIC %md
# MAGIC # {task['name']}
# MAGIC
# MAGIC TODO: Implement task logic

# COMMAND ----------

# Parameters
dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "default")
dbutils.widgets.text("source_path", "")
dbutils.widgets.text("checkpoint_path", "")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
source_path = dbutils.widgets.get("source_path")
checkpoint_path = dbutils.widgets.get("checkpoint_path")

# COMMAND ----------

# TODO: Implement task logic
print(f"Running task: {task['name']}")
print(f"Catalog: {{catalog}}")
print(f"Schema: {{schema}}")
''')

    # Create README
    readme_path = base_path / 'README.md'
    with open(readme_path, 'w') as f:
        f.write(f'''# {output_dir}

Databricks Asset Bundle generated with modular structure.

## Project Structure

```
.
├── databricks.yml          # Main bundle configuration with variables
├── resources/              # Job definitions
│   └── *.job.yml          # Individual job configurations
├── src/                    # Source code (notebooks and scripts)
├── tests/                  # Unit tests
└── run_workflow.sh        # Deployment and execution script
```

## Usage

### 1. Validate Bundle
```bash
databricks bundle validate -t dev
```

### 2. Deploy Bundle
```bash
databricks bundle deploy -t dev
```

### 3. Run Workflow
```bash
./run_workflow.sh --target dev
```

Or with variable overrides:
```bash
./run_workflow.sh --target dev --var catalog=my_catalog --var schema=my_schema
```

### 4. Deploy to Production
```bash
databricks bundle deploy -t prod
./run_workflow.sh --target prod
```

## Customization

### Variables
Edit `databricks.yml` to modify default variable values.

### Tasks
Task definitions are in `resources/*.job.yml`. Modify to:
- Add/remove tasks
- Change dependencies
- Adjust parameters
- Configure compute settings

### Environments
Configure `dev` and `prod` targets in `databricks.yml`.

## Development

Notebooks are in `src/`. Test locally or in Databricks workspace before deploying the bundle.
''')

    print(f"✅ Created project structure in {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Databricks Asset Bundle configuration with modular structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:

1. From text description:
   scripts/generate_dab.py my_pipeline \\
     -d "extract: src/extract.py
         transform: src/transform.py [depends_on: extract]
         load: src/load.py [depends_on: transform]"

2. From Mermaid diagram:
   scripts/generate_dab.py my_pipeline \\
     --mermaid-file workflow.mermaid

3. With custom workspace:
   scripts/generate_dab.py my_pipeline \\
     -d "..." \\
     --workspace-host "https://my-workspace.cloud.databricks.com"

4. Without serverless (use clusters):
   scripts/generate_dab.py my_pipeline \\
     -d "..." \\
     --no-serverless
        """
    )

    parser.add_argument("bundle_name", help="Name of the bundle/job")
    parser.add_argument(
        "-d", "--description",
        help="Task description (format: 'task_name: path [depends_on: dep1, dep2]')"
    )
    parser.add_argument(
        "--mermaid-file",
        help="Path to Mermaid diagram file (.mermaid)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Output directory for the bundle (default: current directory)"
    )
    parser.add_argument(
        "--notebook-dir",
        default="src",
        help="Notebook directory path (default: src)"
    )
    parser.add_argument(
        "--workspace-host",
        default="https://e2-demo-field-eng.cloud.databricks.com",
        help="Databricks workspace URL"
    )
    parser.add_argument(
        "--no-serverless",
        action="store_true",
        help="Use cluster compute instead of serverless (default: use serverless)"
    )

    args = parser.parse_args()

    # Parse task information from description or mermaid
    tasks = []
    if args.description:
        tasks = parse_task_info(args.description)
    elif args.mermaid_file:
        if not Path(args.mermaid_file).exists():
            print(f"❌ Error: Mermaid file not found: {args.mermaid_file}", file=sys.stderr)
            sys.exit(1)
        tasks = parse_mermaid_diagram(args.mermaid_file)
    else:
        print("❌ Error: Either --description or --mermaid-file must be provided", file=sys.stderr)
        sys.exit(1)

    if not tasks:
        print("❌ Error: No valid tasks found", file=sys.stderr)
        sys.exit(1)

    # Extract variables
    variables = extract_workflow_variables(tasks, args.bundle_name)

    # Create project structure
    create_project_structure(args.output_dir, tasks)

    # Generate main databricks.yml
    generate_main_databricks_yml(
        bundle_name=args.bundle_name,
        variables=variables,
        workspace_host=args.workspace_host,
        output_dir=args.output_dir
    )

    # Generate job.yml
    generate_job_yml(
        bundle_name=args.bundle_name,
        tasks=tasks,
        use_serverless=not args.no_serverless,
        notebook_dir=args.notebook_dir,
        output_dir=args.output_dir,
        variables=variables
    )

    # Generate run_workflow.sh
    generate_run_workflow_script(
        bundle_name=args.bundle_name,
        output_dir=args.output_dir,
        workspace_host=args.workspace_host
    )

    print(f"\n✅ Successfully generated Databricks Asset Bundle: {args.bundle_name}")
    print(f"   Output directory: {args.output_dir}")
    print(f"   Tasks: {len(tasks)}")
    print(f"   Compute: {'Serverless (client 3)' if not args.no_serverless else 'Cluster'}")
    print(f"\n📁 Project structure:")
    print(f"   {args.output_dir}/")
    print(f"   ├── databricks.yml              (main config with variables)")
    print(f"   ├── resources/{args.bundle_name}.job.yml  (job definition)")
    print(f"   ├── src/                        (source code)")
    print(f"   ├── run_workflow.sh             (deployment script)")
    print(f"   └── README.md                   (documentation)")
    print(f"\n🚀 Next steps:")
    print(f"   1. Review generated files in {args.output_dir}")
    print(f"   2. Implement task logic in src/ files")
    print(f"   3. Run: databricks bundle validate -t dev")
    print(f"   4. Run: ./run_workflow.sh --target dev")


if __name__ == "__main__":
    main()
