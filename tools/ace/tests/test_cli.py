"""Tests for CLI."""

from click.testing import CliRunner

from ace.adapters.in_.cli import main


class TestCLI:
    """Tests for ace CLI."""

    def test_help(self):
        """CLI shows help."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "ace" in result.output
        assert "extensions" in result.output

    def test_version(self):
        """CLI shows version."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0

    def test_info(self):
        """CLI info command works."""
        runner = CliRunner()
        result = runner.invoke(main, ["info"])

        assert result.exit_code == 0
        assert "ace" in result.output
        assert "Config:" in result.output

    def test_source_list(self):
        """CLI can list sources."""
        runner = CliRunner()
        result = runner.invoke(main, ["source", "list"])

        # Should work even with no sources (shows guidance)
        assert result.exit_code == 0

    def test_list_installed(self):
        """CLI can list installed packages."""
        runner = CliRunner()
        result = runner.invoke(main, ["list"])

        assert result.exit_code == 0

    def test_source_subcommand_help(self):
        """Source subcommand shows help."""
        runner = CliRunner()
        result = runner.invoke(main, ["source", "--help"])

        assert result.exit_code == 0
        assert "add" in result.output
        assert "list" in result.output
        assert "rm" in result.output
