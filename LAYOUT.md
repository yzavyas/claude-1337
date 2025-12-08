# Project Layout

Visual reference for the claude-1337 marketplace structure.

## Repository Structure

```
claude-1337/
│
├── .claude-plugin/
│   └── marketplace.json              # Marketplace definition
│
├── plugins/                          # Plugin container directory
│   └── terminal-1337/                # terminal-1337 plugin
│       ├── commands/                 # Slash commands (future)
│       ├── agents/                   # Specialized agents (future)
│       ├── hooks/                    # Event hooks (future)
│       └── skills/                   # Skills bundled with plugin
│           ├── SKILL.md              # Main skill instructions (8.2kb)
│           ├── references/           # Comprehensive tool docs
│           │   ├── atuin.md          # Shell history (3.3kb)
│           │   ├── bat.md            # File viewer (5.0kb)
│           │   ├── eza.md            # Directory listing (6.1kb)
│           │   ├── fd.md             # File finder (4.3kb)
│           │   ├── fzf.md            # Fuzzy finder (5.8kb)
│           │   ├── jq.md             # JSON processor (5.0kb)
│           │   ├── ripgrep.md        # Code search (5.4kb)
│           │   └── xh.md             # HTTP client (4.1kb)
│           ├── scripts/              # Install scripts (all executable)
│           │   ├── install-atuin.sh
│           │   ├── install-bat.sh
│           │   ├── install-eza.sh
│           │   ├── install-fd.sh
│           │   ├── install-fzf.sh
│           │   ├── install-jq.sh
│           │   ├── install-ripgrep.sh
│           │   └── install-xh.sh
│           └── assets/               # Config snippets
│               └── configs/
│                   └── atuin-init.sh
│
├── docs/                             # Project documentation
│   ├── TERMINAL_SETUP.md             # Comprehensive terminal guide
│   └── terminal-1337.md              # Skill documentation
│
├── scripts/                          # Repository-level scripts
│   └── install-terminal-tools.sh     # Bulk installer
│
├── CLAUDE.md                         # Project steward (for Claude instances)
├── CONTRIBUTING.md                   # Contribution guidelines
├── LAYOUT.md                         # This file
├── LICENSE                           # MIT license
└── README.md                         # Main documentation
```

## Path Resolution

### Marketplace Discovery
```
User adds: https://github.com/yzavyas/claude-1337
           ↓
Claude reads: .claude-plugin/marketplace.json
```

### Plugin Loading
```
marketplace.json → "source": "./plugins/terminal-1337"
                   ↓
Plugin root: plugins/terminal-1337/
```

### Skill Discovery
```
marketplace.json → "skills": ["./skills"]
                   ↓
Relative to plugin source: plugins/terminal-1337/skills/
                   ↓
Loads: plugins/terminal-1337/skills/SKILL.md
```

### Progressive Disclosure
```
1. Metadata (always loaded)
   └─ name, description, keywords, category

2. SKILL.md (loaded when triggered)
   └─ Activation logic, tool detection, behavior

3. References (loaded on-demand)
   └─ Comprehensive tool documentation

4. Scripts (executed on-demand)
   └─ Installation and setup automation

5. Assets (loaded on-demand)
   └─ Configuration snippets for user setup
```

## File Types

### Configuration
- `marketplace.json` - Marketplace and plugin metadata
- `SKILL.md` - Skill instructions with YAML frontmatter

### Documentation
- `*.md` (docs/) - User-facing documentation
- `*.md` (references/) - Tool reference documentation
- `CLAUDE.md` - Project steward for Claude instances
- `CONTRIBUTING.md` - Contributor guidelines
- `LAYOUT.md` - This structure reference

### Scripts
- `install-*.sh` - Tool installation scripts (executable)
- `*.sh` (assets/) - Configuration snippets

## Size Overview

```
Total: ~60KB of carefully curated content

SKILL.md:          8.2 KB   Core skill logic
References:       39.0 KB   8 comprehensive tool guides
Scripts:           8.0 KB   8 install scripts
Assets:            1.5 KB   Config snippets
Docs:             15.0 KB   User documentation
```

## Empty Directories (Future Expansion)

```
plugins/terminal-1337/commands/   # Slash commands
plugins/terminal-1337/agents/     # Specialized agents
plugins/terminal-1337/hooks/      # Event hooks
```

These exist to show future capability and maintain clean structure.

## Key Conventions

### Naming
- Files: `kebab-case.md`, `kebab-case.sh`
- Directories: `kebab-case/`
- Plugin names: `kebab-case` (terminal-1337)
- Skill names: `kebab-case` (same as plugin for single-skill plugins)

### Permissions
- All `.sh` scripts: `755` (executable)
- All `.md` files: `644` (readable)
- All directories: `755` (accessible)

### References
- Each tool gets one comprehensive markdown file
- 200-400 lines per reference
- Includes: overview, installation, usage, options, config, tips, gotchas

### Scripts
- OS detection (macOS/Linux)
- Package manager detection (brew/apt/dnf)
- Error handling (`set -e`)
- Verification after installation
- Clear success messages

## Expansion Pattern

Adding a new plugin:

```
1. Create directory structure:
   plugins/new-plugin/
   ├── commands/
   ├── agents/
   ├── hooks/
   └── skills/
       └── skill-name/
           └── SKILL.md

2. Update marketplace.json:
   Add new plugin entry with metadata

3. Add documentation:
   docs/new-plugin.md

4. Test and commit
```

## Related Documentation

- **CLAUDE.md** - Architecture, patterns, development workflow
- **CONTRIBUTING.md** - How to contribute
- **README.md** - User-facing documentation
- **docs/terminal-1337.md** - terminal-1337 skill details
