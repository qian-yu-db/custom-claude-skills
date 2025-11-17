# Project Starter - Usage Examples

This document provides real-world examples of using the Project Starter skill with Claude Code.

## Example 1: RAG Agent for Document Search

### User Input
```
Create a new RAG agent project called "doc-search-agent" that will search through our company documentation
```

### Claude Code Response
Claude Code will:
1. Create project structure
2. Recommend and add these skills:
   - `langgraph-unstructured-tool-agent` (for RAG implementation)
   - `databricks-agent-deploy2app-skill` (for deployment)
   - `pytest-test-creator` (for testing)
3. Generate documentation explaining:
   - How to setup vector search
   - RAG architecture with 4 patterns (simple, tool-calling, multi-hop, self-query)
   - Databricks Apps deployment process
4. Create initial files:
   - `src/agent.py` - RAG agent implementation
   - `src/tools.py` - Custom search tools
   - `src/config.py` - Configuration
   - `tests/test_agent.py` - Unit tests

### Generated PROJECT_PLAN.md Excerpt
```markdown
## Phase 2: Core Implementation

### RAG Agent Development
Using langgraph-unstructured-tool-agent skill:

1. **Vector Store Setup**
   - Configure Databricks Vector Search
   - Ingest company documentation
   - Create embeddings

2. **Agent Implementation** 
   - Implement agent with tool-calling pattern
   - Add document retrieval tools
   - Configure response generation

3. **Testing**
   - Unit tests with pytest-test-creator
   - Integration tests with sample queries
```

---

## Example 2: Multi-Agent System with Genie

### User Input
```
Create a multi-agent system called "data-analyst-agents" that uses Genie for SQL queries and also searches documentation
```

### Claude Code Response
Claude Code will:
1. Create project structure
2. Add these skills:
   - `langgraph-genie-agent` (SQL queries via Genie)
   - `langgraph-unstructured-tool-agent` (document search)
   - `langgraph-multi-agent-supervisor` (orchestration)
   - `databricks-agent-deploy-model-serving-dab` (deployment)
3. Generate architecture showing:
   - Supervisor agent pattern
   - Two specialized agents (SQL + search)
   - Communication flow between agents
4. Create files for multi-agent system

### Project Structure Created
```
data-analyst-agents/
├── src/
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── genie_agent.py
│   │   └── search_agent.py
│   ├── tools/
│   │   ├── genie_tools.py
│   │   └── search_tools.py
│   └── config.py
├── tests/
│   ├── test_supervisor.py
│   ├── test_genie_agent.py
│   └── test_search_agent.py
└── configs/
    └── agents_config.yaml
```

---

## Example 3: Databricks Notebook Development

### User Input
```
Create a Databricks project called "data-pipeline" for local notebook development with DAB deployment
```

### Claude Code Response
Claude Code will:
1. Create project structure with notebooks/ directory
2. Add these skills:
   - `databricks-local-notebook-skill`
   - `databricks-asset-bundle-skill`
   - `python-code-formatter`
3. Generate:
   - Sample notebooks in `notebooks/`
   - DAB configuration in `configs/databricks.yml`
   - Setup instructions for Databricks Connect
4. Create initial notebooks:
   - `01_setup.py` - Environment setup
   - `02_data_ingestion.py` - Data loading
   - `03_transformation.py` - Data transformation
   - `04_validation.py` - Quality checks

---

## Example 4: Adding Skills to Existing Project

### User Input (in existing project)
```
Add the battle-card-creator-skill to this project
```

### Claude Code Response
Claude Code will:
1. Verify `.claude/skills-repo` exists
2. Create symlink: `.claude/skills/battle-card-creator-skill`
3. Update `.claude/project-context.md`:
   ```markdown
   ## Recently Added Skills
   
   ### battle-card-creator-skill
   - Added: 2025-11-16
   - Purpose: Generate competitive analysis battle cards
   - Integration: Can be used to analyze competitors mentioned in project docs
   ```
4. Update `docs/REQUIREMENTS.md` with new dependencies
5. Suggest usage:
   ```
   You can now use battle-card-creator-skill to:
   - Generate competitive analysis
   - Compare your solution against competitors
   - Create battle cards for sales team
   
   Example usage:
   "Create a battle card comparing our RAG agent to OpenAI's Assistants API"
   ```

---

## Example 5: Documentation Generation

### User Input (in existing project)
```
Generate updated project documentation based on current code
```

### Claude Code Response
Claude Code will:
1. Read all SKILL.md files from `.claude/skills/`
2. Analyze code structure in `src/`
3. Review existing tests in `tests/`
4. Update `docs/PROJECT_PLAN.md`:
   - Current implementation status
   - Completed phases
   - Remaining work
5. Update `docs/REQUIREMENTS.md`:
   - Actual dependencies found in code
   - New requirements discovered
   - Updated setup instructions
6. Generate `docs/ARCHITECTURE.md` if not exists:
   - Component diagram based on code structure
   - Data flow analysis
   - Integration points

---

## Example 6: Project Validation

### User Input
```
Validate my project setup
```

### Claude Code Response
```
✅ Project Validation Results

Directory Structure:
✅ .claude/skills-repo exists
✅ .claude/skills/ contains 3 skills
✅ docs/ directory present
✅ src/ directory present
✅ tests/ directory present

Git Configuration:
✅ Git repository initialized
✅ Submodule configured correctly
✅ .gitignore present

Skills:
✅ langgraph-unstructured-tool-agent - linked correctly
✅ databricks-agent-deploy2app-skill - linked correctly
✅ pytest-test-creator - linked correctly

Files:
✅ README.md present
✅ requirements.txt present
✅ .claude/project-context.md present
✅ docs/PROJECT_PLAN.md present
✅ docs/REQUIREMENTS.md present

Dependencies:
⚠️  Warning: pytest not in requirements.txt (needed by pytest-test-creator)
⚠️  Warning: langgraph not in requirements.txt (needed by langgraph skills)

Recommendations:
1. Add missing dependencies to requirements.txt:
   - pytest>=7.4.0
   - langgraph>=0.0.26
   - databricks-vectorsearch
2. Run: pip install -r requirements.txt
3. Verify environment with: python scripts/verify_setup.py
```

---

## Example 7: Creating a Simple Python Project

### User Input
```
Create a simple Python CLI tool called "data-validator" with testing
```

### Claude Code Response
Claude Code will:
1. Create minimal project structure
2. Add only essential skills:
   - `pytest-test-creator`
   - `python-code-formatter`
3. Generate simple structure:
   ```
   data-validator/
   ├── src/
   │   ├── __init__.py
   │   ├── cli.py
   │   └── validator.py
   ├── tests/
   │   └── test_validator.py
   └── requirements.txt
   ```
4. Create `src/cli.py` with click/argparse boilerplate
5. Generate tests with pytest-test-creator
6. Setup pre-commit hooks for black+isort

---

## Example 8: Competitive Analysis Project

### User Input
```
Create a project called "product-analysis" for creating competitive battle cards
```

### Claude Code Response
Claude Code will:
1. Create documentation-focused structure
2. Add these skills:
   - `battle-card-creator-skill`
   - `jira-epic-creator-skill` (for follow-up action items)
3. Generate structure:
   ```
   product-analysis/
   ├── research/
   │   ├── competitors/
   │   └── features/
   ├── battle-cards/
   ├── epics/
   └── templates/
   ```
4. Create starter templates for research
5. Provide workflow documentation for:
   - Gathering competitive intelligence
   - Using battle-card-creator to generate cards
   - Creating Jira epics from findings

---

## Tips for Best Results

### Be Specific About Requirements
❌ Bad: "Create a project"
✅ Good: "Create a RAG agent project for searching company wikis"

### Mention Deployment if Needed
❌ Bad: "Create a LangGraph agent"
✅ Good: "Create a LangGraph agent that will be deployed to Databricks Apps"

### Specify Testing Preferences
✅ "Create a project with comprehensive test coverage"
✅ "Include the pytest-test-creator skill"

### Request Documentation Style
✅ "Create detailed documentation for a junior developer audience"
✅ "Include architecture diagrams"

### Iterative Development
1. Start minimal: "Create a basic RAG agent"
2. Add features: "Add deployment capabilities"
3. Expand: "Add competitive analysis tools"

---

## Common Patterns

### Pattern 1: Agent → Deploy
```
Skills: langgraph-* + databricks-agent-deploy2app-skill
Use: Build and deploy agents to Databricks
```

### Pattern 2: Notebook → DAB → Deploy
```
Skills: databricks-local-notebook-skill + databricks-asset-bundle-skill
Use: Develop notebooks locally and orchestrate with DABs
```

### Pattern 3: Multi-Agent System
```
Skills: 2+ langgraph agents + langgraph-multi-agent-supervisor
Use: Complex systems with specialized agents
```

### Pattern 4: Development → Testing → Formatting
```
Skills: [main skill] + pytest-test-creator + python-code-formatter
Use: Any Python project with quality standards
```

---

## Skill Recommendation Logic

Claude Code recommends skills based on keywords:

| User Mentions | Recommended Skills |
|---------------|-------------------|
| "RAG", "search", "documents" | langgraph-unstructured-tool-agent |
| "Genie", "SQL", "natural language queries" | langgraph-genie-agent |
| "multi-agent", "multiple agents" | langgraph-multi-agent-supervisor |
| "deploy", "Databricks app" | databricks-agent-deploy2app-skill |
| "notebook", "local development" | databricks-local-notebook-skill |
| "DAB", "asset bundle" | databricks-asset-bundle-skill |
| "tests", "testing" | pytest-test-creator |
| "format", "code quality" | python-code-formatter |
| "competitive", "battle card" | battle-card-creator-skill |
| "Jira", "epic", "user stories" | jira-epic-creator-skill |

---

This examples file should help you understand how to effectively use the Project Starter skill!
