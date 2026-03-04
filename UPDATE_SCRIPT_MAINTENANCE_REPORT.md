## Update Script Maintenance Report

Date: 2026-03-04

- Root cause: automation was tied to mixed triggers and lacked explicit write permission.
- Fixes made: simplified workflow to scheduled/manual execution, upgraded action versions, added `permissions: contents: write`, and kept safe commit guard.
- Validation: reviewed workflow syntax and commit path targeting for generated `data/` and `archive/` outputs.
- Known blockers: none identified in this remediation pass.
