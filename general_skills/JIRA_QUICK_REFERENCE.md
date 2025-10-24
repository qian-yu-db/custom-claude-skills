# Jira Epic Creator - Quick Reference

## Installation
Upload `jira-epic-creator.skill` to Claude

## Quick Usage

### Create Epic from Document
```
"Here's a requirements doc. Create a Jira epic with stories."
[Upload or paste document]
```

### Create Epic from Description
```
"Create a Jira epic for implementing user authentication with OAuth"
```

### Get Just Stories
```
"Break down this epic into user stories"
```

## 5 Required Epic Sections

| Section | Purpose | Key Elements |
|---------|---------|--------------|
| 1. Problem Statement | Define the problem | Who, what, why, metrics |
| 2. Proposed Solution | Describe approach | Features, architecture |
| 3. Existing Solutions | Document alternatives | Workarounds, competitors |
| 4. Deliverables/Impact | Define success | Concrete outputs, metrics |
| 5. Additional Info | Context and support | Dependencies, resources, risks |

## Story Categories

```
Foundation Stories (build first)
├── Data models, APIs
└── Auth, basic UI

Feature Stories (core value)
├── User-facing features
└── Vertical slices

Enhancement Stories (added value)
├── Advanced features
└── Performance

Quality Stories (polish)
├── Testing, docs
└── Accessibility
```

## Story Format

```markdown
Title: [User Role] - [Action]

As a [role]
I want [goal]
So that [benefit]

Acceptance Criteria:
- [ ] Testable criterion 1
- [ ] Testable criterion 2

Technical Notes:
[Implementation details]

Definition of Done:
- [ ] Code reviewed
- [ ] Tests passing
- [ ] Deployed to staging
```

## INVEST Principles

- **I**ndependent - Can develop in any order
- **N**egotiable - Details can be refined
- **V**aluable - Delivers user value
- **E**stimable - Team can estimate
- **S**mall - 1-5 days of work
- **T**estable - Clear acceptance criteria

## Good vs Bad Examples

### Problem Statement

✅ **Good:**
> "Support team receives 200+ tickets/week on exports (40 hours). NPS dropped 5 points in Q3."

❌ **Bad:**
> "Users want better export features."

### Solution

✅ **Good:**
> "Add prominent Export button with modal for PDF/Excel/CSV. Use existing API with new format handlers."

❌ **Bad:**
> "Add an export button."

### Story Title

✅ **Good:**
> "Report Viewer - Export Report as PDF"

❌ **Bad:**
> "Export Feature"

## Document Analysis

Extract key info from documents:

```bash
python scripts/analyze_doc.py document.txt
```

Finds:
- Problem indicators
- Solution proposals
- Metrics and numbers
- Stakeholders
- Existing solutions

## Common Commands

### Refine Output
- "Add more metrics to the problem statement"
- "Break story #5 into smaller pieces"
- "Add testing stories"
- "Reorder stories by dependency"

### Different Formats
- "Create separate files for each story"
- "Format as a table"
- "Export as JSON"

### Add Context
- "Focus on mobile users"
- "Add accessibility requirements"
- "Include performance metrics"

## Sizing Guide

| Size | Duration | Examples |
|------|----------|----------|
| XS | 1 day | Simple UI change, minor bug fix |
| S | 2-3 days | Single feature, simple API |
| M | 3-5 days | Complex feature (backend + frontend) |
| L | 5+ days | **SPLIT INTO SMALLER STORIES** |

## Quality Checklist

### Epic
- [ ] All 5 sections complete
- [ ] Specific metrics included
- [ ] Business impact explained
- [ ] Success criteria defined
- [ ] Dependencies documented

### Stories
- [ ] Follows INVEST principles
- [ ] Clear acceptance criteria (3-5 items)
- [ ] Technical notes included
- [ ] Definition of done present
- [ ] Sized appropriately (1-5 days)

## Tips

**For Best Results:**
- Include metrics in your documents
- Mention specific user complaints
- List current workarounds
- Note dependencies
- Provide context on business impact

**If Information Missing:**
- Claude will note gaps explicitly
- Make reasonable assumptions (documented)
- Suggest follow-up questions
- Use placeholders `[NEEDS INPUT: ...]`

**Iterating:**
- Ask Claude to add more detail
- Request story breakdown
- Add specific story types
- Reorder by priority

## Example Workflow

1. Upload requirements.docx
2. "Create Jira epic and stories"
3. Review output
4. "Add 3 more stories for mobile support"
5. "Break down story #8 into smaller pieces"
6. Copy epic to Jira
7. Copy stories to Jira

## Templates Available

- `assets/epic-template.md` - Blank epic template
- `assets/story-template.md` - Blank story template
- `references/epic-template.md` - Detailed guidelines
- `references/story-breakdown.md` - Story writing guide

## Getting Help

Ask Claude:
- "Show me an example epic"
- "How do I write good acceptance criteria?"
- "What's wrong with this epic?"
- "Break this down differently"
- "Add more technical detail"
