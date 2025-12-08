# 🚀 Elite Dev Terminal Setup Guide (2024-2025 Edition)

## 🎯 Quick Command Reference

### 📁 File Navigation & Management
- `ls` → `eza --icons` - List files with icons, Git awareness
- `cat` → `bat` - Syntax highlighted file viewer with Git integration
- `find` → `fd` - Fast, user-friendly find (respects .gitignore)
- `cd` → `z` (zoxide) - Jump to frecent directories instantly
- `yazi` - Blazing fast terminal file manager (Rust, async I/O, image previews)
- `broot` - New way to navigate directory trees

### 🔍 Search & Replace
- `rg <pattern>` - Ripgrep for blazing fast search (parallel, all CPU cores)
- `fzf` - Fuzzy finder for everything
- `sd <find> <replace>` - Intuitive find & replace (better than sed)

### 📊 System Monitoring
- `htop` - Process viewer (run with `sudo htop` for all processes)
- `btop` - Beautiful resource monitor with graphs
- `lazygit` - Terminal UI for git (line-wise staging, interactive rebasing)
- `lazydocker` - Terminal UI for Docker (45k+ stars, one-keypress commands)

### 🎨 Aesthetic & Fun
- `neofetch` - System info with ASCII art
- `figlet <text>` - ASCII art text generator
- `lolcat` - Rainbow colorize any output
- `glow <file.md>` - Beautiful markdown renderer with TUI mode

### 💻 Development Tools
- `tokei` - Count lines of code instantly
- `hyperfine <command>` - Benchmark command execution
- `gitui` - Fast terminal UI for git
- `delta` - Beautiful git diffs (syntax highlighting, themes)
- `gh` - GitHub CLI (issues, PRs, repos)
- `gh-dash` - Rich TUI for GitHub PRs and issues

### 📝 Data & JSON
- `jq` - JSON processor and query tool
- `fx <file.json>` - Interactive JSON explorer
- `jless <file.json>` - JSON viewer with less-like interface

### 🍬 Gum - Interactive Shell Scripts
```bash
# Input prompt
NAME=$(gum input --placeholder "Enter your name")

# Selection menu
CHOICE=$(gum choose "option1" "option2" "option3")

# Styled output
echo "Hello!" | gum style --foreground 212 --border rounded --padding "1 2"

# File picker
FILE=$(gum file .)

# Confirmation
gum confirm "Continue?" && echo "Proceeding..."

# Spinner for long tasks
gum spin --spinner dot --title "Loading..." -- sleep 3
```

---

## 🤖 AI & Agentic Tools (NEW 2024-2025)

### AI-Powered CLI Assistants

#### **aichat** - All-in-One LLM CLI
```bash
# Installation
cargo install aichat

# Usage
aichat "explain this error: ..."
aichat --role shell "find all .log files modified today"

# Features
# - 20+ LLM providers (OpenAI, Claude, Gemini, Ollama, Groq)
# - Shell Assistant mode
# - Chat-REPL with multi-turn conversations
# - Function calling & AI Tools
# - Custom roles via .aichat/config.yaml
```

#### **llm** (by Simon Willison) - CLI LLM Tool
```bash
# Installation
brew install llm
# or: pip install llm

# Usage
llm "summarize this: $(cat README.md)"
cat error.log | llm "explain this error"

# Plugin ecosystem
llm install llm-claude-3
llm install llm-ollama

# Templates
llm templates path  # Store reusable prompts
```

#### **Aider** - AI Pair Programming
```bash
# Installation
brew install aider
# or: pip install aider-chat

# Usage
aider                        # Start session
aider --model claude-opus-4  # Use specific model
aider file1.py file2.py      # Work on specific files

# Features
# - Git integration (commits changes automatically)
# - Line-wise and hunk-based staging
# - Works with existing codebases
# - Project-specific config: .aider.conf.yml
```

#### **Gemini CLI** - Google's Official Agent
```bash
# Installation
npm install -g @google/generative-ai-cli

# Usage
gemini "fix this code"
gemini --file mycode.py "add error handling"

# Features
# - Custom commands
# - MCP server integration
# - GEMINI.md context files (project-specific instructions)
# - Supports Gemini Flash, Pro, Ultra
```

#### **Fabric** - AI Augmentation Framework
```bash
# Installation
go install github.com/danielmiessler/fabric@latest
# or: brew install fabric

# Usage
echo "long article text" | fabric --pattern summarize
cat code.py | fabric --pattern explain_code
fabric --pattern create_video_script "topic: rust programming"

# Features
# - Crowdsourced AI "Patterns" (prompts)
# - Works with GPT, Claude, Ollama
# - Custom patterns directory
# - v1.4.334+ includes Claude Opus 4.5
```

#### **Shell_GPT (sgpt)** - Command Generation
```bash
# Installation
pip install shell-gpt

# Usage
sgpt "find all files larger than 100MB"
sgpt --code "python script to parse JSON"
sgpt --shell "compress all .txt files"

# Config
export OPENAI_API_KEY="your-key"
```

#### **GitHub Copilot CLI**
```bash
# Installation
gh extension install github/gh-copilot

# Usage in terminal
# Uses Claude Sonnet 4.5 by default
# Natural language to shell commands
# Context-aware suggestions
# Use /model command to switch models
```

#### **Warp Terminal AI Agent Mode**
```bash
# Download from warp.dev (macOS, Linux)

# Features
# - AI embedded in terminal
# - Multi-step workflow support
# - Command generation
# - Terminal multiplexing
# - Block-based output (isolates command results)
```

### Multi-Agent Frameworks

#### **LangGraph** - Multi-Agent Workflows
```bash
pip install langgraph

# Features
# - Each agent is a node in a graph
# - Automatic state saving
# - Supports cycles in workflow
# - Control flow managed by edges
```

#### **Google ADK** - Agent Development Kit
```bash
# Download from developers.google.com/adk

# Features
# - Pre-built tools (Search, Code Exec)
# - MCP tools support
# - Agents can use other agents as tools
# - Visual Web UI for testing locally
```

#### **CrewAI** - Multi-Agent Orchestration
```bash
pip install crewai

# Features
# - No-code tools and templates
# - Multi-agent workflows with any LLM
# - Coding from scratch or using templates
```

### MCP (Model Context Protocol) Integration

#### **Terminal Controller MCP**
```bash
# Enables secure terminal command execution through MCP
# - Command execution with timeout controls
# - Directory management
# - Security safeguards against dangerous commands
# - Command history tracking
```

#### **Pre-built MCP Servers**
- Google Drive MCP
- Slack MCP
- GitHub MCP
- Git MCP
- Postgres MCP
- Puppeteer MCP

---

## 🛠️ Installed Languages & Tools

### Languages
- **Java 21** (via SDKMAN) - `java -version`
- **Kotlin** (via SDKMAN) - `kotlin -version`
- **Python 3.12** (via pyenv) - `python --version`
- **Rust** (via rustup) - `rustc --version`
- **Node.js** (via nvm) - `node --version`
- **Bun** - `bun --version`

### Package Managers
- `gradle` - Build tool for JVM projects
- `cargo` - Rust package manager
- `npm` / `pnpm` - Node package managers
- `bun` - All-in-one JavaScript runtime
- `uv` - Fast Python package manager
- `pip` - Python package installer

### Container & Cloud
- `docker` - Container management
- `kind` - Kubernetes in Docker
- `kubectl` - Kubernetes CLI
- `k9s` - Kubernetes TUI (real-time resource tracking, benchmarking)
- `stern` - Multi-pod log tailing

### AI & LLM
- `ollama` - Run LLMs locally
  - Start service: `brew services start ollama`
  - Pull a model: `ollama pull llama2`
  - Run interactive: `ollama run llama2`

---

## ⚡ Shell Enhancements

### Configured Tools
- **Oh My Zsh** - Zsh framework
- **Starship** - Cross-shell prompt (Rust, blazing fast)
- **tmux** - Terminal multiplexer
- **Zellij** - Modern tmux alternative (intuitive, Rust)
- **zoxide** - Smarter cd command (frecency-based)
- **atuin** - Shell history with SQLite (sync across machines)

### Key Aliases
```bash
alias ls="eza --icons"
alias ll="eza -la --icons --git"
alias cat="bat"
alias find="fd"
alias grep="rg"
alias cd="z"
alias lg="lazygit"
alias ld="lazydocker"
alias v="nvim"
alias ya="yazi"
```

### Useful Shell Shortcuts
- `z <partial-path>` - Jump to frecent directory (zoxide)
- `zi` - Interactive directory selection (zoxide + fzf)
- `Ctrl+R` - Fuzzy search command history (atuin/fzf)
- `**<Tab>` - Fuzzy complete files/dirs (fzf)

---

## 🎨 Terminal Aesthetics (2024-2025)

### Recommended Terminal Emulators

#### **Ghostty** (NEW - December 2024)
```bash
brew install ghostty

# Why Elite:
# - Built by Mitchell Hashimoto (HashiCorp founder)
# - Only terminal with Metal renderer + ligatures
# - Zero configuration required
# - Platform-native UI (AppKit on macOS, GTK on Linux)
# - Supports Kitty graphics protocol
```

#### **Alacritty** (Speed Focused)
```bash
brew install alacritty

# Why Elite:
# - Lowest input latency (~50 MB memory)
# - GPU-accelerated
# - Minimalist (delegates tabs/splits to tmux)
```

#### **Kitty** (Feature-Rich)
```bash
brew install kitty

# Why Elite:
# - Custom graphics protocol
# - Powerful "kittens" (extensions)
# - Built-in multiplexing
# - Scriptable via IPC
```

#### **WezTerm** (Programmable)
```bash
brew install wezterm

# Why Elite:
# - Lua-based configuration
# - Custom keybindings trigger complex functions
# - First-class remote workflows
# - Built-in multiplexing
```

### Color Schemes

#### **Catppuccin** (Fastest-Growing 2024)
```bash
# Flavors: Latte, Frappe, Macchiato, Mocha
# Massive port ecosystem (Neovim, terminals, browsers)
# https://github.com/topics/catppuccin
```

#### **Tokyo Night**
```bash
# Celebrates neon aesthetics of Tokyo nights
# 3 dark + 1 light flavor
# Support: Terminal.app, iTerm2, Alacritty, Warp, Ghostty
```

#### **Dracula**
```bash
# 400+ app ports!
# Slightly darker than Catppuccin
# Purple/orange thematic
```

#### **Nord**
```bash
# Arctic, north-bluish clean aesthetic
# Excellent tmux color theme
```

### Nerd Fonts (with Ligatures)

```bash
# Install via Homebrew
brew tap homebrew/cask-fonts

# Top Choices 2024-2025:
brew install --cask font-jetbrains-mono-nerd-font  # Best for developers
brew install --cask font-fira-code-nerd-font       # Most popular ligatures
brew install --cask font-cascadia-code             # Microsoft's modern font

# Why Nerd Fonts:
# - Patches fonts with glyphs/icons (Font Awesome, Devicons, Octicons)
# - Essential for Starship, Powerlevel10k prompts
# - Ligatures: "!=" → ≠, "->" → →, "==" → ≡
```

---

## ⚡ Performance Optimizations

### Shell Startup Time (Target: <200ms)

#### Problem: Slow Version Managers
```bash
# nvm destroys zsh startup: 1.5s → 200ms with lazy loading
# rbenv, jenv also slow
```

#### Solution 1: Lazy Loading
```bash
# Use zsh-nvm plugin for lazy loading
# Or use zsh-defer to defer initialization
```

#### Solution 2: Use Faster Alternatives

**mise** (Recommended 2024-2025)
```bash
brew install mise

# Why Elite:
# - Replaces asdf + direnv + make in one tool
# - Written in Rust (fast)
# - Reads .nvmrc, .tool-versions, .ruby-version
# - Task runner built-in
# - Popular languages included (no plugin step)

# Usage
mise install node@20
mise use node@20
mise exec -- node --version

# Automatically activates per-directory
eval "$(mise activate zsh)"
```

**fnm** (Fast Node Manager)
```bash
brew install fnm

# Almost no effect on shell loading
# Drop-in nvm replacement
```

#### Solution 3: Cache Eval Statements
```bash
# Instead of:
eval "$(brew shellenv)"

# Paste output directly into .zshrc:
export PATH="/opt/homebrew/bin:$PATH"
```

---

## 🎯 ADHD Productivity Tips

### Visual Feedback
- Use `gum` for interactive scripts with visual prompts
- Pipe commands through `lolcat` for rainbow output
- Use `btop` for visual system monitoring
- Use `yazi` for visual file browsing (images, videos, PDFs)

### Quick Information
- `tldr <command>` - Get quick examples instead of man pages
- `tree | head -20` - Visual directory structure
- `tokei` - Instant project statistics

### Context Management
- **atuin** - Never lose command history, search across all machines
- **mise** - Automatic environment switching per directory
- **direnv** - Auto-loads environment variables per project

### Fun Breaks
```bash
# ASCII art banner
figlet "BREAK TIME" | lolcat

# System info with style
neofetch

# Create rainbow directory listing
eza --icons --long --header --git | lolcat
```

---

## 🔧 Terminal Multiplexers

### Tmux Quick Reference
```bash
# Start new session
tmux new -s mysession

# Key bindings (Ctrl+b is prefix)
Ctrl+b %     # Split vertically
Ctrl+b "     # Split horizontally
Ctrl+b arrow # Navigate panes
Ctrl+b c     # New window
Ctrl+b n     # Next window
Ctrl+b d     # Detach session

# Reattach session
tmux attach -t mysession

# Session managers
# - tmuxinator: Ruby-based, YAML configs
# - tmux-sessionx: Modern with fuzzy finding + preview
```

### Zellij (Modern Alternative)
```bash
brew install zellij

# Why Elite:
# - Built in Rust
# - Intuitive keybinding hints (context menu at bottom)
# - Sessions "just work" (auto-creates random named sessions)
# - Alt+HJKL for navigation (faster than tmux prefix)
# - Productive within minutes
# - WebAssembly plugin system

# Usage
zellij          # Start session
zellij attach   # Reattach
zellij ls       # List sessions

# Elite Pattern: Zellij locally, tmux on remote servers
```

---

## 📦 Additional Elite Tools (2024-2025)

### System Utilities
```bash
brew install gping    # Ping with graphs
brew install duf      # Better df alternative
brew install dust     # Better du alternative
brew install procs    # Modern ps replacement
brew install xh       # HTTPie reimplemented in Rust (faster)
```

### TUI Dashboards
```bash
brew install k9s          # Kubernetes TUI (modify resources)
brew install kdash        # Kubernetes TUI (view-only, faster)
gh extension install dlvhdr/gh-dash  # GitHub PRs/issues TUI
```

### Development Environments
```bash
# Devbox - Nix-powered reproducible environments
curl -fsSL https://get.jetify.com/devbox | bash

# Features:
# - Simplifies Nix
# - Generates devcontainers
# - Fast without Docker overhead
# - Use: devbox generate devcontainer
```

### Terminal Recording
```bash
brew install asciinema   # Terminal session recorder (.cast format)
brew install vhs         # Write terminal GIFs as code

# asciinema - text-based, lightweight, copy/paste from recordings
# VHS - programmatic terminal GIFs for demos
```

### TUI Frameworks (For Building Tools)
```bash
# Bubble Tea (Go)
go get github.com/charmbracelet/bubbletea

# Textual (Python)
pip install textual

# Rich (Python)
pip install rich
```

### HTTP & API Testing
```bash
brew install httpie   # Human-friendly HTTP client
brew install xh       # HTTPie in Rust (faster)
brew install hurl     # HTTP requests in plain text
```

### Workflow Automation
```bash
brew install go-task/tap/go-task   # Taskfile (YAML, modern Make)
cargo install just                  # Justfile (simple command runner)
```

---

## 🌟 Pro Tips

### 1. Benchmark and Optimize
```bash
hyperfine 'fd -e txt' 'find . -name "*.txt"'
hyperfine --warmup 3 'your-command'
```

### 2. Chain Tools for Powerful Workflows
```bash
# Find and open files interactively
fd -t f | fzf | xargs bat

# Interactive git branch switching
git branch | fzf | xargs git checkout

# Search code and preview with context
rg --line-number "pattern" | fzf --preview 'bat {1} -H {2}'
```

### 3. Use fzf with bat Preview
```bash
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_DEFAULT_OPTS="--preview 'bat --style=numbers --color=always --line-range :500 {}'"
```

### 4. AI-Powered Workflows
```bash
# Generate commit message from diff
git diff | aichat "write a concise commit message"

# Explain error logs
tail -n 50 error.log | llm "summarize the errors"

# Code review
aider --review file.py

# Interactive debugging
fabric --pattern debug_code < broken_script.py
```

### 5. Leverage `gum` for User-Friendly Scripts
```bash
# Interactive deployment script
ENV=$(gum choose "staging" "production")
gum confirm "Deploy to $ENV?" && ./deploy.sh $ENV

# Progress indicator
gum spin --spinner dot --title "Deploying..." -- ./long-task.sh
```

### 6. Use `jq` for API Responses
```bash
curl -s api.github.com/users/github | jq '.name, .location'

# Pretty print and colorize
curl -s api.example.com/data | jq '.' | bat -l json
```

### 7. Atuin for Enhanced History
```bash
# Search history across all machines
Ctrl+R

# Search history for specific directory
atuin search --cwd /path/to/project

# Stats
atuin stats
```

### 8. mise for Environment Management
```bash
# Define tools in .mise.toml
[tools]
node = "20"
python = "3.12"

# Activate automatically when entering directory
cd project/  # mise automatically switches versions
```

---

## 🚀 One-Command Elite Setup

```bash
#!/bin/bash
# Elite Terminal Setup Script (2024-2025)

# Homebrew essentials
brew install starship zoxide atuin mise
brew install bat eza fd ripgrep git-delta fzf
brew install lazygit lazydocker yazi glow gum
brew install neovim tmux zellij
brew install btop htop tokei hyperfine
brew install jq fx gh
brew install zsh-autosuggestions zsh-syntax-highlighting

# AI & Agentic tools
brew install aider ollama
cargo install aichat
pip install llm shell-gpt
npm install -g @google/generative-ai-cli
go install github.com/danielmiessler/fabric@latest

# Terminal emulators (choose one)
brew install ghostty     # NEW 2024 - Zero config, Metal renderer
# brew install alacritty # Speed focused
# brew install kitty     # Feature-rich
# brew install wezterm   # Programmable

# Fonts
brew tap homebrew/cask-fonts
brew install --cask font-jetbrains-mono-nerd-font
brew install --cask font-fira-code-nerd-font

# Optional: Window management (macOS)
brew install nikitabobko/tap/aerospace  # i3-like tiling

# Optional: Additional utilities
brew install gping duf dust procs xh

echo "✅ Elite terminal setup complete!"
echo "🔧 Next steps:"
echo "   1. Configure Starship: starship preset nerd-font-symbols -o ~/.config/starship.toml"
echo "   2. Add to .zshrc:"
echo "      eval \"\$(starship init zsh)\""
echo "      eval \"\$(zoxide init zsh)\""
echo "      eval \"\$(atuin init zsh)\""
echo "      eval \"\$(mise activate zsh)\""
echo "   3. Reload shell: exec zsh"
```

---

## 📚 Configuration Examples

### ~/.zshrc (Elite 2024-2025)
```bash
# Performance: Lazy load or cache evals

# Shell enhancements
eval "$(starship init zsh)"
eval "$(zoxide init zsh)"
eval "$(atuin init zsh)"
eval "$(mise activate zsh)"

# Plugins (if using Oh My Zsh alternatives)
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# Modern CLI aliases
alias cat='bat'
alias ls='eza --icons'
alias ll='eza -la --icons --git'
alias cd='z'
alias find='fd'
alias grep='rg'

# Git aliases
alias lg='lazygit'
alias gd='git diff | delta'

# Development
alias v='nvim'
alias ld='lazydocker'
alias ya='yazi'

# fzf with bat preview
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_DEFAULT_OPTS="--preview 'bat --style=numbers --color=always --line-range :500 {}'"

# Bind fzf to Ctrl+T for file selection
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

### ~/.config/starship.toml (Minimal)
```toml
# Get preset
# starship preset nerd-font-symbols -o ~/.config/starship.toml

format = """
[┌─](bold green)$directory$git_branch$git_status
[└─>](bold green) """

[directory]
truncation_length = 3
truncate_to_repo = true

[git_branch]
format = "[$symbol$branch]($style) "

[git_status]
format = '([\[$all_status$ahead_behind\]]($style) )'
```

### ~/.tmux.conf (Elite Config)
```bash
# Use C-a as prefix (easier than C-b)
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Vi mode
set-window-option -g mode-keys vi
bind -T copy-mode-vi v send -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel 'xclip -selection clipboard -i'

# Vim-tmux navigator (install plugin)
bind -n C-h select-pane -L
bind -n C-j select-pane -D
bind -n C-k select-pane -U
bind -n C-l select-pane -R

# Better split commands
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# Nord theme (optional)
# set -g @plugin 'arcticicestudio/nord-tmux'

# TPM (Tmux Plugin Manager)
# set -g @plugin 'tmux-plugins/tpm'
# set -g @plugin 'tmux-plugins/tmux-sensible'
# run '~/.tmux/plugins/tpm/tpm'
```

---

## 🏆 What Makes This Setup "Elite" (2024-2025)?

1. **Performance-First**: Sub-200ms shell startup, Rust tools, lazy loading
2. **AI-Integrated**: LLM CLI tools (aichat, llm, aider, fabric)
3. **Modern Aesthetics**: Nerd Fonts, ligatures, Catppuccin/Tokyo Night
4. **Keyboard-Driven**: Vim keybindings, minimal mouse usage
5. **Context-Aware**: atuin, mise, zoxide remember your environment
6. **Multi-Agent Ready**: LangGraph, CrewAI, MCP integration
7. **Automated Setup**: One-command installation, dotfiles in Git
8. **Cross-Platform**: Works on macOS + Linux
9. **Extensible**: Plugin ecosystems, scriptable tools
10. **Production-Ready**: Battle-tested tools + bleeding-edge innovations

---

## 📊 Complexity Rankings

### Low (Start Immediately)
- Ghostty terminal
- Starship prompt
- Modern CLI tools (bat, eza, fd, rg)
- zoxide, fzf, glow, gum

### Medium (Weekend Project)
- Zsh + Oh My Zsh
- Zellij multiplexer
- mise version manager
- AI CLI tools (aichat, llm)
- lazygit, lazydocker, yazi

### High (Ongoing Refinement)
- Neovim custom config
- Tmux with extensive plugins
- WezTerm with Lua programming
- Multi-agent workflows (LangGraph, CrewAI)
- Complex dotfile automation

---

## 🔥 2024-2025 Trends

1. **Rust Dominance**: Most modern CLI tools written in Rust
2. **AI-First Terminals**: Warp, Ghostty, integrated LLM agents
3. **Powerlevel10k → Starship**: P10k deprecated, Starship wins
4. **mise Consolidation**: Replaces asdf + direnv + make
5. **Zellij Rising**: User-friendly tmux alternative
6. **Catppuccin Explosion**: Fastest-growing color scheme
7. **MCP Protocol**: Model Context Protocol for agent integration
8. **Multi-Agent Frameworks**: LangGraph, Google ADK mainstream

---

*Last Updated: 2024-11-30*
*Your terminal is now an AI-augmented, ADHD-optimized productivity powerhouse! 🚀*

---

## 📖 Resources

- [Awesome Dotfiles](https://github.com/webpro/awesome-dotfiles)
- [Awesome ZSH Plugins](https://github.com/unixorn/awesome-zsh-plugins)
- [Nerd Fonts](https://www.nerdfonts.com)
- [Starship](https://starship.rs)
- [Ghostty](https://ghostty.org)
- [mise](https://mise.jdx.dev)
- [Zellij](https://zellij.dev)
- [aichat](https://github.com/sigoden/aichat)
- [LangGraph](https://langchain.com/langgraph)
- [Model Context Protocol](https://modelcontextprotocol.io)
