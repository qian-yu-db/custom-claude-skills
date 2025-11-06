# Jira Epic Creator Skill

Transform any document into a structured Jira epic with comprehensive user stories following your organization's 5-section template.

## What This Skill Does

This skill helps you:

1. **Convert documents to Jira epics** - Transform requirements docs, proposals, or any document into properly structured epics
2. **Follow your epic template** - Ensures all 5 required sections are included and complete
3. **Break down into stories** - Automatically generates user stories with acceptance criteria
4. **Analyze documents** - Extracts problems, solutions, metrics, and stakeholders from text
5. **Ensure quality** - Enforces best practices for epic and story writing

## Epic Template (5 Required Sections)

Every epic created includes:

1. **Problem Statement or Opportunity Statement**
   - Who is affected, what the issue is, why it matters
   - Includes metrics and quantifiable impact

2. **Proposed Solution**
   - High-level approach and key features
   - Technical approaches and architecture notes

3. **What solutions exist today to address the problem / opportunity statement**
   - Current workarounds and their limitations
   - Competitor solutions
   - Why existing solutions are inadequate

4. **What does the final deliverable / impact for this project look like?**
   - Concrete deliverables (features, docs, etc.)
   - Quantified expected impact with metrics
   - Success criteria

5. **Additional Information for Support Requested**
   - Dependencies on other teams/projects
   - Resource requirements (engineers, designers, etc.)
   - Links to research, designs, docs
   - Risks and constraints

## How to Use

### Quick Start

1. **Upload or paste your document**
   ```
   "Here's a requirements document for a new feature. Create a Jira epic and stories."
   ```

2. **Claude will:**
   - Read and analyze the document
   - Extract key information (problems, solutions, metrics)
   - Create a complete epic with all 5 sections
   - Break it down into 10-20 user stories
   - Format everything for easy Jira import

3. **You get:**
   - Complete epic ready to copy into Jira
   - User stories with acceptance criteria
   - Proper categorization (foundation, feature, quality stories)
   - Story dependencies and ordering

### What Gets Analyzed

The skill automatically extracts:
- **Problem indicators**: Issues, pain points, complaints
- **Solution proposals**: Implementations, features, approaches
- **Metrics**: Numbers, percentages, time savings, costs
- **Stakeholders**: Users, teams, roles mentioned
- **Existing solutions**: Current workflows and workarounds
- **Impact statements**: Benefits, outcomes, goals

### Story Breakdown

Stories are organized into categories:

**Foundation Stories** (build first):
- Data models and APIs
- Authentication/authorization
- Basic UI framework

**Feature Stories** (core value):
- User-facing functionality
- Vertical slices of features
- Incremental value delivery

**Enhancement Stories** (added value):
- Advanced features
- Performance improvements
- Nice-to-have functionality

**Quality Stories** (polish):
- Testing and QA
- Documentation
- Accessibility
- Performance optimization

## Features

### 📋 Epic Templates
- Blank template ready to fill (`assets/epic-template.md`)
- Detailed examples for each section
- Quality guidelines and anti-patterns

### 📝 Story Templates
- User story format with example
- Acceptance criteria checklist
- Technical notes structure
- Definition of done

### 🔍 Document Analysis
- Python script to extract epic components
- Identifies problems, solutions, metrics
- Highlights stakeholders and dependencies
- Generates analysis report

### 📚 Comprehensive Guides
- Epic writing best practices
- Story breakdown principles (INVEST)
- Vertical slicing vs horizontal
- Sizing and estimation guidance

## Example Output

### Input Document
A 3-page requirements doc describing user complaints about slow report loading

### Output

**Epic**: Report Performance Optimization

With complete 5-section structure including:
- Problem: "Users wait 30+ seconds for reports, 45% abandon, $50k ARR at risk"
- Solution: "Implement caching layer, optimize queries, add loading indicators"
- Existing: "Current workarounds and why they fail"
- Deliverables: "3x faster load times, 90% under 10 seconds, metrics dashboard"
- Support: "Needs 2 backend engineers, 3 sprints, depends on DB upgrade"

**12 User Stories**:
- 3 foundation (caching infrastructure, query optimization framework)
- 5 feature (implement caching for each report type)
- 2 enhancement (predictive preloading, cache warming)
- 2 quality (performance testing, monitoring dashboard)

All stories include acceptance criteria, technical notes, and definition of done.

## Best Practices Built In

### Epic Writing
✅ Specific problem statements with metrics
✅ Quantified expected impact
✅ Clear success criteria
✅ All 5 sections complete
✅ Business context explained

### Story Writing
✅ INVEST principles followed
✅ Vertical slicing (full-stack stories)
✅ 1-5 day sizing
✅ Clear acceptance criteria
✅ Proper dependency ordering

## Common Use Cases

### Requirements Document
Upload a product requirements doc → Get epic + stories ready for sprint planning

### Feature Request
Paste a detailed feature request → Get structured epic with implementation stories

### Bug Report
Share a critical bug report → Get epic with root cause analysis and fix stories

### Proposal Document
Upload a project proposal → Get complete epic with all dependencies documented

### Meeting Notes
Paste brainstorming notes → Get organized epic with prioritized stories

## What Makes This Skill Special

1. **Enforces your template** - Ensures all 5 required sections are complete
2. **Extracts metrics** - Finds and highlights quantifiable data
3. **Smart breakdown** - Creates logical story sequence with dependencies
4. **Quality focused** - Includes testing and documentation stories automatically
5. **Ready for Jira** - Formatted output that copies cleanly

## Tips for Best Results

### Good Input Documents
- Include specific user complaints or data
- Mention current workarounds
- List stakeholders and teams
- Include metrics where possible
- Note dependencies and constraints

### If Information is Missing
Claude will:
- Note what's missing explicitly
- Make reasonable assumptions (documented)
- Suggest follow-up questions
- Use placeholders like `[NEEDS INPUT: user interview data]`

### Iterating on Output
You can ask Claude to:
- "Add more stories for the testing phase"
- "Break story #5 into smaller pieces"
- "Add more metrics to the problem statement"
- "Rewrite the solution to focus on mobile users"

## Files Included

```
jira-epic-creator/
├── SKILL.md                          # Main skill instructions
├── references/
│   ├── epic-template.md              # Detailed epic guidelines with examples
│   └── story-breakdown.md            # Story writing comprehensive guide
├── assets/
│   ├── epic-template.md              # Blank fillable epic template
│   └── story-template.md             # Blank fillable story template
└── scripts/
    └── analyze_doc.py                # Document analysis script
```

## Requirements

- Any text document (Word, PDF, Google Doc, plain text)
- The docx skill (for reading Word documents)
- The pdf skill (for reading PDF documents)

## Example Workflow

1. **User uploads document**: "product_requirements_v2.docx"
2. **Claude reads it**: Uses docx skill to extract text
3. **Claude analyzes**: Identifies problems, solutions, metrics
4. **Claude creates epic**: All 5 sections with specific details
5. **Claude breaks down**: 15 stories organized by category
6. **Claude formats**: Ready to copy into Jira
7. **User refines**: "Add stories for mobile support"
8. **Claude updates**: Adds 3 mobile-specific stories

## Support

### Getting Help
Ask Claude:
- "Show me an example epic for a payment feature"
- "How should I write acceptance criteria?"
- "Break this epic into more granular stories"
- "What's missing from this epic?"

### Troubleshooting
- **Epic too vague**: Ask Claude to add more specific metrics and examples
- **Too many stories**: Ask to combine related stories
- **Missing context**: Upload additional documents or provide more details
- **Wrong format**: Ask Claude to reformat for your Jira fields

## Version

Created for Jira epic format with 5-section template structure (October 2025).
