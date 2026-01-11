"""
Reference Documentation Validator

Validates that our extension-builder references document ALL fields
defined in the official schemas.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .schemas import SCHEMAS, get_schema_fields


@dataclass
class ValidationResult:
    """Result of validating a reference document."""

    reference_file: str
    schema_name: str
    documented_fields: set[str] = field(default_factory=set)
    missing_fields: set[str] = field(default_factory=set)
    extra_fields: set[str] = field(default_factory=set)
    coverage_percent: float = 0.0
    passed: bool = False

    def __str__(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        lines = [
            f"{status} {self.reference_file} ({self.schema_name})",
            f"  Coverage: {self.coverage_percent:.1f}%",
        ]
        if self.missing_fields:
            lines.append(f"  Missing: {', '.join(sorted(self.missing_fields))}")
        if self.extra_fields:
            lines.append(f"  Extra (not in schema): {', '.join(sorted(self.extra_fields))}")
        return "\n".join(lines)


def extract_documented_fields(content: str) -> set[str]:
    """
    Extract field names documented in a markdown reference.

    Looks for:
    - Table rows with field names: | `field_name` | ...
    - YAML/code examples: field_name: value
    - Inline code references: `field_name`
    """
    fields = set()

    # Pattern 1: Table rows with backtick fields
    # | `field-name` | ... or | `field_name` | ...
    table_pattern = r"\|\s*`([a-z][a-z0-9_-]*)`\s*\|"
    for match in re.finditer(table_pattern, content, re.IGNORECASE):
        fields.add(match.group(1))

    # Pattern 2: YAML frontmatter/code examples
    # field-name: value or field_name: value
    yaml_pattern = r"^[ ]*([a-z][a-z0-9_-]*):\s*"
    for match in re.finditer(yaml_pattern, content, re.MULTILINE | re.IGNORECASE):
        field_name = match.group(1)
        # Skip common non-field YAML keys
        if field_name not in {"type", "example", "context", "user", "assistant"}:
            fields.add(field_name)

    # Pattern 3: Section headers that are field names
    # ### field_name or ### field-name
    header_pattern = r"^###\s+([a-z][a-z0-9_-]*)\s*$"
    for match in re.finditer(header_pattern, content, re.MULTILINE | re.IGNORECASE):
        fields.add(match.group(1))

    return fields


def validate_reference(
    reference_path: Path,
    schema_name: str,
    min_coverage: float = 90.0,
) -> ValidationResult:
    """
    Validate a reference document against its schema.

    Args:
        reference_path: Path to the markdown reference file
        schema_name: Name of schema to validate against
        min_coverage: Minimum coverage percentage to pass (default 90%)

    Returns:
        ValidationResult with details
    """
    if schema_name not in SCHEMAS:
        raise ValueError(f"Unknown schema: {schema_name}")

    content = reference_path.read_text()
    schema_fields = get_schema_fields(schema_name)
    documented_fields = extract_documented_fields(content)

    # Normalize field names (handle both underscore and hyphen)
    def normalize(f: str) -> str:
        return f.replace("-", "_").lower()

    schema_normalized = {normalize(f): f for f in schema_fields}
    documented_normalized = {normalize(f): f for f in documented_fields}

    # Find matches
    matched = set()
    for norm, original in documented_normalized.items():
        if norm in schema_normalized:
            matched.add(schema_normalized[norm])

    missing = schema_fields - matched
    extra = documented_fields - {schema_normalized.get(normalize(f), f) for f in documented_fields if normalize(f) in schema_normalized}

    coverage = (len(matched) / len(schema_fields) * 100) if schema_fields else 100.0

    return ValidationResult(
        reference_file=str(reference_path.name),
        schema_name=schema_name,
        documented_fields=matched,
        missing_fields=missing,
        extra_fields=extra - matched,
        coverage_percent=coverage,
        passed=coverage >= min_coverage,
    )


def validate_all_references(
    references_dir: Path,
    min_coverage: float = 90.0,
) -> list[ValidationResult]:
    """
    Validate all reference documents in a directory.

    Args:
        references_dir: Path to references directory
        min_coverage: Minimum coverage to pass

    Returns:
        List of validation results
    """
    # Map reference files to their schemas
    schema_mapping = {
        "skills.md": "skill",
        "commands.md": "command",
        "agents.md": "agent",
        "plugin-schema.md": "plugin",
        "hooks.md": "hooks",
        "mcp.md": "mcp",
        "marketplace-schema.md": "marketplace",
    }

    results = []
    for filename, schema_name in schema_mapping.items():
        ref_path = references_dir / filename
        if ref_path.exists():
            result = validate_reference(ref_path, schema_name, min_coverage)
            results.append(result)
        else:
            # Missing file is a failure
            results.append(
                ValidationResult(
                    reference_file=filename,
                    schema_name=schema_name,
                    passed=False,
                    missing_fields=get_schema_fields(schema_name),
                )
            )

    return results


def print_validation_report(results: list[ValidationResult]) -> bool:
    """
    Print validation report and return overall pass/fail.

    Returns:
        True if all validations passed
    """
    print("=" * 60)
    print("Extension Builder Reference Validation Report")
    print("=" * 60)
    print()

    all_passed = True
    total_missing = set()

    for result in results:
        print(result)
        print()
        if not result.passed:
            all_passed = False
        total_missing.update(result.missing_fields)

    print("-" * 60)
    if all_passed:
        print("✅ All references pass schema validation!")
    else:
        print(f"❌ {sum(1 for r in results if not r.passed)}/{len(results)} references need updates")
        if total_missing:
            print(f"\nTotal missing fields across all refs: {len(total_missing)}")

    return all_passed


if __name__ == "__main__":
    import sys

    # Find references directory
    script_dir = Path(__file__).parent
    refs_dir = script_dir.parent / "references"

    if not refs_dir.exists():
        print(f"References directory not found: {refs_dir}")
        sys.exit(1)

    results = validate_all_references(refs_dir, min_coverage=80.0)
    passed = print_validation_report(results)

    sys.exit(0 if passed else 1)
