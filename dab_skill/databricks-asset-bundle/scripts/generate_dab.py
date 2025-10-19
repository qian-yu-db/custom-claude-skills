#!/usr/bin/env python3
"""
Generate Databricks Asset Bundle (DAB) configuration from notebooks or Python files.

This script creates a databricks.yml configuration file for a DAB project,
setting up jobs with tasks based on provided notebooks/Python files and their dependencies.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
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


def generate_dab_config(
    bundle_name: str,
    tasks: List[Dict],
    cluster_config: Optional[Dict] = None,
    notebook_dir: str = "./notebooks",
    output_path: str = "databricks.yml"
) -> None:
    """
    Generate a Databricks Asset Bundle configuration file.
    
    Args:
        bundle_name: Name of the bundle/job
        tasks: List of task dictionaries with name, path, and dependencies
        cluster_config: Optional cluster configuration dictionary
        notebook_dir: Directory where notebooks/files are located
        output_path: Path to write the databricks.yml file
    """
    
    # Default cluster configuration if none provided
    if cluster_config is None:
        cluster_config = {
            "spark_version": "13.3.x-scala2.12",
            "node_type_id": "i3.xlarge",
            "num_workers": 2
        }
    
    # Build job tasks
    job_tasks = []
    for task in tasks:
        file_path = task['path']
        is_notebook = file_path.endswith('.ipynb')
        
        task_config = {
            "task_key": task['name']
        }
        
        # Add dependencies if present
        if task['dependencies']:
            task_config["depends_on"] = [{"task_key": dep} for dep in task['dependencies']]
        
        # Configure task type based on file extension
        if is_notebook:
            task_config["notebook_task"] = {
                "notebook_path": f"{notebook_dir}/{file_path}",
                "source": "WORKSPACE"
            }
        else:
            # Python file
            task_config["python_wheel_task"] = {
                "package_name": bundle_name,
                "entry_point": file_path.replace('.py', '').replace('/', '.')
            }
        
        # Add cluster configuration
        task_config["new_cluster"] = cluster_config
        
        job_tasks.append(task_config)
    
    # Build complete DAB configuration
    config = {
        "bundle": {
            "name": bundle_name
        },
        "resources": {
            "jobs": {
                f"{bundle_name}_job": {
                    "name": f"{bundle_name}_job",
                    "tasks": job_tasks,
                    "max_concurrent_runs": 1
                }
            }
        },
        "targets": {
            "dev": {
                "mode": "development",
                "default": True,
                "workspace": {
                    "host": "${workspace.host}"
                }
            },
            "prod": {
                "mode": "production",
                "workspace": {
                    "host": "${workspace.host}"
                }
            }
        }
    }
    
    # Write to file
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, indent=2)
    
    print(f"✅ Generated Databricks Asset Bundle configuration: {output_path}")
    print(f"   Bundle name: {bundle_name}")
    print(f"   Tasks: {len(tasks)}")
    print(f"\nNext steps:")
    print(f"   1. Review and customize {output_path}")
    print(f"   2. Run: databricks bundle validate")
    print(f"   3. Run: databricks bundle deploy")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Databricks Asset Bundle configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example task description format:
  - extract_data: notebooks/extract.ipynb
  - transform_data: src/transform.py [depends_on: extract_data]
  - load_data: src/load.py [depends_on: transform_data]
        """
    )
    
    parser.add_argument("bundle_name", help="Name of the bundle/job")
    parser.add_argument(
        "-d", "--description",
        help="Task description (format: 'task_name: path [depends_on: dep1, dep2]')",
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        default="databricks.yml",
        help="Output file path (default: databricks.yml)"
    )
    parser.add_argument(
        "--notebook-dir",
        default="./notebooks",
        help="Notebook directory path (default: ./notebooks)"
    )
    parser.add_argument(
        "--spark-version",
        default="13.3.x-scala2.12",
        help="Spark version (default: 13.3.x-scala2.12)"
    )
    parser.add_argument(
        "--node-type",
        default="i3.xlarge",
        help="Node type ID (default: i3.xlarge)"
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=2,
        help="Number of workers (default: 2)"
    )
    
    args = parser.parse_args()
    
    # Parse task information
    tasks = parse_task_info(args.description)
    
    if not tasks:
        print("❌ Error: No valid tasks found in description", file=sys.stderr)
        sys.exit(1)
    
    # Build cluster configuration
    cluster_config = {
        "spark_version": args.spark_version,
        "node_type_id": args.node_type,
        "num_workers": args.num_workers
    }
    
    # Generate configuration
    generate_dab_config(
        bundle_name=args.bundle_name,
        tasks=tasks,
        cluster_config=cluster_config,
        notebook_dir=args.notebook_dir,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
