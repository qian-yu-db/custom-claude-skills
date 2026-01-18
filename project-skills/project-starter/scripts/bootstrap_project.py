#!/usr/bin/env python3
"""
Bootstrap Project Script
Creates a new project with selected Claude skills from custom-claude-skills repository.

Usage:
    python bootstrap_project.py <project-name> [skill1] [skill2] ... [--cross-platform]

Example:
    python bootstrap_project.py my-rag-agent \\
        langgraph_skills/langgraph-unstructured-tool-agent \\
        databricks_platform_skills/databricks-agent-deploy2app \\
        --cross-platform

Cross-Platform Support:
    Use --cross-platform flag to generate CLAUDE.md, AGENTS.md (Codex), and GEMINI.md
    from selected skills. This makes your project work with Claude Code, Codex CLI, and Gemini CLI.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict

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
    "develop_planning_skills/cross-platform-skill": "Convert skills for Codex CLI and Gemini CLI",
    "general_skills/jira-epic-creator": "Jira epic generation",
    "general_skills/battle-card-creator": "Competitive analysis",
}

# Cross-platform conversion mappings
CLAUDE_TO_CODEX = {
    r'/project:(\w+)': r'/prompts:\1',
    r'\.claude/commands/': '.codex/prompts/',
    r'\.mcp\.json': '~/.codex/config.toml (mcp_servers section)',
    r'Claude Code': 'Codex CLI',
    r'claude code': 'Codex CLI',
}

CLAUDE_TO_GEMINI = {
    r'/project:(\w+)': r'/\1',
    r'\.claude/commands/': '.gemini/commands/',
    r'\.mcp\.json': '.gemini/settings.json (mcpServers section)',
    r'Claude Code': 'Gemini CLI',
    r'claude code': 'Gemini CLI',
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
    print("Adding custom-claude-skills repository as git submodule...")

    # Add submodule
    run_command(
        ["git", "submodule", "add", SKILLS_REPO, ".claude/skills-repo"],
        cwd=project_root
    )

    # Initialize and update submodules
    run_command(
        ["git", "submodule", "update", "--init", "--recursive"],
        cwd=project_root
    )

    # Commit the .gitmodules file and submodule reference
    run_command(
        ["git", "add", ".gitmodules", ".claude/skills-repo"],
        cwd=project_root
    )

    print("✅ Added skills repository as submodule (.gitmodules created)")
    print("   When you push this project to GitHub, others can clone with:")
    print("   git clone --recurse-submodules <your-repo-url>")


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
# Clone with submodules (IMPORTANT: includes skill repository)
git clone --recurse-submodules <repo-url>
cd {project_name}

# If you already cloned without --recurse-submodules, initialize submodules:
# git submodule update --init --recursive

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates .venv and installs packages)
uv sync
```

**Note**: This project uses git submodules to include the custom-claude-skills repository in `.claude/skills-repo/`. The skills directory contains symlinks to the selected skills from this submodule. Always clone with `--recurse-submodules` or run `git submodule update --init --recursive` after cloning.

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


def extract_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Extract YAML frontmatter from markdown content."""
    frontmatter = {}
    body = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            body = parts[2].strip()

    return frontmatter, body


def apply_replacements(content: str, replacements: Dict[str, str]) -> str:
    """Apply regex replacements to content."""
    result = content
    for pattern, replacement in replacements.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def merge_skill_files(project_root: Path, skills: List[str], project_name: str) -> str:
    """Merge selected skills' SKILL.md files into a unified instruction document."""
    merged_content = f"""# {project_name} - Project Instructions

This document combines instructions from all selected skills for this project.
Use this as your guide when working with Claude Code, Codex CLI, or Gemini CLI.

---

"""

    for skill_path in skills:
        skill_name = Path(skill_path).name
        skill_md_path = project_root / ".claude/skills-repo" / skill_path / "SKILL.md"

        if skill_md_path.exists():
            content = skill_md_path.read_text()
            _, body = extract_frontmatter(content)

            merged_content += f"\n## Skill: {skill_name}\n\n"
            merged_content += f"*Source: `{skill_path}/SKILL.md`*\n\n"
            merged_content += body
            merged_content += "\n\n---\n"
        else:
            merged_content += f"\n## Skill: {skill_name}\n\n"
            merged_content += f"*Note: SKILL.md not found at {skill_path}*\n\n---\n"

    return merged_content


def convert_to_codex(content: str, source_name: str) -> str:
    """Convert Claude instructions to Codex CLI format."""
    _, body = extract_frontmatter(content)
    converted = apply_replacements(body, CLAUDE_TO_CODEX)

    # Add MCP configuration note if MCP is mentioned
    if 'mcp' in content.lower():
        mcp_note = """> **Codex CLI MCP Configuration**: Configure MCP servers in `~/.codex/config.toml`:
> ```toml
> [mcp_servers.my-server]
> command = "npx"
> args = ["-y", "@my/mcp-server"]
> ```

"""
        converted = mcp_note + converted

    header = f"<!-- Generated from {source_name} for Codex CLI -->\n"
    header += "<!-- Keep in sync with instructions.md -->\n\n"
    return header + converted


def convert_to_gemini(content: str, source_name: str) -> str:
    """Convert Claude instructions to Gemini CLI format."""
    _, body = extract_frontmatter(content)
    converted = apply_replacements(body, CLAUDE_TO_GEMINI)

    # Add MCP configuration note if MCP is mentioned
    if 'mcp' in content.lower():
        mcp_note = """> **Gemini CLI MCP Configuration**: Configure MCP servers in `.gemini/settings.json`:
> ```json
> {
>   "mcpServers": {
>     "my-server": {
>       "command": "npx",
>       "args": ["-y", "@my/mcp-server"]
>     }
>   }
> }
> ```

"""
        converted = mcp_note + converted

    # Add Gemini-specific tip
    memory_tip = "> **Tip**: Use `/memory add <instruction>` to add rules to your global GEMINI.md on the fly.\n\n"
    converted = memory_tip + converted

    header = f"<!-- Generated from {source_name} for Gemini CLI -->\n"
    header += "<!-- Keep in sync with instructions.md -->\n\n"
    return header + converted


def generate_cross_platform_files(project_root: Path, project_name: str, skills: List[str]):
    """Generate cross-platform instruction files (CLAUDE.md, AGENTS.md, GEMINI.md)."""
    if not skills:
        print("⚠️  No skills selected - skipping cross-platform generation")
        return

    print("\n📦 Generating cross-platform instruction files...")

    # Step 1: Merge all skill files into unified instructions
    merged_content = merge_skill_files(project_root, skills, project_name)
    instructions_path = project_root / "instructions.md"
    instructions_path.write_text(merged_content)
    print("  ✅ Created instructions.md (canonical source)")

    # Step 2: Generate CLAUDE.md (for Claude Code)
    _, body = extract_frontmatter(merged_content)
    claude_content = f"<!-- Generated from instructions.md for Claude Code -->\n"
    claude_content += f"<!-- This is the canonical instruction file for this project -->\n\n"
    claude_content += body
    (project_root / "CLAUDE.md").write_text(claude_content)
    print("  ✅ Created CLAUDE.md (Claude Code)")

    # Step 3: Generate AGENTS.md (for Codex CLI)
    codex_content = convert_to_codex(merged_content, "instructions.md")
    (project_root / "AGENTS.md").write_text(codex_content)
    print("  ✅ Created AGENTS.md (Codex CLI)")

    # Step 4: Generate GEMINI.md (for Gemini CLI)
    gemini_content = convert_to_gemini(merged_content, "instructions.md")
    (project_root / "GEMINI.md").write_text(gemini_content)
    print("  ✅ Created GEMINI.md (Gemini CLI)")

    # Step 5: Create sync script for future updates
    sync_script = """#!/bin/bash
# Sync cross-platform instruction files from instructions.md
# Run this after updating instructions.md

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Syncing cross-platform instruction files..."

# Check if instructions.md exists
if [ ! -f "$PROJECT_ROOT/instructions.md" ]; then
    echo "Error: instructions.md not found"
    exit 1
fi

# Use the convert_skill.py from skills-repo if available
CONVERTER="$PROJECT_ROOT/.claude/skills-repo/develop_planning_skills/cross-platform-skill/scripts/convert_skill.py"

if [ -f "$CONVERTER" ]; then
    python "$CONVERTER" "$PROJECT_ROOT/instructions.md" --output-dir "$PROJECT_ROOT"
    echo "✅ Sync complete using cross-platform-skill converter"
else
    echo "⚠️  Converter not found. Manual sync required."
    echo "   Run: python .claude/skills-repo/develop_planning_skills/cross-platform-skill/scripts/convert_skill.py instructions.md"
fi
"""
    sync_path = project_root / "scripts/sync_instructions.sh"
    sync_path.write_text(sync_script)
    sync_path.chmod(0o755)
    print("  ✅ Created scripts/sync_instructions.sh")

    print("\n✅ Cross-platform files generated!")
    print("   Your project now works with Claude Code, Codex CLI, and Gemini CLI")


def print_summary(project_name: str, project_root: Path, skills: List[str], cross_platform: bool = False):
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

    print("\n🔧 Git & Submodules:")
    print("   - Skills repo added as git submodule in .claude/skills-repo/")
    print("   - Commit your initial setup: git commit -m 'Initial project setup'")
    print("   - Push to remote: git push -u origin main")
    print("   - Others can clone with: git clone --recurse-submodules <repo-url>")
    print("   - If they forgot: git submodule update --init --recursive")

    if cross_platform:
        print("\n🌐 Cross-Platform Support:")
        print("   - CLAUDE.md    → Claude Code")
        print("   - AGENTS.md    → Codex CLI (OpenAI)")
        print("   - GEMINI.md    → Gemini CLI (Google)")
        print("   - instructions.md → Canonical source (edit this, then sync)")
        print("   - scripts/sync_instructions.sh → Re-generate platform files")

    print("\n💡 Tips:")
    print("   - Use 'uv run <command>' to run commands in project environment")
    print("   - Use 'uv add <package>' to add dependencies")
    print("   - Use 'claude-code chat' to interact with your project skills")
    print("   - The .gitmodules file tracks the skills repo - don't delete it!")
    if cross_platform:
        print("   - After editing instructions.md, run: ./scripts/sync_instructions.sh")
    print("="*60 + "\n")


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python bootstrap_project.py <project-name> [skill1] [skill2] ... [--cross-platform]")
        print("\nOptions:")
        print("  --cross-platform    Generate CLAUDE.md, AGENTS.md, GEMINI.md from selected skills")
        print("\nAvailable skills:")
        for skill_path, desc in AVAILABLE_SKILLS.items():
            print(f"  {skill_path}")
            print(f"    {desc}")
        print("\nExamples:")
        print("  # Basic project:")
        print("  python bootstrap_project.py my-agent \\")
        print("    langgraph_skills/langgraph-genie-agent \\")
        print("    databricks_platform_skills/databricks-asset-bundle")
        print()
        print("  # With cross-platform support:")
        print("  python bootstrap_project.py my-agent \\")
        print("    langgraph_skills/langgraph-genie-agent \\")
        print("    --cross-platform")
        sys.exit(1)

    # Parse arguments
    args = sys.argv[1:]
    cross_platform = "--cross-platform" in args
    if cross_platform:
        args.remove("--cross-platform")

    project_name = args[0]
    skills = args[1:] if len(args) > 1 else []
    
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
    if cross_platform:
        print("Cross-platform: ✅ Enabled (will generate CLAUDE.md, AGENTS.md, GEMINI.md)")
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

        # Generate cross-platform files if requested
        if cross_platform:
            generate_cross_platform_files(project_root, project_name, skills)

        print_summary(project_name, project_root, skills, cross_platform)

    except Exception as e:
        print(f"\n❌ Error during project creation: {e}")
        print(f"You may need to manually clean up: {project_root}")
        sys.exit(1)


if __name__ == "__main__":
    main()
