from preprocessing import build_master_dataset

print("Starting preprocessing test...\n")

try:
    df = build_master_dataset()

    print("\n===== MASTER DATASET PREVIEW =====\n")
    print(df.head())

    print("\n===== DATASET INFO =====\n")
    print("Total Students:", len(df))
    print("Dropout Rate:", round(df["dropout_flag"].mean(), 3))

    print("\nColumns:", df.columns.tolist())

    print("\nPreprocessing completed successfully ✅")

except Exception as e:
    print("\n❌ Error occurred during preprocessing:")
    print(e)