# ace

**Agentic Capability Extensions** — CLI for managing extensions that enhance what AI agents can do.

Part of [claude-1337](../README.md).

## What It Does

Discover, install, and manage capability extensions for AI coding assistants.

Extensions include:
- **Skills** — knowledge and decision frameworks (cognitive)
- **Agents** — specialized subagents for delegation
- **Hooks** — event-triggered behaviors
- **MCPs** — external system integrations
- **Tools/CLIs** — operational capabilities

## Install

```bash
uv tool install "ace @ git+https://github.com/yzavyas/claude-1337#subdirectory=ace"
```

## Usage

```bash
# Add a source (marketplace)
ace source add https://github.com/yzavyas/claude-1337

# List available packages
ace list --available

# Install a package
ace install core-1337

# Show package details
ace show core-1337

# Update all packages
ace update
```

## Architecture

Hexagonal architecture with clear separation:

```
ace/src/ace/
├── domain/         # Core models (Source, Package, Extension)
├── ports/          # Interfaces (Repository, Registry, Target)
├── adapters/       # Implementations
│   ├── in_/        # CLI (driving adapter)
│   └── out/        # Git, filesystem, claude-code (driven adapters)
└── application/    # Use cases
```

## Status

Core functionality implemented:
- [x] Source management (add, remove, list, refresh)
- [x] Package discovery and installation
- [x] Claude Code target adapter
- [x] Git repository adapter
- [ ] Plugin README metadata parsing
- [ ] Version pinning and updates
- [ ] Multiple target support
