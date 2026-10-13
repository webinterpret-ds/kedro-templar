from pathlib import Path

from click.testing import CliRunner

from kedro_templar.plugin import commands

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def run_apply(output_dir: Path, *extra_args: str):
    return CliRunner().invoke(
        commands,
        [
            "templar",
            "apply",
            "-c",
            str(EXAMPLES_DIR / "definition.yaml"),
            "-t",
            str(EXAMPLES_DIR),
            "-o",
            str(output_dir),
            *extra_args,
        ],
        catch_exceptions=False,
    )


def test_apply_renders_templates(tmp_path):
    result = run_apply(tmp_path)

    assert result.exit_code == 0, result.output
    catalog = (tmp_path / "base" / "catalog.yml").read_text()
    parameters = (tmp_path / "base" / "parameters.yml").read_text()
    assert "s3://your_bucket/run_1/subfolder/data/sample_data.csv" in catalog
    assert "start_date: 2030-04-04" in parameters
    assert "end_date: 2040-04-06" in parameters


def test_apply_does_not_overwrite_without_force(tmp_path):
    existing = tmp_path / "base" / "catalog.yml"
    existing.parent.mkdir()
    existing.write_text("existing")

    result = run_apply(tmp_path)

    assert result.exit_code == 0, result.output
    assert existing.read_text() == "existing"


def test_apply_overwrites_with_force(tmp_path):
    existing = tmp_path / "base" / "catalog.yml"
    existing.parent.mkdir()
    existing.write_text("existing")

    result = run_apply(tmp_path, "-f")

    assert result.exit_code == 0, result.output
    assert "s3://your_bucket/run_1/subfolder/data/sample_data.csv" in existing.read_text()
