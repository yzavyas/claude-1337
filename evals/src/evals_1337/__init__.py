"""evals-1337: Extension evaluation framework for claude-1337 marketplace.

Evaluates all extension types:
- Skills: Activation (F1) + Behavioral (methodology adherence)
- Agents: Task completion, tool correctness
- MCP Servers: MCPGauge (proactivity, compliance, effectiveness, overhead)
- Commands: Execution accuracy, output quality
- Hooks: Trigger accuracy, side effects

Usage:
    evals-1337 skills plugins/rust-1337
    evals-1337 skills plugins/core-1337 --behavioral
"""

__version__ = "0.2.0"
