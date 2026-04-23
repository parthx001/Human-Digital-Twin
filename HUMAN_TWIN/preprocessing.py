import pandas as pd
import os
from pathlib import Path

def normalize(series):
    if series.max() == series.min():
        return series
    return (series - series.min()) / (series.max() - series.min())


def build_master_dataset():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    
    # Build file paths
    info_path = data_dir / "studentInfo.csv"
    assessment_path = data_dir / "studentAssessment.csv"
    vle_path = data_dir / "studentVle.csv"
    
    # Check if files exist
    for path in [info_path, assessment_path, vle_path]:
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            print(f"Current directory: {os.getcwd()}")
            print(f"Script directory: {script_dir}")
            raise FileNotFoundError(f"Required data file not found: {path}")
    
    try:
        studentInfo = pd.read_csv(str(info_path), encoding='utf-8')
        studentAssessment = pd.read_csv(str(assessment_path), encoding='utf-8')
        studentVle = pd.read_csv(str(vle_path), encoding='utf-8')
        print("[OK] Data loaded successfully")
    except UnicodeDecodeError as e:
        print(f"ERROR: Encoding issue reading CSV files: {e}")
        print("Trying with 'latin-1' encoding...")
        studentInfo = pd.read_csv(str(info_path), encoding='latin-1')
        studentAssessment = pd.read_csv(str(assessment_path), encoding='latin-1')
        studentVle = pd.read_csv(str(vle_path), encoding='latin-1')
    except Exception as e:
        print(f"ERROR reading CSV files: {e}")
        raise

    engagement = (
        studentVle.groupby("id_student")["sum_click"]
        .sum()
        .reset_index()
    )
    engagement.rename(columns={"sum_click": "engagement"}, inplace=True)

    grades = (
        studentAssessment.groupby("id_student")["score"]
        .mean()
        .reset_index()
    )
    grades.rename(columns={"score": "avg_grade"}, inplace=True)

    df = studentInfo.merge(grades, on="id_student", how="left")
    df = df.merge(engagement, on="id_student", how="left")
    df = df.fillna(0)

    df["dropout_flag"] = df["final_result"].apply(
        lambda x: 1 if x == "Withdrawn" else 0
    )

    df["engagement_norm"] = normalize(df["engagement"])
    df["grade_norm"] = normalize(df["avg_grade"])
    df["stress_proxy"] = 1 - df["engagement_norm"]

    return df[[
        "engagement_norm",
        "grade_norm",
        "stress_proxy",
        "dropout_flag"
    ]]