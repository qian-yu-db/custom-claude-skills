# Project Starter Skill

## Purpose
This skill enables Claude Code to bootstrap new projects by selecting and integrating skills from the custom-claude-skills repository, setting up proper project structure, and generating comprehensive documentation.

## Repository Reference
- **Skills Repository**: https://github.com/qian-yu-db/custom-claude-skills
- **Available Skills**: 12 specialized skills across Databricks, LangGraph, Python, and general domains

## Skill Catalog

### Databricks Platform Skills (4)
1. **databricks-asset-bundle-skill** - Generate DAB configurations from notebooks/Python files
2. **databricks-local-notebook-skill** - Create notebooks with local IDE development via Databricks Connect
3. **databricks-agent-deploy2app-skill** - Deploy AI agents to Databricks Apps
4. **databricks-agent-deploy-model-serving-dab** - Deploy agents to Model Serving using DABs

### LangGraph Skills (4)
1. **langgraph-genie-agent** - Build agents with Databricks Genie API for natural language queries
2. **langgraph-unstructured-tool-agent** - Build RAG agents with Vector Search (4 patterns)
3. **langgraph-multi-agent-supervisor** - Build multi-agent systems with supervisor orchestration
4. **langgraph-mcp-tool-calling-agent** - Build agents with Model Context Protocol (MCP) tools

### Python Skills (2)
1. **pytest-test-creator** - Auto-generate comprehensive unit tests
2. **python-code-formatter** - Format code (blackbricks for Databricks, black+isort for regular Python)

### General Skills (2)
1. **jira-epic-creator-skill** - Transform documents into structured Jira epics
2. **battle-card-creator-skill** - Automate competitive battle card creation

## Project Structure
When initializing a project, create this structure:

```
project-name/
├── .claude/
│   ├── skills-repo/          # Git submodule of custom-claude-skills
│   ├── skills/                # Symlinks to selected skills
│   │   ├── skill-1/
│   │   └── skill-2/
│   └── project-context.md     # Generated context for this project
├── docs/
│   ├── PROJECT_PLAN.md        # Generated comprehensive plan
│   ├── REQUIREMENTS.md        # Generated requirements
│   ├── ARCHITECTURE.md        # Generated architecture (if applicable)
│   └── SETUP.md              # Setup instructions
├── src/                       # Source code
├── tests/                     # Test files
├── notebooks/                 # Databricks notebooks (if using Databricks skills)
├── configs/                   # Configuration files
├── .gitignore
├── README.md
└── requirements.txt
```

## Initialization Workflow

### Step 1: Understand User Requirements
When user requests a new project, gather:
- **Project name** and description
- **Primary goal** (e.g., build RAG agent, create Databricks app, generate documentation)
- **Skills needed** (based on project type, suggest relevant skills)
- **Tech stack** preferences

### Step 2: Skill Selection Logic
Based on project type, recommend skill combinations:

**For RAG/Agent Projects:**
- langgraph-unstructured-tool-agent (RAG)
- databricks-agent-deploy2app-skill (deployment)
- pytest-test-creator (testing)

**For Multi-Agent Systems:**
- langgraph-genie-agent + langgraph-unstructured-tool-agent
- langgraph-multi-agent-supervisor
- databricks-agent-deploy-model-serving-dab

**For Databricks Development:**
- databricks-local-notebook-skill
- databricks-asset-bundle-skill
- python-code-formatter

**For Documentation/Analysis:**
- battle-card-creator-skill
- jira-epic-creator-skill

### Step 3: Create Project Structure
Execute these actions:

1. **Create directories** according to project structure above
2. **Initialize git repository**
3. **Add skills repository as submodule**:
   ```bash
   git submodule add https://github.com/qian-yu-db/custom-claude-skills .claude/skills-repo
   git submodule update --init --recursive
   ```
4. **Create symlinks** for selected skills:
   ```bash
   ln -s ../.claude/skills-repo/[skill-path] .claude/skills/[skill-name]
   ```

### Step 4: Generate Project Context
Create `.claude/project-context.md`:

```markdown
# Project Context: [Project Name]

## Project Overview
[Description of what this project does]

## Selected Skills
[List each skill with brief description of why it's included]

## Skill Integration Points
[How skills work together in this project]

## Development Workflow
[Step-by-step workflow leveraging the skills]
```

### Step 5: Generate Documentation

#### PROJECT_PLAN.md Template
```markdown
# Project Plan: [Project Name]

## 1. Project Overview
- **Goal**: [Primary objective]
- **Deliverables**: [What will be built]
- **Timeline**: [Estimated phases]

## 2. Architecture
[Based on selected skills, describe architecture]
- Components
- Data flow
- Integration points

## 3. Development Phases
### Phase 1: Setup & Foundation
- Environment setup
- Skill integration verification
- Basic scaffolding

### Phase 2: Core Implementation
[Based on skills - e.g., agent development, notebook creation, etc.]

### Phase 3: Testing & Validation
[Using pytest-test-creator if selected]

### Phase 4: Deployment
[Using deployment skills if selected]

## 4. Skills Utilized
[For each selected skill, explain how it's used in the project]

### [Skill Name]
- **Purpose**: [Why this skill is needed]
- **Usage**: [How it will be applied]
- **Deliverables**: [What this skill helps create]

## 5. Dependencies
[Aggregated from selected skills' requirements]

## 6. Success Criteria
[Measurable outcomes]
```

#### REQUIREMENTS.md Template
```markdown
# Requirements: [Project Name]

## Functional Requirements
[Based on project goals]

## Technical Requirements
### Environment
[From selected skills]

### Dependencies
[Aggregate from all selected skills]

### Tools Required
[Claude Code, Git, skill-specific tools]

## Skill-Specific Requirements
[For each skill, list its requirements]

### [Skill Name]
- Python packages
- Environment variables
- External services

## Setup Instructions
1. Clone repository with submodules
2. Install dependencies
3. Configure environment
4. Verify skill integration

## Testing Requirements
[If pytest-test-creator is selected]
```

### Step 6: Create Initial Scaffolding

Based on selected skills, create appropriate starter files:

**For LangGraph projects:**
- `src/agent.py` - Main agent implementation
- `src/tools.py` - Custom tools
- `src/config.py` - Configuration
- `tests/test_agent.py` - Basic tests

**For Databricks projects:**
- `notebooks/01_setup.py` - Setup notebook
- `configs/databricks.yml` - DAB configuration
- `src/utils.py` - Shared utilities

**For general projects:**
- `src/main.py` - Entry point
- `tests/test_main.py` - Basic tests
- `configs/config.yaml` - Configuration

### Step 7: Generate README.md
```markdown
# [Project Name]

[Project description]

## Quick Start

### Prerequisites
- Python 3.x
- Claude Code
- [Other requirements based on skills]

### Installation
\`\`\`bash
# Clone with submodules
git clone --recurse-submodules [repo-url]
cd [project-name]

# Install dependencies
pip install -r requirements.txt
\`\`\`

### Usage
[Based on project type and skills]

## Project Structure
[Explain directory layout]

## Skills Used
[Link to each skill's documentation]

## Documentation
- [PROJECT_PLAN.md](docs/PROJECT_PLAN.md) - Detailed project plan
- [REQUIREMENTS.md](docs/REQUIREMENTS.md) - Requirements and setup
- [SETUP.md](docs/SETUP.md) - Detailed setup instructions

## Development
[Workflow for using Claude Code with this project]

## License
[License information]
```

## Claude Code Commands

### Initialize New Project
**User says**: "Create a new project called [name] for [purpose]"

**Claude Code should**:
1. Ask clarifying questions about requirements
2. Suggest relevant skills based on purpose
3. Confirm skill selection with user
4. Execute initialization workflow (Steps 1-7 above)
5. Provide summary of created structure

### Add Skills to Existing Project
**User says**: "Add [skill-name] to this project"

**Claude Code should**:
1. Verify .claude/skills-repo exists (if not, add submodule)
2. Create symlink to requested skill
3. Update project-context.md
4. Update REQUIREMENTS.md with new dependencies
5. Suggest integration points in existing code

### Generate Project Documentation
**User says**: "Generate/update project documentation"

**Claude Code should**:
1. Read all SKILL.md files from .claude/skills/
2. Analyze existing code structure
3. Generate/update PROJECT_PLAN.md
4. Generate/update REQUIREMENTS.md
5. Update README.md if needed

### Validate Project Setup
**User says**: "Validate project setup" or "Check if project is configured correctly"

**Claude Code should**:
1. Verify directory structure
2. Check submodule status
3. Verify skill symlinks
4. Check for required files (README, requirements.txt, etc.)
5. Validate dependencies from skills are in requirements.txt
6. Report any issues found

## Best Practices

### Skill Selection
- Start minimal - add skills as needed
- Consider skill dependencies (e.g., deployment skills need corresponding development skills)
- Review each skill's QUICK_REFERENCE.md for capabilities

### Documentation
- Keep PROJECT_PLAN.md updated as project evolves
- Reference skill documentation for detailed usage
- Document integration points between skills

### Project Organization
- Keep skill-specific code in appropriate directories
- Use clear naming conventions
- Maintain separation between generated and custom code

### Version Control
- Commit .claude/project-context.md with project
- Document skill versions used (via submodule commit)
- Include .gitignore appropriate for tech stack

## Troubleshooting

### Submodule Issues
If skills-repo submodule is not properly initialized:
```bash
git submodule update --init --recursive
```

### Symlink Issues
On Windows, ensure Developer Mode is enabled or use directory junctions:
```bash
mklink /D .claude\skills\skill-name .claude\skills-repo\path\to\skill
```

### Skill Conflicts
If skills have conflicting requirements:
1. Review each skill's SKILL.md for dependencies
2. Create virtual environment with compatible versions
3. Document resolution in REQUIREMENTS.md

## Examples

### Example 1: RAG Agent with Databricks Deployment
```
User: "Create a new RAG agent project that queries our product documentation"

Claude Code creates:
- Project structure with src/agent.py
- Skills: langgraph-unstructured-tool-agent, databricks-agent-deploy2app-skill
- Documentation explaining RAG setup and Databricks deployment
- Sample code for vector search integration
```

### Example 2: Multi-Agent System
```
User: "Create a multi-agent system with Genie integration"

Claude Code creates:
- Project with multi-agent architecture
- Skills: langgraph-genie-agent, langgraph-multi-agent-supervisor
- Documentation for supervisor pattern
- Configuration for agent orchestration
```

### Example 3: Databricks Notebook Development
```
User: "Create a Databricks project with local development"

Claude Code creates:
- Notebooks directory with starter notebooks
- Skills: databricks-local-notebook-skill, databricks-asset-bundle-skill
- DAB configuration files
- Local development setup with Databricks Connect
```

## Integration with Claude Code

When user provides a project request, Claude Code should:

1. **Activate this skill** by reading this SKILL.md
2. **Parse user intent** to determine project type
3. **Consult skill catalog** to recommend appropriate skills
4. **Execute initialization workflow** systematically
5. **Read selected skills' SKILL.md files** for detailed instructions
6. **Generate all documentation** based on combined skill knowledge
7. **Create working code scaffolding** that demonstrates skill usage
8. **Provide clear next steps** for development

## Skill Maintenance

This skill assumes the custom-claude-skills repository structure:
```
custom-claude-skills/
├── databricks_platform_skills/
├── langgraph_skills/
├── python_sklls/  # Note: typo in original repo
└── general_skills/
```

If repository structure changes, update the Skill Catalog section accordingly.

## Version
- **Version**: 1.0.0
- **Last Updated**: November 2025
- **Compatible with**: Claude Code, custom-claude-skills v1.x

## Support
For issues or questions about specific skills, refer to individual skill documentation in the custom-claude-skills repository.
