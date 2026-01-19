"""Storage Port - Interface for result persistence.

Why a Protocol?
--------------
Experiments need different storage strategies:
- Streaming: Append results as they complete (JSONL)
- Batch: Save all at end (JSON)
- Cloud: S3, GCS for large experiments

The domain streams results; adapters decide where they go.

Streaming Design:
- append_result(): Add one result (incremental write)
- stream_results(): Read results one at a time (lazy)
- save_summary(): Write final aggregated summary
"""

from pathlib import Path
from typing import Protocol, Iterator

from lab.domain.models import RunResult, BatchResults, Batch, RunIdentity


class StoragePort(Protocol):
    """Port for experiment result storage.

    The domain needs to:
    1. Append results incrementally (streaming)
    2. Read results back (for resumption)
    3. Save final summary

    Implementations:
    - StreamingFileAdapter: JSONL for results, JSON for summary
    - InMemoryAdapter: For testing
    - S3Adapter: Cloud storage for production
    """

    def append_result(
        self,
        batch_name: str,
        result: RunResult,
    ) -> None:
        """Append a single result to storage.

        Called after each run completes. Must be durable
        (flush to disk/cloud immediately).

        This is the key streaming method - results are written
        incrementally, not held in memory.
        """
        ...

    def stream_results(
        self,
        batch_name: str,
    ) -> Iterator[RunResult]:
        """Stream results from storage.

        Yields results one at a time (lazy loading).
        Used for:
        - Resumption (find completed runs)
        - Analysis (process without loading all)
        """
        ...

    def get_completed_runs(
        self,
        batch_name: str,
    ) -> set[RunIdentity]:
        """Get identities of completed runs.

        Used for resumption - skip runs that already completed.
        """
        ...

    def save_summary(
        self,
        batch_name: str,
        summary: BatchResults,
    ) -> Path:
        """Save final summary after all runs complete.

        Unlike append_result, this overwrites (final aggregation).
        Returns the path where summary was saved.
        """
        ...

    def load_batch(
        self,
        batch_path: Path,
    ) -> Batch:
        """Load a batch configuration from storage.

        Loads YAML config and referenced conditions/tasks.
        """
        ...

    def batch_exists(
        self,
        batch_name: str,
    ) -> bool:
        """Check if results exist for a batch.

        Used to warn about overwriting or offer resumption.
        """
        ...
