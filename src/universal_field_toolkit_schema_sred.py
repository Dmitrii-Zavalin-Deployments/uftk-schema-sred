import os

# ---------------------------------------------------------
# Unified working directory
# ---------------------------------------------------------
WORKING_DIR = "/data/testing-input-output"
SCHEMA_PATH = os.path.join(WORKING_DIR, "schema.md")
os.makedirs(WORKING_DIR, exist_ok=True)

# ---------------------------------------------------------
# Generate rich schema.md (Book 7 content)
# ---------------------------------------------------------
def write_schema():
    with open(SCHEMA_PATH, "w") as f:
        f.write("# Universal Field Toolkit CSV Schema & Data Standards\n\n")
        f.write("This document defines the complete data contract for the Universal Field Toolkit.\n")
        f.write("It is the single source of truth for all pipeline stages.\n\n")

        # ---------------------------------------------------------
        # Column Reference Table
        # ---------------------------------------------------------
        f.write("## Column Reference\n\n")
        f.write("| Column Name | Type | Description | Example |\n")
        f.write("|-------------|------|-------------|---------|\n")
        f.write("| Observation_ID | str | Unique identifier for each observation | OBS-20251230-001 |\n")
        f.write("| Photo_Filename | str | Filename of the processed photo | photo1_ingested.jpg |\n")
        f.write("| Observation_Type | str | 'photo' or 'manual' | photo |\n")
        f.write("| Timestamp | str | ISO or EXIF timestamp | 2025-12-30 14:30:00 |\n")
        f.write("| Date | str | Date extracted from timestamp | 2025-12-30 |\n")
        f.write("| Time_Of_Day | str | Time extracted from timestamp | 14:30:00 |\n")
        f.write("| Part_Of_Day | str | Morning / Afternoon / Evening / Night | afternoon |\n")
        f.write("| GPS | str | Raw GPSInfo or coordinates | (63.123, -135.456) |\n")
        f.write("| Brightness | float | Mean grayscale value — proxy for albedo | 185.2 |\n")
        f.write("| Mean_R / Mean_G / Mean_B | float | Channel means — color balance | 190.1 / 185.3 / 180.5 |\n")
        f.write("| Normalized_Blue | float | mean_B / total — ice/water proxy | 0.34 |\n")
        f.write("| Color_Temp_Proxy | float | 1000 × (mean_R / mean_B) — light source warmth | 4200 |\n")
        f.write("| Light_Source_Flag | str | 'natural' or 'artificial' | artificial |\n")
        f.write("| Texture | float | Laplacian variance — surface roughness | 7324.29 |\n")
        f.write("| Relative_Texture_Variance | float | Quadrant-normalized texture | 0.92 |\n")
        f.write("| Texture_Class | str | smooth / grainy (expandable) | grainy |\n")
        f.write("| Edge_Density | float | Canny edge count — crust/melt features | 3092272.0 |\n")
        f.write("| Shadow_Intensity | float | Dark pixel ratio — sun angle proxy | 0.20 |\n")
        f.write("| Shadow_Direction_Variance | float | Sobel gradient variance | 1450.3 |\n")
        f.write("| Shadow_Variance_Flag | str | natural / artificial | artificial |\n")
        f.write("| Relative_Brightness_Variance | float | Uneven illumination metric | 0.15 |\n")
        f.write("| Human_Influence_Score | int | 1–10 scale (see rubric) | 8 |\n")
        f.write("| Human_Influence_Note | str | Free-text human impact description | near road, truck soot |\n")
        f.write("| Predicted_Change_Flag | int | 1 = change likely, 0 = stable | 1 |\n")
        f.write("| Predicted_Melt_Rate | str/float | fast / moderate / slow / regression value | fast |\n")
        f.write("| Explanation | str | Rule-based or regression reasoning | Predicted Fast Melt BECAUSE... |\n")
        f.write("| Global_Correlation_Count | int | Number of features used in correlation | 12 |\n\n")

        # ---------------------------------------------------------
        # Human Influence Rubric
        # ---------------------------------------------------------
        f.write("## Human Influence Rubric (1–10)\n\n")
        f.write("- **1–3**: Minimal — pristine snow, no visible human activity\n")
        f.write("- **4–6**: Moderate — nearby roads/structures but no direct contact\n")
        f.write("- **7–10**: Strong — soot, exhaust, footprints, traffic, machinery\n\n")

        # ---------------------------------------------------------
        # Example Rows (multi-domain)
        # ---------------------------------------------------------
        f.write("## Example Rows (Snow, Aurora, Air Quality)\n\n")
        f.write("```csv\n")
        f.write("# Snow domain\n")
        f.write("OBS-20251230-001,photo1_ingested.jpg,185.2,grainy,8,fast,\"Predicted Fast Melt BECAUSE Brightness > 180 AND Texture = grainy\"\n")
        f.write("OBS-20251230-002,photo2_ingested.jpg,95.1,smooth,2,slow,\"Predicted Slow Melt BECAUSE Brightness < 100 AND Texture = smooth\"\n\n")
        f.write("# Aurora domain\n")
        f.write("OBS-20251230-101,aurora1_ingested.jpg,12.4,smooth,1,moderate,\"Low brightness; aurora detection pipeline uses color channels instead\"\n\n")
        f.write("# Air quality domain\n")
        f.write("OBS-20251230-201,sky1_ingested.jpg,210.5,grainy,6,fast,\"High brightness + particulate scattering detected\"\n")
        f.write("```\n\n")

        # ---------------------------------------------------------
        # Best Practices
        # ---------------------------------------------------------
        f.write("## Best Practices\n")
        f.write("- Keep filenames consistent across pipeline stages\n")
        f.write("- Use Human_Influence_Note for qualitative context\n")
        f.write("- Texture_Class will expand with future classifier upgrades\n")
        f.write("- Ensure timestamps are ISO-formatted for cross-system compatibility\n\n")

        # ---------------------------------------------------------
        # Optional Future Feature
        # ---------------------------------------------------------
        f.write("## Optional Future: CSV Validation Mode\n")
        f.write("A future `--validate-csv` mode may:\n")
        f.write("- Check required columns\n")
        f.write("- Validate data types\n")
        f.write("- Flag missing or malformed fields\n")
        f.write("- Produce a compliance report\n\n")

    print("✓ Rich schema.md generated")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    # Schema stage requires no CSV input
    write_schema()
    print("🎉 Schema stage complete. Final outputs written to /data/testing-input-output")
    print("🏁 This is the final resting place of the pipeline.")


if __name__ == "__main__":
    main()



