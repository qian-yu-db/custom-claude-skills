# Project Plan: {{PROJECT_NAME}}

## 1. Project Overview

**Project Name**: {{PROJECT_NAME}}  
**Created**: {{CREATION_DATE}}  
**Last Updated**: {{LAST_UPDATED}}

### Goal
{{PROJECT_GOAL}}

### Deliverables
{{DELIVERABLES_LIST}}

### Timeline
- **Phase 1**: Setup & Foundation ({{PHASE1_DURATION}})
- **Phase 2**: Core Implementation ({{PHASE2_DURATION}})
- **Phase 3**: Testing & Validation ({{PHASE3_DURATION}})
- **Phase 4**: Deployment ({{PHASE4_DURATION}})

---

## 2. Architecture

### Overview
{{ARCHITECTURE_OVERVIEW}}

### Components
{{COMPONENTS_LIST}}

### Data Flow
{{DATA_FLOW_DESCRIPTION}}

### Integration Points
{{INTEGRATION_POINTS}}

---

## 3. Development Phases

### Phase 1: Setup & Foundation

**Objectives:**
- Environment setup
- Skill integration verification
- Basic scaffolding

**Tasks:**
- [ ] Initialize project structure
- [ ] Configure development environment
- [ ] Verify skill installations
- [ ] Create base configuration files
- [ ] Setup version control

**Deliverables:**
- Working development environment
- Initial project structure
- Configuration files

---

### Phase 2: Core Implementation

**Objectives:**
{{PHASE2_OBJECTIVES}}

**Tasks:**
{{PHASE2_TASKS}}

**Deliverables:**
{{PHASE2_DELIVERABLES}}

---

### Phase 3: Testing & Validation

**Objectives:**
- Comprehensive testing
- Performance validation
- Bug fixes

**Tasks:**
- [ ] Write unit tests
- [ ] Integration testing
- [ ] Performance testing
- [ ] Security review
- [ ] Documentation review

**Deliverables:**
- Test suite with >80% coverage
- Performance benchmarks
- Bug fixes
- Updated documentation

---

### Phase 4: Deployment

**Objectives:**
{{PHASE4_OBJECTIVES}}

**Tasks:**
{{PHASE4_TASKS}}

**Deliverables:**
{{PHASE4_DELIVERABLES}}

---

## 4. Skills Utilized

### Skill Integration Overview
This project leverages the following skills from custom-claude-skills:

{{SKILLS_LIST}}

---

{{#each SELECTED_SKILLS}}
### {{name}}

**Purpose**: {{purpose}}

**Usage in this Project**:
{{usage}}

**Key Capabilities**:
{{capabilities}}

**Deliverables from this Skill**:
{{deliverables}}

**References**:
- SKILL.md: `.claude/skills/{{name}}/SKILL.md`
- Quick Reference: `.claude/skills/{{name}}/QUICK_REFERENCE.md`

---

{{/each}}

## 5. Dependencies

### Core Dependencies
{{CORE_DEPENDENCIES}}

### Skill-Specific Dependencies
{{SKILL_DEPENDENCIES}}

### Development Dependencies
{{DEV_DEPENDENCIES}}

### External Services
{{EXTERNAL_SERVICES}}

---

## 6. Success Criteria

### Functional Criteria
{{FUNCTIONAL_CRITERIA}}

### Technical Criteria
{{TECHNICAL_CRITERIA}}

### Performance Criteria
{{PERFORMANCE_CRITERIA}}

### Quality Criteria
- Code coverage: >80%
- Documentation: Complete
- Security: No critical vulnerabilities
- Performance: Meets requirements

---

## 7. Risks & Mitigation

### Technical Risks
{{TECHNICAL_RISKS}}

### Resource Risks
{{RESOURCE_RISKS}}

### Timeline Risks
{{TIMELINE_RISKS}}

---

## 8. Development Workflow

### Daily Workflow
1. Review project context: `.claude/project-context.md`
2. Use Claude Code with integrated skills
3. Reference skill documentation as needed
4. Update documentation as you build
5. Commit regularly with descriptive messages

### Skill Usage Workflow
{{SKILL_USAGE_WORKFLOW}}

### Testing Workflow
{{TESTING_WORKFLOW}}

### Deployment Workflow
{{DEPLOYMENT_WORKFLOW}}

---

## 9. Monitoring & Maintenance

### Monitoring
{{MONITORING_STRATEGY}}

### Maintenance Plan
{{MAINTENANCE_PLAN}}

---

## 10. Next Steps

### Immediate Actions
1. [ ] Review this project plan
2. [ ] Setup development environment
3. [ ] Read selected skills' documentation
4. [ ] Begin Phase 1 tasks

### Resources
- Project Requirements: `docs/REQUIREMENTS.md`
- Architecture Details: `docs/ARCHITECTURE.md`
- Setup Guide: `docs/SETUP.md`
- Skills Documentation: `.claude/skills/*/SKILL.md`

---

## Appendix

### Glossary
{{GLOSSARY}}

### References
- custom-claude-skills: https://github.com/qian-yu-db/custom-claude-skills
- Claude Code Docs: https://docs.claude.com/en/docs/claude-code

### Change Log
| Date | Version | Changes | Author |
|------|---------|---------|--------|
| {{CREATION_DATE}} | 1.0.0 | Initial project plan | Claude Code |
