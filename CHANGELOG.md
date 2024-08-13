# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.4] - 2024-08-12

### Fixed
- Functions used in global scope (decorator, default args) are sorted correctly.


## [0.1.3] - 2024-08-12

### Fixed
- Module docstrings stay sorted above imports.
- Add cycle detection. No longer removes nodes from files with cycles.


## [0.1.2] - 2024-08-11

### Fixed
- Fixed bug where using an imported symbol would cause the target symbol to sort too high in the output, creating invalid code.
- Sort `if TYPE_CHECKING:` blocks into the "imports" section


## [0.1.1] - 2024-08-03

### Changed
- Functions should now more stably sort by call hierarchy order. Added a second pass of sorting to make this logic easier.


## [0.1.0] - 2024-08-02

### Added
- Hacky, but better argument parsing from CLI. Supports --version and --help.


## [0.0.6] - 2024-08-01

### Changed
- Ignore usages of imports when topological sorting
- Allow multiple passes of codemod until stable. This lays out functions in order of usage.


## [0.0.5] - 2024-07-31

### Fixed
- Ignore self-edges; Fixes bug causing top-level nodes to disappear.
- Generically, fixes the bug where nodes were appearing out of order by hardening the concept of a Section.

## [0.0.4] - 2024-07-31

### Fixed
- Functions will correctly be sorted before classes is the function is used in the class scope.


## [0.0.3] - 2024-07-30

### Changed
- Order functions by leafs last.
- Secondarily order nodes by their first access.


## [0.0.2] - 2024-07-30

### Changed
- Robustly handle most top-level nodes in a module body.
- Order should be more deterministic
- Use libcst codemod interface instead of click


## [0.0.1] - 2024-07-29

### Added
- Initial release