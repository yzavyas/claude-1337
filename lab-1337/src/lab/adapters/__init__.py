"""Lab-1337 Adapters Layer.

Adapters implement the port interfaces with concrete technology.
They're the "how" to the domain's "what".

Driven adapters (secondary):
- claude_sdk: LLMPort implementation using Claude Agent SDK
- mock_grader: GraderPort implementation for testing
- swebench_grader: GraderPort implementation for SWE-bench tasks
- phoenix: TracerPort implementation using Phoenix/OTel
- console_tracer: TracerPort implementation for console output
- filesystem: StoragePort implementation using JSONL files

Driving adapters (primary):
- cli: Thin wrapper connecting Click CLI to use cases
"""

from .driven.claude_sdk import ClaudeSDKAdapter
from .driven.phoenix import PhoenixTracerAdapter
from .driven.console_tracer import ConsoleTracerAdapter, NoOpTracerAdapter
from .driven.filesystem import StreamingFileAdapter
from .driven.mock_grader import MockGraderAdapter
from .driven.swebench_grader import SWEBenchGraderAdapter

__all__ = [
    "ClaudeSDKAdapter",
    "PhoenixTracerAdapter",
    "ConsoleTracerAdapter",
    "NoOpTracerAdapter",
    "StreamingFileAdapter",
    "MockGraderAdapter",
    "SWEBenchGraderAdapter",
]
