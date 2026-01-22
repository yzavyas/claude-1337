"""Lab-1337 Adapters Layer.

Adapters implement the port interfaces with concrete technology.
They're the "how" to the domain's "what".

Driven adapters (secondary):
- claude_sdk: LLMPort implementation using Claude Agent SDK
- mock_grader: GraderPort implementation for testing
- function_grader: GraderPort implementation for custom function graders
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
from .driven.function_grader import FunctionGraderAdapter

__all__ = [
    "ClaudeSDKAdapter",
    "PhoenixTracerAdapter",
    "ConsoleTracerAdapter",
    "NoOpTracerAdapter",
    "StreamingFileAdapter",
    "MockGraderAdapter",
    "FunctionGraderAdapter",
]
