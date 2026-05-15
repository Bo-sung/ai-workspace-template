# Google Sheets Project Management Schema

Initial project management uses Google Sheets.
Obsidian Markdown remains the source of truth for planning documents.
Git manages versions of code and Obsidian documents.
Google Sheets is used for tasks, schedule, status, commit linking, and AI modification queues.

This schema is designed to be migration-friendly for future adoption of GitHub Issues / GitHub Projects.

## Recommended Sheets

1. **Project_Master**: Main task tracker
2. **Templates**: Standard task/issue templates
3. **Git_Log**: Synchronization of git commit history
4. **Docs_Index**: Index of Obsidian markdown files
5. **Schedule**: Timeline and milestones
6. **Change_Log**: Log of major status changes
7. **AI_Queue**: Tasks queued for AI workers
8. **AI_Output**: Draft outputs from AI workers
9. **Proposed_Changes**: AI modification proposals

## Project_Master Columns

- **ID**: Unique identifier (e.g., TSK-001). Never change this.
- **GitHub Issue #**: For future migration mapping.
- **Type**: Feature, Bug, Docs, QA, Planning, Chore
- **Status**: Backlog, Ready, In Progress, Review, Done, Canceled
- **Priority**: P0, P1, P2, P3
- **Title**: Short description of the task.
- **Description**: Markdown formatted description.
- **Acceptance Criteria**: Markdown formatted criteria for completion.
- **Owner**: Assigned person or AI role.
- **Due**: Target date.
- **Milestone**: Target release or sprint.
- **Labels**: Comma-separated tags.
- **Source Doc**: Relative path to Obsidian Markdown doc.
- **Related Branch**: Git branch name.
- **Related Commits**: Comma-separated commit SHAs.
- **Created At**: Timestamp.
- **Updated At**: Timestamp.
- **Migration Status**: Blank, Pending, Migrated.
- **AI Status**: e.g., AI Draft Ready, AI Reviewing.
- **Notes**: Additional context.

## Operating Rules

1. IDs are immutable. Use `Status=Canceled` instead of deleting rows.
2. `Description` and `Acceptance Criteria` must be Markdown.
3. `Source Doc` uses relative paths from the Obsidian repo root.
4. AI workers must not directly edit `Project_Master`.
5. AI creates drafts in `Proposed_Changes`.
6. Only user-approved items from `Proposed_Changes` are merged into the main tracking sheets or codebase.
7. Bulk edits are limited to 10 rows per operation.
8. Modifying Status/Priority/Due requires explicit human approval.
