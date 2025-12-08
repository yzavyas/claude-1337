#!/bin/bash
# atuin shell initialization snippet
# Add this to your ~/.zshrc or ~/.bashrc

# For Zsh
if [[ -n "$ZSH_VERSION" ]]; then
    eval "$(atuin init zsh)"
fi

# For Bash
if [[ -n "$BASH_VERSION" ]]; then
    eval "$(atuin init bash)"
fi

# Optional: atuin configuration
# See: https://github.com/atuinsh/atuin
