# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Set default render engine to Local PlantUML to prioritize offline execution.
- Removed default Remote Server URL from settings.
- Improved the configuration saved success message to be more concise.
- Improved the error message when the remote rendering server is unavailable to avoid displaying long URLs.

### Fixed
- Fixed an issue where the packaged macOS `.app` bundle opened the file explorer in the root directory instead of the directory containing the application.
- Modified the file explorer to show the full filesystem structure, allowing navigation upwards from the starting directory.
- Added a 5-second timeout to remote rendering requests to prevent long UI freezes when the server is unreachable.

### Added
- Added local PlantUML rendering execution mode using `java -jar plantuml.jar` via temporary files processing to avoid stdout corruption.
- Integrated the pure Java `Smetana` layout engine (`-Playout=smetana`) to entirely remove the requirement for installing Graphviz system-wide on any OS.
- Added automatic downloading of `plantuml.jar` from GitHub if it's missing locally.
- Supported toggling between Remote Server and Local PlantUML rendering directly in the Settings dialog.
- Async background image rendering capability (using QThread) ensuring smooth UI.
- Auto-render sequence triggered automatically when selecting a valid file.
- "Unsaved Changes" protection prompt added when closing application or selecting another file with pending edits.
- Image Viewer zoom controls (Zoom In, Zoom Out, Actual Size, Fit to Window) added to the Toolbar.
- Refined text editor syntax highlighting colors to match Azure PlantUML examples (Teal properties, Brown strings, Red comments).
- Three-pane layout with integrated text Editor (`ui/syntax_highlighter.py`).
- Syntax highlighting for PlantUML keywords, arrows, and comments.
- "Save File" toolbar action to save source edits.
- Default tree view directory is now the current working directory.
- Initial project structure.
- Documentation rules, tech stack configuration.
- `plantuml_encoder.py` core for encoding strings and `api_client` for communication with the PlantUML server.
- PyQt6 User Interface with dual pane view and settings dialog.
- Core settings manager matching `TECH_STACK.md` guidelines for database/json migration.
- Localization (CS/EN) logic and integration into components matching rules.
