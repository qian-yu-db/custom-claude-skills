---
name: jira-epic-creator
description: Transform documents into structured Jira epics with user stories. Use when user needs to create Jira epics from documents, requirements, or proposals, or wants to break down epics into user stories following the 5-section epic template format (Problem Statement, Proposed Solution, Existing Solutions, Deliverables/Impact, Additional Information).
---

# Jira Epic Creator

Transform documents and requirements into well-structured Jira epics with comprehensive user stories.

## When to Use This Skill

Use this skill when:
- Converting a document (Word, PDF, text) into a Jira epic
- Creating epics that follow a specific 5-section template
- Breaking down epics into actionable user stories
- Analyzing requirements documents for epic creation
- Ensuring epics have proper structure and completeness

## Epic Template Structure

Every epic must include these 5 sections in order:

1. **Problem Statement or Opportunity Statement** - Define the problem or opportunity (who, what, why)
2. **Proposed Solution** - Describe the approach and key features
3. **What solutions exist today** - Document current workarounds and alternatives
4. **Final deliverable / impact** - Define success metrics and deliverables
5. **Additional Information for Support Requested** - Dependencies, resources, risks, links

For detailed guidelines on each section, see `references/epic-template.md`.

## Workflow

### Step 1: Analyze the Document

When a user provides a document (uploaded or pasted), first read and understand its content:

```python
# For uploaded documents, use view tool
view /mnt/user-data/uploads/requirements.docx
```

Identify key elements:
- Problem descriptions or pain points
- Proposed solutions or goals
- Existing systems or workarounds
- Success metrics or KPIs
- Stakeholders and dependencies

### Step 2: Extract Key Information

Use the analysis script to identify epic components:

```bash
python scripts/analyze_doc.py <document_path>
```

This extracts:
- Problem indicators (complaints, issues, pain points)
- Solution indicators (proposals, implementations)
- Metrics and quantifiable data
- Stakeholder mentions
- Existing solution references

Review the script output to understand what information is available.

### Step 3: Create the Epic

Generate a complete epic following the 5-section template. Use the template in `assets/epic-template.md` as structure.

**Important Guidelines:**
- Be specific and concrete - avoid vague statements
- Include metrics and numbers wherever possible
- Explain WHY things matter (business impact)
- Document what exists today before proposing new solutions
- Define measurable success criteria

**Example Quality Standards:**

✅ **Good Problem Statement:**
> "Our customer support team receives 200+ tickets per week asking how to export reports. This represents 40 hours of support time weekly. Users struggle to find the export functionality, leading to frustration and decreased product satisfaction scores (NPS dropped 5 points in Q3)."

❌ **Bad Problem Statement:**
> "Users want better export features."

### Step 4: Break Down into User Stories

After creating the epic, break it down into user stories following INVEST principles:
- **Independent** - Can be developed in any order
- **Negotiable** - Details can be refined
- **Valuable** - Delivers user/business value
- **Estimable** - Team can estimate effort
- **Small** - Fits in a sprint (1-5 days)
- **Testable** - Clear acceptance criteria

**Story Categories:**

1. **Foundation Stories** (Build first)
   - Data models and schemas
   - API endpoints and authentication
   - Basic UI framework

2. **Feature Stories** (Core value)
   - User-facing functionality
   - Vertical slices of features
   - Incremental value delivery

3. **Enhancement Stories** (Added value)
   - Advanced features
   - Nice-to-have functionality
   - Performance improvements

4. **Quality Stories** (Polish)
   - Testing and QA
   - Documentation
   - Accessibility
   - Performance optimization

See `references/story-breakdown.md` for detailed guidelines and examples.

### Step 5: Format for Jira

Format the epic and stories for easy copying into Jira:

**Epic Format:**
- Use clear section headers (## for H2)
- Use bullet points for lists
- Bold key points for emphasis
- Include all 5 required sections

**Story Format:**
```
Title: [User Role] - [Action/Goal]

As a [user role]
I want [goal/desire]
So that [benefit/value]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

Technical Notes:
[Implementation details]

Definition of Done:
- [ ] Code reviewed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Product owner approval
```

Use the template in `assets/story-template.md` for consistency.

## Common Document Types

### Requirements Document
- Focus on extracting functional and non-functional requirements
- Map requirements to problem statements and solutions
- Identify constraints and dependencies

### Proposal Document
- Extract the opportunity statement
- Highlight proposed approach and alternatives
- Capture expected benefits and ROI

### Bug Report / Issue
- Convert problem description to problem statement
- Identify root cause for proposed solution
- Document current workarounds
- Define success as "bug fixed" with metrics

### Feature Request
- Extract user pain point as problem statement
- Describe requested feature as solution
- Compare to competitor features (existing solutions)
- Define adoption metrics as impact

## Best Practices

### For Epics
1. **Be specific** - Use concrete examples and metrics
2. **Quantify impact** - Include numbers, percentages, time saved
3. **Show context** - Explain why it matters to the business
4. **Document alternatives** - Show what exists today and why it's insufficient
5. **Define success** - Clear, measurable outcomes

### For Stories
1. **Vertical slicing** - Prefer full-stack stories over layer-by-layer
2. **Small scope** - Stories should be 1-5 days of work
3. **Clear acceptance** - Testable criteria for "done"
4. **Show dependencies** - Link related stories
5. **Add context** - Technical notes help developers

### For Story Breakdown
1. **Foundation first** - Build infrastructure before features
2. **Incremental value** - Each story should deliver something useful
3. **Logical order** - Sequence stories to minimize blockers
4. **Balance size** - Mix of small, medium stories (avoid all large)
5. **Include quality** - Don't forget testing and documentation stories

## Templates

### Epic Template
Use `assets/epic-template.md` as the starting point for all epics. It includes:
- All 5 required sections with examples
- Formatting guidelines
- Placeholders for content

### Story Template
Use `assets/story-template.md` for consistent story format. It includes:
- User story format
- Acceptance criteria checklist
- Technical notes section
- Definition of done
- Example completed story

## Analysis Script

The `scripts/analyze_doc.py` script helps identify epic components in documents:

```bash
# Analyze uploaded document
python scripts/analyze_doc.py /mnt/user-data/uploads/requirements.docx

# Save analysis to file
python scripts/analyze_doc.py /mnt/user-data/uploads/requirements.docx analysis.md
```

Use this as a starting point, then enhance with context and details.

## Handling Missing Information

If the document lacks information for required sections:

1. **Note what's missing** - Be explicit about gaps
2. **Make reasonable assumptions** - Document assumptions clearly
3. **Suggest follow-up questions** - Help user gather missing info
4. **Use placeholders** - `[NEEDS INPUT: stakeholder approval]`

Example:
> **Existing Solutions:**
> The document doesn't mention current workarounds. Consider:
> - Are users manually doing this task today?
> - Do competitor products offer this feature?
> - [NEEDS INPUT: Interview users about current workflow]

## Output Formatting

Create outputs in markdown format that can be easily copied to Jira:

1. **Epic first** - Complete 5-section epic
2. **Story list** - Table of contents with story titles
3. **Detailed stories** - One section per story with full details
4. **Summary** - Total story count and estimated duration

Optionally create a separate document for each story if requested.

## References

- **references/epic-template.md** - Detailed epic template with examples and guidelines
- **references/story-breakdown.md** - Comprehensive story writing and breakdown guide
- **assets/epic-template.md** - Blank epic template ready to fill
- **assets/story-template.md** - Blank story template with example

## Example Workflow

**User:** "Here's a requirements document for a new export feature. Create a Jira epic and stories."

**Claude:**
1. Reads the uploaded document
2. Runs analysis script to extract key information
3. Creates epic with all 5 sections, using metrics from document
4. Breaks down into 12-15 user stories across categories:
   - 3 foundation stories (API, data model, UI framework)
   - 6 feature stories (export formats, UI components)
   - 2 enhancement stories (bulk export, scheduling)
   - 3 quality stories (testing, docs, performance)
5. Provides formatted output ready for Jira
6. Estimates 3-4 sprints total

## Tips for Success

- **Read the entire document** before creating the epic
- **Ask clarifying questions** if critical information is missing
- **Use the analysis script** as a starting point, not the final answer
- **Include concrete examples** in problem statements
- **Quantify everything possible** - use numbers, percentages, time
- **Break stories vertically** - full stack features, not by layer
- **Size stories realistically** - 1-5 days each
- **Link dependencies** - show which stories block others
- **Review completeness** - ensure all 5 epic sections are thorough
