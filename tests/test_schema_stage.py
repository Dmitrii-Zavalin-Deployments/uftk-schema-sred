import os
from pathlib import Path
import pytest

import universal_field_toolkit_schema_sred as schema


# ---------------------------------------------------------
# write_schema
# ---------------------------------------------------------

def test_write_schema_creates_file_and_basic_sections(tmp_path, monkeypatch, capsys):
    schema_path = tmp_path / "schema.md"
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(schema_path))

    schema.write_schema()

    assert schema_path.is_file()
    content = schema_path.read_text()

    # Core headings
    assert "# Universal Field Toolkit CSV Schema & Data Standards" in content
    assert "## Column Reference" in content
    assert "## Human Influence Rubric" in content
    assert "## Example Rows" in content
    assert "## Best Practices" in content
    assert "## Optional Future: CSV Validation Mode" in content

    # Confirm generation message
    out = capsys.readouterr().out
    assert "schema.md generated" in out


def test_write_schema_includes_required_columns(tmp_path, monkeypatch):
    schema_path = tmp_path / "schema.md"
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(schema_path))

    schema.write_schema()
    content = schema_path.read_text()

    required_columns = [
        "Observation_ID",
        "Photo_Filename",
        "Observation_Type",
        "Timestamp",
        "Date",
        "Time_Of_Day",
        "Part_Of_Day",
        "GPS",
        "Brightness",
        "Mean_R",
        "Mean_G",
        "Mean_B",
        "Normalized_Blue",
        "Color_Temp_Proxy",
        "Light_Source_Flag",
        "Texture",
        "Relative_Texture_Variance",
        "Texture_Class",
        "Edge_Density",
        "Shadow_Intensity",
        "Shadow_Direction_Variance",
        "Shadow_Variance_Flag",
        "Relative_Brightness_Variance",
        "Human_Influence_Score",
        "Human_Influence_Note",
        "Predicted_Change_Flag",
        "Predicted_Melt_Rate",
        "Explanation",
        "Global_Correlation_Count",
    ]

    for col in required_columns:
        assert col in content


def test_write_schema_includes_multi_domain_examples(tmp_path, monkeypatch):
    schema_path = tmp_path / "schema.md"
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(schema_path))

    schema.write_schema()
    content = schema_path.read_text()

    # Snow example
    assert "photo1_ingested.jpg" in content
    assert "grainy" in content

    # Aurora example
    assert "aurora1_ingested.jpg" in content

    # Air quality example
    assert "sky1_ingested.jpg" in content


def test_write_schema_is_idempotent(tmp_path, monkeypatch):
    """Running write_schema twice should overwrite cleanly without errors."""
    schema_path = tmp_path / "schema.md"
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(schema_path))

    schema.write_schema()
    first = schema_path.read_text()

    schema.write_schema()
    second = schema_path.read_text()

    assert first == second  # deterministic output


# ---------------------------------------------------------
# main()
# ---------------------------------------------------------

def test_main_creates_schema_without_csv(tmp_path, monkeypatch, capsys):
    """Schema stage should NOT require CSV anymore."""
    monkeypatch.setattr(schema, "WORKING_DIR", str(tmp_path))
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(tmp_path / "schema.md"))

    schema.main()

    out = capsys.readouterr().out
    assert "Schema stage complete" in out
    assert "final resting place" in out

    assert (tmp_path / "schema.md").is_file()


def test_main_overwrites_existing_schema(tmp_path, monkeypatch):
    monkeypatch.setattr(schema, "WORKING_DIR", str(tmp_path))
    schema_path = tmp_path / "schema.md"
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(schema_path))

    # Pre-existing file
    schema_path.write_text("OLD CONTENT")

    schema.main()

    new_content = schema_path.read_text()
    assert "OLD CONTENT" not in new_content
    assert "Universal Field Toolkit CSV Schema" in new_content


def test_main_creates_directory_if_missing(tmp_path, monkeypatch):
    """WORKING_DIR may not exist; main() should still succeed."""
    working_dir = tmp_path / "nested" / "deep"
    monkeypatch.setattr(schema, "WORKING_DIR", str(working_dir))
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(working_dir / "schema.md"))

    schema.main()

    assert (working_dir / "schema.md").is_file()



