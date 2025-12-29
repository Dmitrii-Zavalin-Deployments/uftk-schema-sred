import os
import shutil
from pathlib import Path
import pytest

import universal_field_toolkit_schema_sred as schema


# ---------------------------------------------------------
# write_schema
# ---------------------------------------------------------

def test_write_schema_creates_correct_file(tmp_path, monkeypatch, capsys):
    # Patch SCHEMA_PATH
    schema_path = tmp_path / "schema.md"
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(schema_path))

    schema.write_schema()

    assert schema_path.is_file()

    content = schema_path.read_text()

    # Basic structure
    assert "# Universal Field Toolkit Schema" in content
    assert "## Required Columns" in content

    # Required fields
    required_fields = [
        "Observation_ID",
        "Photo_Filename",
        "Observation_Type",
        "Timestamp",
        "Date",
        "Time_Of_Day",
        "GPS",
        "Human_Influence_Score",
        "Human_Influence_Note",
        "Notes",
        "brightness",
        "Mean_R",
        "Mean_G",
        "Mean_B",
        "Texture",
        "Texture_Class",
        "Edge_Density",
        "Shadow_Intensity",
        "Predicted_Melt_Rate",
        "Explanation",
        "Global_Correlation_Count",
    ]

    for field in required_fields:
        assert f"- {field}" in content

    captured = capsys.readouterr()
    assert "schema.md generated" in captured.out


# ---------------------------------------------------------
# generate_final_images
# ---------------------------------------------------------

def test_generate_final_images_copies_predicted_files(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(schema, "WORKING_DIR", str(tmp_path))

    # Create predicted images
    pred1 = tmp_path / "img1_predicted.jpg"
    pred2 = tmp_path / "img2_predicted.jpg"
    pred1.write_bytes(b"jpeg1")
    pred2.write_bytes(b"jpeg2")

    # Create unrelated files
    (tmp_path / "notes.txt").write_text("ignore me")
    (tmp_path / "img3_analyzed.jpg").write_bytes(b"nope")

    schema.generate_final_images()

    # Check final images
    final1 = tmp_path / "img1_final.jpg"
    final2 = tmp_path / "img2_final.jpg"

    assert final1.is_file()
    assert final2.is_file()

    assert final1.read_bytes() == b"jpeg1"
    assert final2.read_bytes() == b"jpeg2"

    captured = capsys.readouterr()
    assert "Created" in captured.out


def test_generate_final_images_no_predicted_files(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(schema, "WORKING_DIR", str(tmp_path))

    # Only non-predicted files
    (tmp_path / "random.jpg").write_bytes(b"data")

    schema.generate_final_images()

    captured = capsys.readouterr()
    # Should not print any "Created"
    assert "Created" not in captured.out


# ---------------------------------------------------------
# main() — missing CSV
# ---------------------------------------------------------

def test_main_missing_csv(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(schema, "WORKING_DIR", str(tmp_path))
    monkeypatch.setattr(schema, "CSV_PATH", str(tmp_path / "field_data.csv"))
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(tmp_path / "schema.md"))

    schema.main()

    captured = capsys.readouterr()
    assert "field_data.csv not found" in captured.out

    # No schema.md created
    assert not (tmp_path / "schema.md").exists()


# ---------------------------------------------------------
# main() — happy path
# ---------------------------------------------------------

def test_main_happy_path(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(schema, "WORKING_DIR", str(tmp_path))
    csv_path = tmp_path / "field_data.csv"
    schema_path = tmp_path / "schema.md"

    monkeypatch.setattr(schema, "CSV_PATH", str(csv_path))
    monkeypatch.setattr(schema, "SCHEMA_PATH", str(schema_path))

    # Create CSV so main() proceeds
    csv_path.write_text("dummy,data\n")

    # Create predicted images
    pred = tmp_path / "img_predicted.jpg"
    pred.write_bytes(b"jpegdata")

    schema.main()

    captured = capsys.readouterr()

    # Schema created
    assert schema_path.is_file()
    assert "schema.md generated" in captured.out

    # Final image created
    final = tmp_path / "img_final.jpg"
    assert final.is_file()
    assert final.read_bytes() == b"jpegdata"

    # Final messages
    assert "Schema stage complete" in captured.out
    assert "final resting place" in captured.out



