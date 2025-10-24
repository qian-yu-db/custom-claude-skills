# Jira Epic Template Structure

## Epic Format

Every epic must include the following sections in order:

### 1. Problem Statement or Opportunity Statement
**Purpose**: Clearly define the problem being solved or the opportunity being pursued.

**Guidelines**:
- Be specific about WHO is affected (users, customers, team)
- Explain WHAT the problem/opportunity is
- Describe WHY it matters (impact, cost, risk)
- Include quantifiable metrics when possible

**Good Example**:
> Our customer support team receives 200+ tickets per week asking how to export reports. This represents 40 hours of support time weekly. Users struggle to find the export functionality, leading to frustration and decreased product satisfaction scores (NPS dropped 5 points in Q3).

**Bad Example**:
> Users want better export features.

### 2. Proposed Solution
**Purpose**: Describe the proposed approach to solve the problem or capture the opportunity.

**Guidelines**:
- Outline the high-level solution approach
- Explain HOW it addresses the problem statement
- Include key features or capabilities
- Mention any critical technical approaches or architectural decisions

**Good Example**:
> Implement a prominent "Export" button in the top-right of all report pages that opens a modal with export options (PDF, Excel, CSV). Add contextual help tooltips and a quick-start guide. Use the existing reporting API backend with new export format handlers.

**Bad Example**:
> Add an export button.

### 3. What solutions exist today to address the problem / opportunity statement
**Purpose**: Document existing solutions, workarounds, or related features.

**Guidelines**:
- List current workarounds users employ
- Mention competitor solutions if relevant
- Explain why current solutions are inadequate
- Note any existing internal tools or features that partially address this

**Good Example**:
> Currently, users can:
> - Use browser "Print to PDF" (loses formatting, breaks on large reports)
> - Copy-paste data into Excel (time-consuming, error-prone)
> - Request exports from support team (slow, creates bottleneck)
> 
> Competitors like DataViz Pro offer one-click export with format selection, which our users cite as a key advantage.

**Bad Example**:
> There are some workarounds but they don't work well.

### 4. What does the final deliverable / impact for this project look like?
**Purpose**: Define success criteria and expected outcomes.

**Guidelines**:
- List concrete deliverables (features, documentation, etc.)
- Quantify expected impact with metrics
- Define success criteria that can be measured
- Include timeline expectations if relevant

**Good Example**:
> **Deliverables**:
> - Export functionality on all 12 report types
> - Support for PDF, Excel, and CSV formats
> - In-app help documentation and tooltips
> - User guide video (2-3 minutes)
> 
> **Expected Impact**:
> - Reduce support tickets related to exports by 80% (from 200 to 40/week)
> - Improve NPS score by 3-5 points
> - Save 30+ support hours per week
> - Increase report usage by 25% (currently 2,000 reports/month)

**Bad Example**:
> Users will be able to export reports and will be happier.

### 5. Additional Information for Support Requested
**Purpose**: Provide context, dependencies, and resources needed.

**Guidelines**:
- List dependencies (other teams, projects, systems)
- Note resource requirements (design, eng, PM hours)
- Include relevant links (docs, prototypes, research)
- Mention risks or constraints
- Add any stakeholder information

**Good Example**:
> **Dependencies**:
> - Design team: 40 hours for mockups and user testing
> - Backend team: Integration with reporting API (estimated 2 sprints)
> - Dependency on Q4 API refactor project (blocks implementation)
> 
> **Resources**:
> - Frontend: 1 engineer, 3 sprints
> - QA: 1 tester, 1 sprint
> - PM: 20 hours coordination
> 
> **Links**:
> - User research findings: [link]
> - Competitor analysis: [link]
> - Technical design doc: [link]
> 
> **Risks**:
> - API performance may degrade with large exports (needs load testing)
> - PDF rendering library licensing costs ($5k/year)

**Bad Example**:
> We'll need some help from other teams.

## Formatting Guidelines

- Use clear, descriptive section headers (H2 or H3)
- Use bullet points for lists
- Use bold for emphasis on key points
- Include numbers and metrics whenever possible
- Keep paragraphs concise (3-4 sentences max)
- Use tables for comparing options or listing many items

## Common Mistakes to Avoid

1. **Too vague**: "Improve user experience" → Specify what and how
2. **No metrics**: "Make it faster" → By how much? Current vs target?
3. **Missing context**: Explain why this matters to the business
4. **No alternatives**: Always document what exists today
5. **Unclear success**: Define measurable outcomes upfront
