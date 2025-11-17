# Requirements: {{PROJECT_NAME}}

**Version**: 1.0.0  
**Last Updated**: {{LAST_UPDATED}}

---

## 1. Functional Requirements

### Core Features
{{CORE_FEATURES}}

### User Stories
{{USER_STORIES}}

### Feature Requirements
{{FEATURE_REQUIREMENTS}}

---

## 2. Technical Requirements

### Environment Requirements

**Python Version**: {{PYTHON_VERSION}}  
**Operating System**: {{OS_REQUIREMENTS}}  
**Required Tools**:
- Claude Code
- Git
- {{ADDITIONAL_TOOLS}}

### System Requirements
- **CPU**: {{CPU_REQUIREMENTS}}
- **Memory**: {{MEMORY_REQUIREMENTS}}
- **Storage**: {{STORAGE_REQUIREMENTS}}
- **Network**: {{NETWORK_REQUIREMENTS}}

---

## 3. Dependencies

### Core Python Packages
```txt
{{CORE_PACKAGES}}
```

### Skill-Specific Dependencies

{{#each SELECTED_SKILLS}}
#### {{name}}
```txt
{{dependencies}}
```
**Installation**:
```bash
{{installation_commands}}
```

**Configuration**:
{{configuration_notes}}

---

{{/each}}

### Development Dependencies
```txt
{{DEV_PACKAGES}}
```

---

## 4. Environment Setup

### 4.1 Prerequisites Checklist
- [ ] Python {{PYTHON_VERSION}} installed
- [ ] Git installed and configured
- [ ] Claude Code installed
- [ ] {{ADDITIONAL_PREREQUISITES}}

### 4.2 Installation Steps

#### Step 1: Clone Repository
```bash
# Clone with submodules (includes skills)
git clone --recurse-submodules {{REPO_URL}}
cd {{PROJECT_NAME}}
```

#### Step 2: Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n {{PROJECT_NAME}} python={{PYTHON_VERSION}}
conda activate {{PROJECT_NAME}}
```

#### Step 3: Install Dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

#### Step 4: Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Required variables:
{{REQUIRED_ENV_VARS}}
```

#### Step 5: Verify Installation
```bash
# Run verification script
python scripts/verify_setup.py
```

---

## 5. Configuration Requirements

### Application Configuration
**File**: `configs/config.yaml`

```yaml
{{CONFIG_YAML_TEMPLATE}}
```

### Skill-Specific Configuration

{{#each SELECTED_SKILLS}}
#### {{name}}
**Configuration File**: {{config_file}}

{{config_description}}

**Example**:
```yaml
{{config_example}}
```

---

{{/each}}

---

## 6. External Services

### Required Services
{{REQUIRED_SERVICES}}

### Optional Services
{{OPTIONAL_SERVICES}}

### API Keys & Credentials
{{API_KEYS_NEEDED}}

---

## 7. Development Environment

### IDE Recommendations
- **VS Code** with Python extension
- **PyCharm** Professional
- **Cursor** with Claude integration

### Recommended VS Code Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    {{ADDITIONAL_EXTENSIONS}}
  ]
}
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
  
  {{ADDITIONAL_HOOKS}}
```

---

## 8. Testing Requirements

### Unit Testing
- **Framework**: pytest
- **Coverage Target**: >80%
- **Test Location**: `tests/`

### Integration Testing
{{INTEGRATION_TESTING_REQUIREMENTS}}

### Performance Testing
{{PERFORMANCE_TESTING_REQUIREMENTS}}

### Test Data
{{TEST_DATA_REQUIREMENTS}}

---

## 9. Security Requirements

### Authentication & Authorization
{{AUTH_REQUIREMENTS}}

### Data Security
{{DATA_SECURITY_REQUIREMENTS}}

### Secrets Management
{{SECRETS_MANAGEMENT}}

### Compliance
{{COMPLIANCE_REQUIREMENTS}}

---

## 10. Performance Requirements

### Response Times
{{RESPONSE_TIME_REQUIREMENTS}}

### Throughput
{{THROUGHPUT_REQUIREMENTS}}

### Resource Limits
{{RESOURCE_LIMITS}}

### Scalability
{{SCALABILITY_REQUIREMENTS}}

---

## 11. Documentation Requirements

### Code Documentation
- Docstrings for all public functions/classes
- Type hints throughout codebase
- Inline comments for complex logic

### User Documentation
- README.md with quick start guide
- API documentation (if applicable)
- Usage examples
- Troubleshooting guide

### Developer Documentation
- Architecture documentation
- Setup guide (this document)
- Contribution guidelines
- Skill integration notes

---

## 12. Quality Requirements

### Code Quality
- **Linting**: Ruff/Black
- **Type Checking**: mypy
- **Complexity**: Max cyclomatic complexity: 10
- **Test Coverage**: Minimum 80%

### Code Review
- All changes require review
- Automated checks must pass
- Documentation must be updated

---

## 13. Deployment Requirements

### Deployment Targets
{{DEPLOYMENT_TARGETS}}

### CI/CD Requirements
{{CICD_REQUIREMENTS}}

### Monitoring Requirements
{{MONITORING_REQUIREMENTS}}

---

## 14. Skill-Specific Setup

### Verify Skills Installation
```bash
# List installed skills
ls -la .claude/skills/

# Verify submodule
git submodule status
```

### Update Skills
```bash
# Update all skills to latest
git submodule update --remote

# Update specific skill
cd .claude/skills-repo
git pull origin main
```

### Add New Skill
```bash
# Link additional skill
ln -s .claude/skills-repo/path/to/skill .claude/skills/skill-name

# Update project documentation
# Run: "Update project documentation with new skill"
```

---

## 15. Troubleshooting

### Common Issues

#### Submodule not initialized
```bash
git submodule update --init --recursive
```

#### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Environment variable issues
```bash
# Verify .env file exists and has correct values
cat .env

# Source environment
source .env  # Linux/Mac
```

#### Skill not found
```bash
# Verify symlink
ls -la .claude/skills/

# Recreate symlink
ln -sf ../.claude/skills-repo/path/to/skill .claude/skills/skill-name
```

---

## 16. Support & Resources

### Documentation
- Project Plan: `docs/PROJECT_PLAN.md`
- Architecture: `docs/ARCHITECTURE.md`
- Skills: `.claude/skills/*/SKILL.md`

### External Resources
- custom-claude-skills: https://github.com/qian-yu-db/custom-claude-skills
- Claude Code: https://docs.claude.com/en/docs/claude-code
- {{ADDITIONAL_RESOURCES}}

### Getting Help
{{SUPPORT_CHANNELS}}

---

## Appendix A: Dependency Matrix

| Package | Version | Purpose | Required By |
|---------|---------|---------|-------------|
{{DEPENDENCY_MATRIX}}

---

## Appendix B: Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
{{ENV_VARS_TABLE}}

---

## Appendix C: Verification Checklist

### Pre-Development Checklist
- [ ] All prerequisites installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Skills linked correctly
- [ ] Tests pass
- [ ] Documentation reviewed

### Development Ready
- [ ] Can run `python src/main.py` without errors
- [ ] Can run `pytest` and tests pass
- [ ] Can access external services (if applicable)
- [ ] Claude Code can read skills
- [ ] Configuration files are valid

---

**Change Log**

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| {{CREATION_DATE}} | 1.0.0 | Initial requirements | Claude Code |
