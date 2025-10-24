# Story Breakdown Guidelines

## Story Structure

Each user story should follow this format:

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
[Implementation details, dependencies, considerations]

Definition of Done:
- [ ] Code complete and reviewed
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Product owner approval
```

## Story Breakdown Principles

### 1. Size and Scope
- Stories should be completable in 1-5 days
- If larger, break down further into smaller stories
- Each story should deliver incremental value
- Stories should be testable independently

### 2. INVEST Criteria

Stories should be:
- **Independent**: Can be developed in any order
- **Negotiable**: Details can be discussed and refined
- **Valuable**: Delivers value to users or business
- **Estimable**: Team can estimate effort
- **Small**: Small enough to fit in a sprint
- **Testable**: Clear acceptance criteria exist

### 3. Vertical Slicing

Prefer vertical slices (full stack) over horizontal (by layer):

**Good (Vertical)**:
- Story 1: "Export single report as PDF"
- Story 2: "Export single report as Excel"
- Story 3: "Export multiple reports at once"

**Bad (Horizontal)**:
- Story 1: "Build export backend API"
- Story 2: "Build export frontend UI"
- Story 3: "Connect frontend to backend"

### 4. Dependencies and Ordering

- Identify dependencies between stories
- Order stories to minimize blockers
- Foundation stories come first (auth, APIs, data models)
- UI stories typically come after backend stories
- Testing and polish stories come last

## Common Story Types

### Feature Stories
Implement new user-facing functionality
```
Title: User - Export report as PDF
As a report viewer
I want to export my report as a PDF
So that I can share it offline or print it

Acceptance Criteria:
- [ ] Export button visible on all report pages
- [ ] Clicking export opens format selection modal
- [ ] PDF option generates downloadable PDF
- [ ] PDF maintains report formatting and branding
- [ ] Loading indicator shown during generation
```

### Technical Stories
Non-user-facing infrastructure work
```
Title: Backend - Implement PDF generation service
As a developer
I want a reliable PDF generation service
So that we can support PDF exports

Acceptance Criteria:
- [ ] Service accepts report data and returns PDF
- [ ] Handles reports up to 1000 pages
- [ ] Response time under 5 seconds for typical reports
- [ ] Includes error handling and retry logic
- [ ] Logging and monitoring configured
```

### Bug Fix Stories
Fix existing issues
```
Title: Fix - Report export timeout on large datasets
As a user
I want large reports to export successfully
So that I don't lose my work

Acceptance Criteria:
- [ ] Reports with 10,000+ rows export without timeout
- [ ] User sees progress indicator during export
- [ ] Error message shown if export fails
- [ ] Failed exports can be retried
```

### Documentation Stories
Create or update documentation
```
Title: Documentation - Export feature user guide
As a user
I want clear documentation on how to export reports
So that I can use the feature effectively

Acceptance Criteria:
- [ ] Step-by-step export guide written
- [ ] Screenshots included for each step
- [ ] All export formats documented
- [ ] Troubleshooting section added
- [ ] Video tutorial recorded (2-3 minutes)
```

### Testing Stories
Comprehensive testing efforts
```
Title: QA - Export feature end-to-end testing
As a QA engineer
I want to validate all export scenarios
So that we ship a quality feature

Acceptance Criteria:
- [ ] Test all report types with all export formats
- [ ] Test edge cases (empty reports, huge reports)
- [ ] Test error scenarios (network failure, timeout)
- [ ] Test cross-browser compatibility
- [ ] Test accessibility compliance
- [ ] Performance testing completed
```

## Breaking Down Epics into Stories

### Step 1: Identify Major Themes
Group functionality into logical themes:
- Core functionality
- User interface
- Backend/API
- Testing
- Documentation
- Polish/Enhancements

### Step 2: Create Foundation Stories First
Start with stories that other stories depend on:
- Data models
- API endpoints
- Authentication/Authorization
- Basic UI framework

### Step 3: Layer on Feature Stories
Build incrementally:
- Minimum viable feature first
- Add format options
- Add bulk operations
- Add advanced features

### Step 4: Add Quality Stories
- Testing stories
- Documentation stories
- Performance optimization
- Accessibility improvements

### Step 5: Include Polish Stories
- UI improvements
- Animation and transitions
- Help text and tooltips
- Onboarding flows

## Story Sizing Guide

### Extra Small (1 day)
- Simple UI changes
- Minor bug fixes
- Small configuration changes

### Small (2-3 days)
- Single feature implementation
- Simple API endpoint
- Basic UI component

### Medium (3-5 days)
- Complex feature with backend + frontend
- API with multiple endpoints
- Feature with multiple edge cases

### Large (5+ days - SPLIT THIS)
If a story is this large, break it down further

## Example Epic Breakdown

**Epic**: Export Report Functionality

**Foundation Stories** (Do First):
1. Backend - Create export API endpoint structure
2. Backend - Implement report data serialization
3. Frontend - Create export modal component

**Feature Stories** (Core Value):
4. User - Export single report as PDF
5. User - Export single report as Excel
6. User - Export single report as CSV
7. User - Select custom date range for export
8. User - Export multiple reports at once

**Enhancement Stories** (Added Value):
9. User - Schedule automated exports
10. User - Save export preferences
11. User - Share exported files via email

**Quality Stories** (Polish):
12. QA - Comprehensive export testing
13. Documentation - Export user guide
14. Performance - Optimize large report exports
15. Accessibility - Ensure export UI is accessible

**Estimated Total**: 15 stories across 3-4 sprints

## Tips for Good Story Writing

1. **Use "As a [role]" format**: Makes user focus clear
2. **One story, one goal**: Don't combine multiple features
3. **Include concrete acceptance criteria**: Make it testable
4. **Add technical notes**: Help developers understand complexity
5. **Estimate effort**: Use story points or time estimates
6. **Link related stories**: Show dependencies clearly
7. **Attach mockups**: Visual references help clarity
8. **Reference research**: Link to user interviews, data
