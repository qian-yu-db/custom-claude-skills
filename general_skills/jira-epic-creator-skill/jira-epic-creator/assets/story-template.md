# User Story Template

## Story Title
[User Role] - [Action/Goal]

## Story Description

**As a** [user role]
**I want** [goal/desire]
**So that** [benefit/value]

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] [Specific, testable criterion 4]

## Technical Notes

[Add implementation details, architectural considerations, dependencies, or technical constraints here]

**Dependencies:**
- [List any blocking stories or external dependencies]

**Technical Approach:**
- [High-level implementation approach]

**APIs/Endpoints:**
- [Any APIs that need to be created or called]

**Database Changes:**
- [Any schema changes required]

## Definition of Done

- [ ] Code complete and peer reviewed
- [ ] Unit tests written and passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Deployed to staging environment
- [ ] QA testing completed
- [ ] Product owner acceptance
- [ ] Deployed to production

## Additional Information

**Story Points:** [Estimate: 1, 2, 3, 5, 8, 13]

**Priority:** [High / Medium / Low]

**Sprint:** [Sprint number or name]

**Assignee:** [Team member name]

**Labels:** [Add relevant labels: frontend, backend, bug, enhancement, etc.]

**Related Stories:**
- [Link to related or dependent stories]

**Mockups/Designs:**
- [Link to design files or attach images]

**User Research:**
- [Link to user interviews, surveys, or data]

## Questions/Risks

- [Any open questions that need clarification]
- [Any identified risks or concerns]

---

## Example Story

### Story Title
Report Viewer - Export Report as PDF

### Story Description

**As a** report viewer
**I want** to export my report as a PDF
**So that** I can share it offline or print it with preserved formatting

### Acceptance Criteria

- [ ] "Export" button is visible in top-right corner of all report pages
- [ ] Clicking "Export" opens a modal with format options (PDF, Excel, CSV)
- [ ] Selecting PDF generates a downloadable PDF file
- [ ] PDF maintains all report formatting, colors, and branding
- [ ] Loading indicator is shown during PDF generation (max 10 seconds)
- [ ] Error message is shown if export fails with retry option
- [ ] Exported PDF filename includes report name and timestamp

### Technical Notes

**Dependencies:**
- Requires export API endpoint (Story #123)
- Requires authentication middleware (Story #124)

**Technical Approach:**
- Use wkhtmltopdf library for PDF generation
- Generate PDF server-side via POST /api/reports/{id}/export
- Return signed S3 URL for download
- Implement 60-second timeout with retry logic

**APIs/Endpoints:**
- POST /api/reports/{id}/export
  - Body: { format: 'pdf', options: {...} }
  - Response: { downloadUrl: string, expiresAt: timestamp }

**Database Changes:**
- Add export_history table to track exports
- Columns: id, user_id, report_id, format, created_at, file_size

### Definition of Done

- [x] Code complete and peer reviewed
- [x] Unit tests written and passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Deployed to staging environment
- [ ] QA testing completed
- [ ] Product owner acceptance
- [ ] Deployed to production

### Additional Information

**Story Points:** 5

**Priority:** High

**Sprint:** Sprint 42

**Assignee:** Jane Developer

**Labels:** frontend, backend, feature, export

**Related Stories:**
- Epic: Export Report Functionality (#100)
- Depends on: Export API Endpoint (#123)
- Depends on: Auth Middleware (#124)
- Blocks: Export as Excel (#126)

**Mockups/Designs:**
- Figma link: [https://figma.com/...]

**User Research:**
- User survey results: 85% of users want PDF export
- Support ticket analysis: 200 tickets/week mention export

### Questions/Risks

- Q: Should we support custom page sizes for PDF?
  - A: Start with standard A4, add custom sizes in Phase 2
- Risk: PDF generation may be slow for large reports (>100 pages)
  - Mitigation: Implement async job queue for large reports
