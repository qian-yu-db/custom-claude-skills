#!/usr/bin/env python3
"""
Bootstrap Project Script
Creates a new project with selected Claude skills from custom-claude-skills repository.

Usage:
    python bootstrap_project.py <project-name> [skill1] [skill2] ...

Example:
    python bootstrap_project.py my-rag-agent \\
        langgraph_skills/langgraph-unstructured-tool-agent \\
        databricks_platform_skills/databricks-agent-deploy2app-skill
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List

# Skills repository
SKILLS_REPO = "https://github.com/qian-yu-db/custom-claude-skills"

# Available skills catalog
AVAILABLE_SKILLS = {
    "databricks_platform_skills/databricks-asset-bundle": "Generate DAB configurations (serverless, modular, Mermaid support)",
    "databricks_platform_skills/databricks-local-notebook": "Local notebook development",
    "databricks_platform_skills/databricks-agent-deploy2app": "Deploy to Databricks Apps",
    "databricks_platform_skills/databricks-agent-deploy-model-serving-dab": "Deploy to Model Serving",
    "langgraph_skills/langgraph-genie-agent": "Databricks Genie integration",
    "langgraph_skills/langgraph-unstructured-tool-agent": "RAG agents (4 patterns)",
    "langgraph_skills/langgraph-multi-agent-supervisor": "Multi-agent orchestration",
    "langgraph_skills/langgraph-mcp-tool-calling-agent": "MCP tool integration",
    "python_sklls/pytest-test-creator": "Auto-generate tests with coverage",
    "python_sklls/python-code-formatter": "Code formatting (blackbricks + black + isort)",
    "develop_planning_skills/mermaid-diagrams-creator": "Create Mermaid diagrams with PNG/SVG/PDF generation",
    "general_skills/jira-epic-creator": "Jira epic generation",
    "general_skills/battle-card-creator": "Competitive analysis",
}


def run_command(cmd: List[str], cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e


def create_directory_structure(project_root: Path):
    """Create the project directory structure."""
    directories = [
        ".claude/skills",
        "docs",
        "src",
        "tests",
        "notebooks",
        "configs",
        "scripts",
    ]
    
    for dir_path in directories:
        (project_root / dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created directory structure")


def initialize_git(project_root: Path):
    """Initialize git repository."""
    run_command(["git", "init"], cwd=project_root)
    print("✅ Initialized git repository")


def add_skills_submodule(project_root: Path):
    """Add custom-claude-skills as a git submodule."""
    run_command(
        ["git", "submodule", "add", SKILLS_REPO, ".claude/skills-repo"],
        cwd=project_root
    )
    run_command(
        ["git", "submodule", "update", "--init", "--recursive"],
        cwd=project_root
    )
    print("✅ Added skills repository as submodule")


def link_skills(project_root: Path, skills: List[str]):
    """Create symlinks to selected skills."""
    skills_dir = project_root / ".claude/skills"
    
    for skill_path in skills:
        skill_name = Path(skill_path).name
        source = project_root / ".claude/skills-repo" / skill_path
        target = skills_dir / skill_name
        
        if not source.exists():
            print(f"⚠️  Warning: Skill not found: {skill_path}")
            continue
        
        # Create symlink
        if not target.exists():
            target.symlink_to(source, target_is_directory=True)
            print(f"✅ Linked skill: {skill_name}")


def generate_project_context(project_root: Path, project_name: str, skills: List[str]):
    """Generate project-context.md file."""
    context_content = f"""# Project Context: {project_name}

**Created**: {datetime.now().strftime("%Y-%m-%d")}

## Project Overview
This project was initialized using the Project Starter skill.

## Selected Skills

"""
    
    for skill_path in skills:
        skill_name = Path(skill_path).name
        skill_desc = AVAILABLE_SKILLS.get(skill_path, "Custom skill")
        context_content += f"### {skill_name}\n"
        context_content += f"- **Path**: `{skill_path}`\n"
        context_content += f"- **Description**: {skill_desc}\n"
        context_content += f"- **Documentation**: `.claude/skills/{skill_name}/SKILL.md`\n\n"
    
    context_content += """## Skill Integration Points
[To be documented as development progresses]

## Development Workflow
1. Review skill documentation in `.claude/skills/*/SKILL.md`
2. Use Claude Code with integrated skills
3. Follow project plan in `docs/PROJECT_PLAN.md`
4. Update documentation as you build

## Next Steps
1. Review `docs/PROJECT_PLAN.md`
2. Review `docs/REQUIREMENTS.md`
3. Setup development environment
4. Begin development with Claude Code
"""
    
    (project_root / ".claude/project-context.md").write_text(context_content)
    print("✅ Generated project-context.md")


def generate_gitignore(project_root: Path):
    """Generate .gitignore file."""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments (uv creates .venv)
.venv/
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Environment
.env
.env.local
*.env

# Databricks
.databricks/

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp
"""

    (project_root / ".gitignore").write_text(gitignore_content)
    print("✅ Generated .gitignore")


def generate_readme(project_root: Path, project_name: str, skills: List[str]):
    """Generate README.md file."""
    readme_content = f"""# {project_name}

**Created**: {datetime.now().strftime("%Y-%m-%d")}

## Overview
[Describe your project here]

## Quick Start

### Prerequisites
- Python 3.11+
- Claude Code
- Git
- uv ([install guide](https://github.com/astral-sh/uv))

### Installation

```bash
# Clone with submodules
git clone --recurse-submodules <repo-url>
cd {project_name}

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates .venv and installs packages)
uv sync
```

### Running Commands

```bash
# Run scripts in project environment
uv run python src/main.py

# Run tests
uv run pytest

# Add new dependencies
uv add package-name
```

### Usage
[Add usage instructions]

## Project Structure

```
{project_name}/
├── .claude/
│   ├── skills-repo/      # Git submodule of custom-claude-skills
│   ├── skills/           # Symlinked skills
│   └── project-context.md
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── REQUIREMENTS.md
│   └── SETUP.md
├── src/                  # Application code
├── tests/                # Test files
├── notebooks/            # Databricks notebooks
├── configs/              # Configuration files
└── README.md
```

## Skills Used

This project integrates the following skills from [custom-claude-skills](https://github.com/qian-yu-db/custom-claude-skills):

"""
    
    for skill_path in skills:
        skill_name = Path(skill_path).name
        skill_desc = AVAILABLE_SKILLS.get(skill_path, "Custom skill")
        readme_content += f"- **{skill_name}**: {skill_desc}\n"
    
    readme_content += """
For detailed skill documentation, see `.claude/skills/*/SKILL.md`

## Documentation

- [PROJECT_PLAN.md](docs/PROJECT_PLAN.md) - Comprehensive project plan
- [REQUIREMENTS.md](docs/REQUIREMENTS.md) - Technical requirements
- [SETUP.md](docs/SETUP.md) - Detailed setup instructions

## Development

Use Claude Code with integrated skills for development tasks:

```bash
claude-code chat
```

Reference skill documentation as needed during development.

## Testing

```bash
# Run tests
uv run pytest

# With coverage
uv run pytest --cov=src tests/
```

## License
[Add license information]

## Contributing
[Add contribution guidelines]
"""
    
    (project_root / "README.md").write_text(readme_content)
    print("✅ Generated README.md")


def init_uv_project(project_root: Path, project_name: str):
    """Initialize uv project with pyproject.toml."""
    # Run uv init in the project directory
    result = run_command(
        ["uv", "init", "--name", project_name, "--python", "3.11"],
        cwd=project_root,
        check=False
    )

    if result.returncode == 0:
        print("✅ Initialized uv project (pyproject.toml, .python-version)")

        # Add common dev dependencies
        run_command(
            ["uv", "add", "--dev", "pytest", "pytest-cov", "ruff"],
            cwd=project_root,
            check=False
        )
        print("✅ Added dev dependencies (pytest, pytest-cov, ruff)")
    else:
        print("⚠️  Warning: uv not found. Creating basic pyproject.toml manually.")
        # Fallback: create basic pyproject.toml manually
        pyproject_content = f"""[project]
name = "{project_name}"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.ruff]
line-length = 100
target-version = "py311"
"""
        (project_root / "pyproject.toml").write_text(pyproject_content)
        (project_root / ".python-version").write_text("3.11\n")
        print("✅ Created pyproject.toml and .python-version")
        print("⚠️  Note: Install uv for better dependency management: https://github.com/astral-sh/uv")


def generate_init_prompt(project_root: Path, project_name: str, skills: List[str]):
    """Generate initialization prompt for Claude Code."""
    prompt_content = f"""# Project Initialization: {project_name}

## Context
This project was initialized using the Project Starter skill.

## Selected Skills
"""
    
    for skill_path in skills:
        skill_name = Path(skill_path).name
        skill_desc = AVAILABLE_SKILLS.get(skill_path, "Custom skill")
        prompt_content += f"- **{skill_name}**: {skill_desc}\n"
    
    prompt_content += """
## Tasks for Claude Code

Please complete the following initialization tasks:

1. **Read Skill Documentation**
   - Review all SKILL.md files from selected skills in `.claude/skills/*/SKILL.md`
   - Understand capabilities and workflows of each skill

2. **Generate PROJECT_PLAN.md**
   - Create comprehensive project plan in `docs/PROJECT_PLAN.md`
   - Include architecture decisions based on available skills
   - Define development phases
   - Identify integration points between skills
   - Set success criteria

3. **Generate REQUIREMENTS.md**
   - Create detailed requirements document in `docs/REQUIREMENTS.md`
   - List functional and technical requirements
   - Aggregate dependencies from all selected skills
   - Include environment setup instructions
   - Define testing strategy

4. **Generate ARCHITECTURE.md** (if applicable)
   - Create architecture documentation in `docs/ARCHITECTURE.md`
   - Include system diagrams
   - Explain component interactions
   - Document data flows

5. **Create Initial Code Scaffolding**
   - Generate appropriate starter files in `src/`
   - Create basic test files in `tests/`
   - Add configuration files in `configs/`
   - Ensure scaffolding aligns with selected skills

6. **Generate SETUP.md**
   - Create detailed setup guide in `docs/SETUP.md`
   - Include step-by-step environment setup
   - Document skill-specific configuration
   - Add troubleshooting tips

## Notes
- Base all documentation on the capabilities of selected skills
- Ensure integration points are clearly documented
- Provide working code examples where appropriate
- Keep documentation clear and actionable
"""
    
    (project_root / ".claude/init-prompt.md").write_text(prompt_content)
    print("✅ Generated initialization prompt")


def print_summary(project_name: str, project_root: Path, skills: List[str]):
    """Print summary and next steps."""
    print("\n" + "="*60)
    print(f"🎉 Project '{project_name}' created successfully!")
    print("="*60)
    print(f"\n📁 Location: {project_root.absolute()}")
    print(f"\n🎯 Selected Skills ({len(skills)}):")
    for skill_path in skills:
        skill_name = Path(skill_path).name
        print(f"   - {skill_name}")
    
    print("\n📋 Next Steps:")
    print(f"   1. cd {project_name}")
    print("   2. uv sync  # Sync dependencies and create .venv")
    print("   3. Review .claude/init-prompt.md")
    print("   4. Run: claude-code chat")
    print("   5. Paste/reference the initialization prompt")
    print("   6. Claude Code will generate documentation and scaffolding")
    print("\n💡 Tips:")
    print("   - Use 'uv run <command>' to run commands in project environment")
    print("   - Use 'uv add <package>' to add dependencies")
    print("   - Use 'claude-code chat' to interact with your project skills")
    print("="*60 + "\n")


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python bootstrap_project.py <project-name> [skill1] [skill2] ...")
        print("\nAvailable skills:")
        for skill_path, desc in AVAILABLE_SKILLS.items():
            print(f"  {skill_path}")
            print(f"    {desc}")
        print("\nExample:")
        print("  python bootstrap_project.py my-agent \\")
        print("    langgraph_skills/langgraph-genie-agent \\")
        print("    databricks_platform_skills/databricks-asset-bundle-skill")
        sys.exit(1)
    
    project_name = sys.argv[1]
    skills = sys.argv[2:] if len(sys.argv) > 2 else []
    
    # Validate project name
    if not project_name.replace("-", "").replace("_", "").isalnum():
        print("Error: Project name should only contain letters, numbers, hyphens, and underscores")
        sys.exit(1)
    
    # Validate skills
    for skill in skills:
        if skill not in AVAILABLE_SKILLS:
            print(f"Warning: Unknown skill: {skill}")
            print("Continuing anyway - skill may be from a newer version of custom-claude-skills")
    
    project_root = Path.cwd() / project_name
    
    # Check if project already exists
    if project_root.exists():
        print(f"Error: Directory '{project_name}' already exists")
        sys.exit(1)
    
    print(f"Creating project: {project_name}")
    print(f"Location: {project_root}")
    if skills:
        print(f"Skills: {len(skills)} selected")
    else:
        print("⚠️  No skills selected - you can add them later")
    print()
    
    try:
        # Create project
        project_root.mkdir(parents=True)
        create_directory_structure(project_root)
        initialize_git(project_root)
        add_skills_submodule(project_root)
        
        if skills:
            link_skills(project_root, skills)
        
        generate_project_context(project_root, project_name, skills)
        generate_gitignore(project_root)
        init_uv_project(project_root, project_name)
        generate_readme(project_root, project_name, skills)
        generate_init_prompt(project_root, project_name, skills)
        
        print_summary(project_name, project_root, skills)
        
    except Exception as e:
        print(f"\n❌ Error during project creation: {e}")
        print(f"You may need to manually clean up: {project_root}")
        sys.exit(1)


if __name__ == "__main__":
    main()
