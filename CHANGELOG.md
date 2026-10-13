# FWIN Data Entry v0.4.0

## Highlights

This release completes support for FN121 effort entry and introduces additional validation and usability improvements throughout the application.

## Added

### FN121 Effort Entry

Added support for:

- Site Temperature (SITEM0)
- Minimum Gear Depth (GRDEPMIN)
- Maximum Gear Depth (GRDEPMAX)
- Lift Date (EFFDT1)
- Lift Time (EFFTM1)
- Effort Status (EFFST)

### Validation

Added validation for:

- Site Temperature
- Secchi Depth
- Minimum Gear Depth
- Maximum Gear Depth

Added validation to ensure:

- Numeric values are non-negative
- Maximum Gear Depth cannot be less than Minimum Gear Depth

### User Experience

Improved error handling during record editing.

Validation errors now:

- Display user-friendly warning messages
- Keep dialogs open for correction
- Prevent application tracebacks during normal use

## Existing Functionality

- FN011 project management
- FN121 effort entry and editing
- FN123 catch summaries
- FN125 fish samples
- User-selectable database locations
- Referential integrity validation
- Species code support with leading zeros

## Known Areas for Future Improvement

- Date validation
- Time validation
- Additional automated testing
- Executable packaging refinements

## Feedback Requested

Please report:

- Data entry issues
- Validation concerns
- Workflow improvements
- Application crashes
- User interface suggestions

# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-10-09

### Added

#### Project Management

- Create new projects
- Open existing projects
- User-selectable project database locations
- Automatic loading of newly created projects

#### Workspace

- Project workspace
- Project banner
- SAM navigation panel
- Workspace-driven data entry workflows
- Automatic workspace refresh

#### FN121

- Add effort records
- Edit effort records
- Multi-SAM entry workflow
- Automatic SAM numbering
- Sticky GR field
- Sticky crew field

#### FN123

- Add catch summaries
- Edit catch summaries
- Multi-species entry workflow
- Catch summary table display

#### FN125

- Add fish samples
- Edit fish samples
- Multi-fish entry workflow
- Automatic fish numbering
- Fish table display

#### Validation

- Friendly validation dialogs
- Duplicate SAM prevention
- Duplicate catch summary prevention
- FN123 requires FN121
- FN125 requires FN123
- Project overwrite prevention

#### Data Model

- FishNet-compatible SQLite schema
- FN011 support
- FN121 support
- FN123 support
- FN125 support
- Species codes stored as three-character identifiers

### Changed

- Application workflow is now workspace-driven.
- Data-entry functions moved from File menu to workspace controls.
- Add and Edit workflows separated for FN121, FN123 and FN125.

### Known Limitations

- Record deletion not yet implemented.
- FN012 integration not yet implemented.
- FLEN and TLEN are still stored as REAL and should be converted to INTEGER in a future release.

---

## [0.2.0]

### Added

- PySide6 application shell
- Project creation dialog
- Project selection workflow

---

## [0.1.0]

### Added

- SQLite schema
- Database initialization
- Service layer
- Validation framework
- Project, effort, catch summary and fish sample models