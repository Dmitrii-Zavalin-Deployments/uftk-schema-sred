import os
import shutil

# ---------------------------------------------------------
# Unified working directory
# ---------------------------------------------------------

WORKING_DIR = "/data/testing-input-output"
CSV_PATH = os.path.join(WORKING_DIR, "field_data.csv")
SCHEMA_PATH = os.path.join(WORKING_DIR, "schema.md")

# ---------------------------------------------------------
# Generate schema.md
# ---------------------------------------------------------

def write_schema():
    with open(SCHEMA_PATH, "w") as f:
        f.write("# Universal Field Toolkit Schema\n\n")
        f.write("## Required Columns\n")
        f.write("- Observation_ID\n")
        f.write("- Photo_Filename\n")
        f.write("- Observation_Type\n")
        f.write("- Timestamp\n")
        f.write("- Date\n")
        f.write("- Time_Of_Day\n")
        f.write("- GPS\n")
        f.write("- Human_Influence_Score\n")
        f.write("- Human_Influence_Note\n")
        f.write("- Notes\n")
        f.write("- brightness\n")
        f.write("- Mean_R\n")
        f.write("- Mean_G\n")
        f.write("- Mean_B\n")
        f.write("- Texture\n")
        f.write("- Texture_Class\n")
        f.write("- Edge_Density\n")
        f.write("- Shadow_Intensity\n")
        f.write("- Predicted_Melt_Rate\n")
        f.write("- Explanation\n")
        f.write("- Global_Correlation_Count\n")

    print("✓ schema.md generated")

# ---------------------------------------------------------
# Copy predicted → final
# ---------------------------------------------------------

def generate_final_images():
    for filename in os.listdir(WORKING_DIR):
        if filename.endswith("_predicted.jpg"):
            src = os.path.join(WORKING_DIR, filename)
            base = filename.replace("_predicted", "")
            dst = os.path.join(WORKING_DIR, f"{base}_final.jpg")
            shutil.copy2(src, dst)
            print(f"✓ Created {dst}")

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    if not os.path.isfile(CSV_PATH):
        print("❌ ERROR: field_data.csv not found.")
        return

    write_schema()
    generate_final_images()

    print("🎉 Schema stage complete. Final outputs written to /data/testing-input-output")
    print("🏁 This is the final resting place of the pipeline.")

if __name__ == "__main__":
    main()



