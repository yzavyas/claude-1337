"""Dependency Injection Container.

Wires up all adapters and use cases. The CLI and tests use this
to get fully-configured instances without knowing the wiring.

Usage:
    container = Container.create()
    use_case = container.run_experiment_use_case()
    async for result in use_case.execute(input):
        print(result)

    # Or with custom configuration:
    container = Container.create(
        tracer="console",  # "phoenix", "console", or "noop"
        grader="mock",     # "mock" for now
    )
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from lab.adapters.driven.claude_sdk import ClaudeSDKAdapter
from lab.adapters.driven.phoenix import PhoenixTracerAdapter
from lab.adapters.driven.console_tracer import ConsoleTracerAdapter, NoOpTracerAdapter
from lab.adapters.driven.filesystem import StreamingFileAdapter
from lab.adapters.driven.mock_grader import MockGraderAdapter
from lab.adapters.driven.swebench_grader import SWEBenchGraderAdapter
from lab.adapters.driven.swebench_docker_grader import SWEBenchDockerGraderAdapter
from lab.adapters.driven.function_grader import FunctionGraderAdapter

from lab.ports.driven.llm import LLMPort
from lab.ports.driven.grader import GraderPort
from lab.ports.driven.tracer import TracerPort
from lab.ports.driven.storage import StoragePort

from lab.ports.driving.use_cases import (
    RunExperimentUseCase,
    LoadBatchUseCase,
)


TracerType = Literal["phoenix", "console", "noop"]
GraderType = Literal["mock", "swebench", "swebench-docker", "function"]


class ContainerConfig(BaseModel):
    """Configuration for the container."""
    model_config = ConfigDict(frozen=True)

    # Tracer configuration
    tracer: TracerType = "console"
    phoenix_endpoint: str = "http://localhost:6006/v1/traces"
    verbose_tracing: bool = True

    # Storage configuration
    results_dir: Path = Path("results")

    # Grader configuration
    grader: GraderType = "mock"
    mock_pass_rate: float = 0.5  # For mock grader
    swebench_workspace: Path | None = None  # For swebench grader
    swebench_timeout: int = 300  # 5 min default

    # LLM configuration
    working_dir: Path | None = None


class Container:
    """Dependency injection container.

    Creates and wires up all adapters and use cases.
    Manages lifecycle of stateful components.
    """

    def __init__(self, config: ContainerConfig):
        """Initialize with configuration.

        Use Container.create() for convenience.
        """
        self.config = config

        # Lazy-initialized adapters
        self._llm: LLMPort | None = None
        self._grader: GraderPort | None = None
        self._tracer: TracerPort | None = None
        self._storage: StoragePort | None = None

    @classmethod
    def create(
        cls,
        tracer: TracerType = "console",
        grader: GraderType = "mock",
        results_dir: Path | None = None,
        working_dir: Path | None = None,
        verbose: bool = True,
        mock_pass_rate: float = 0.5,
        swebench_workspace: Path | None = None,
        swebench_timeout: int = 300,
    ) -> "Container":
        """Create a container with sensible defaults.

        Args:
            tracer: Which tracer to use (phoenix, console, noop)
            grader: Which grader to use (mock, swebench)
            results_dir: Where to store results
            working_dir: Working directory for agent
            verbose: Verbose tracing output
            mock_pass_rate: Pass rate for mock grader
            swebench_workspace: Workspace for swebench grader
            swebench_timeout: Timeout for swebench grader

        Returns:
            Configured Container instance
        """
        config = ContainerConfig(
            tracer=tracer,
            results_dir=results_dir or Path("results"),
            working_dir=working_dir,
            verbose_tracing=verbose,
            grader=grader,
            mock_pass_rate=mock_pass_rate,
            swebench_workspace=swebench_workspace,
            swebench_timeout=swebench_timeout,
        )
        return cls(config)

    # --- Adapter Factories ---

    def llm(self) -> LLMPort:
        """Get or create the LLM adapter."""
        if self._llm is None:
            self._llm = ClaudeSDKAdapter(
                working_dir=self.config.working_dir,
            )
        return self._llm

    def grader(self) -> GraderPort:
        """Get or create the grader adapter."""
        if self._grader is None:
            if self.config.grader == "mock":
                self._grader = MockGraderAdapter(
                    strategy="random",
                    pass_rate=self.config.mock_pass_rate,
                )
            elif self.config.grader == "swebench":
                self._grader = SWEBenchGraderAdapter(
                    workspace_dir=self.config.swebench_workspace,
                    timeout=self.config.swebench_timeout,
                )
            elif self.config.grader == "swebench-docker":
                self._grader = SWEBenchDockerGraderAdapter(
                    workspace_dir=self.config.swebench_workspace,
                    timeout=self.config.swebench_timeout,
                )
            elif self.config.grader == "function":
                self._grader = FunctionGraderAdapter(
                    timeout=30,
                    keep_workspace=True,  # Keep for debugging
                )
            else:
                raise ValueError(f"Unknown grader type: {self.config.grader}")
        return self._grader

    def tracer(self) -> TracerPort:
        """Get or create the tracer adapter."""
        if self._tracer is None:
            if self.config.tracer == "phoenix":
                self._tracer = PhoenixTracerAdapter(
                    endpoint=self.config.phoenix_endpoint,
                )
            elif self.config.tracer == "console":
                self._tracer = ConsoleTracerAdapter(
                    verbose=self.config.verbose_tracing,
                )
            elif self.config.tracer == "noop":
                self._tracer = NoOpTracerAdapter()
            else:
                raise ValueError(f"Unknown tracer type: {self.config.tracer}")
        return self._tracer

    def storage(self) -> StoragePort:
        """Get or create the storage adapter."""
        if self._storage is None:
            self._storage = StreamingFileAdapter(
                results_dir=self.config.results_dir,
            )
        return self._storage

    # --- Use Case Factories ---

    def run_experiment_use_case(self) -> RunExperimentUseCase:
        """Create the RunExperiment use case with all dependencies."""
        return RunExperimentUseCase(
            llm=self.llm(),
            grader=self.grader(),
            tracer=self.tracer(),
            storage=self.storage(),
        )

    def load_batch_use_case(self) -> LoadBatchUseCase:
        """Create the LoadBatch use case."""
        return LoadBatchUseCase(storage=self.storage())


# --- Convenience functions for CLI ---


def get_container(**kwargs) -> Container:
    """Get a configured container.

    Convenience function for CLI usage.
    """
    return Container.create(**kwargs)


def run_experiment(
    batch_path: Path,
    resume: bool = False,
    tracer: TracerType = "console",
    **kwargs,
) -> RunExperimentUseCase:
    """Get a configured RunExperimentUseCase.

    Convenience function for running experiments.
    """
    container = Container.create(tracer=tracer, **kwargs)
    return container.run_experiment_use_case()
