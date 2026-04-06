"""
CHUONG 2.2 - Bai tap xu ly du lieu sinh vien.

Muc tieu:
- Moi bai in ro "Yeu cau" khi chay.
- Code chay on dinh tren terminal.
- Duong dan file duoc tinh theo vi tri script.
"""

import os
import sys
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
plt.rcParams["font.family"] = "DejaVu Sans"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "students_performance.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "students_cleaned_final.csv")
OUTPUT_PNG = os.path.join(BASE_DIR, "students_by_city.png")


def section(title: str, requirement: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print(f"Yeu cau: {requirement}")
    print("=" * 80)


def print_assignment_requirements() -> None:
    print("=" * 80)
    print("DE BAI - YEU CAU KHI CHAY C2.2_BT.py")
    print("=" * 80)
    print("Bai 1: Doc CSV, xem head/info/describe.")
    print("Bai 2: Lam sach du lieu (ep kieu, xu ly missing, duplicate).")
    print("Bai 3: Chuan hoa Name/City/Class.")
    print("Bai 4: Tao bien moi Total va Score_norm.")
    print("Bai 5: Phan tich theo City, Class, va top 3 Total.")
    print("Bai 6: Tim outlier theo Score (>9.5 hoac <5).")
    print("Bai 7: Truc quan hoa so luong sinh vien theo City.")
    print("Bai 8: In ket qua tong hop sau xu ly.")
    print("Bai 9: Luu ket qua ra CSV.")
    print("=" * 80)


print_assignment_requirements()
print("=" * 80)
print("BAI TAP XU LY DU LIEU SINH VIEN")
print("=" * 80)


# BAI 1: DOC VA KHAM PHA DU LIEU
section("BAI 1: DOC VA KHAM PHA DU LIEU", "Doc file dau vao va in thong tin tong quan.")
df = pd.read_csv(INPUT_CSV)
print("5 dong dau tien:")
print(df.head())
print("\nThong tin du lieu:")
df.info()
print("\nThong ke mo ta:")
print(df.describe(include="all"))


# BAI 2: LAM SACH DU LIEU
section(
    "BAI 2: LAM SACH DU LIEU",
    "Ep kieu cot so, xu ly gia tri thieu, va xoa dong trung lap.",
)

for col in ["Age", "Score", "Bonus"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
print("Da ep kieu Age/Score/Bonus ve dang so (neu co cot).")

print("\nSo luong du lieu thieu truoc xu ly:")
print(df.isnull().sum())

if "Age" in df.columns:
    age_mean = df["Age"].mean()
    df["Age"] = df["Age"].fillna(age_mean)
    print(f"Da thay Age thieu bang mean = {age_mean:.2f}")

if "Score" in df.columns:
    score_mean = df["Score"].mean()
    df["Score"] = df["Score"].fillna(score_mean)
    print(f"Da thay Score thieu bang mean = {score_mean:.2f}")

if "Bonus" in df.columns:
    bonus_mean = df["Bonus"].mean()
    df["Bonus"] = df["Bonus"].fillna(bonus_mean)
    print(f"Da thay Bonus thieu bang mean = {bonus_mean:.2f}")

if "City" in df.columns:
    df["City"] = df["City"].fillna("UNKNOWN")
    print("Da thay City thieu bang 'UNKNOWN'.")

duplicate_count = int(df.duplicated().sum())
print(f"So dong trung lap truoc khi xoa: {duplicate_count}")
df = df.drop_duplicates()
print(f"So dong con lai sau khi xoa duplicate: {len(df)}")

print("\nSo luong du lieu thieu sau xu ly:")
print(df.isnull().sum())
print(f"So dong trung lap sau xu ly: {int(df.duplicated().sum())}")


# BAI 3: CHUAN HOA DU LIEU
section(
    "BAI 3: CHUAN HOA DU LIEU",
    "Chuan hoa chuoi Name/City/Class: strip + doi dang chu.",
)

if "Name" in df.columns:
    df["Name"] = df["Name"].astype(str).str.strip().str.capitalize()
    print("Name sau chuan hoa:", sorted(df["Name"].dropna().unique()))

if "City" in df.columns:
    df["City"] = df["City"].astype(str).str.strip().str.upper()
    print("City sau chuan hoa:", sorted(df["City"].dropna().unique()))

if "Class" in df.columns:
    df["Class"] = df["Class"].astype(str).str.strip().str.upper()
    print("Class sau chuan hoa:", sorted(df["Class"].dropna().unique()))


# BAI 4: TAO BIEN MOI
section(
    "BAI 4: TAO BIEN MOI",
    "Tao cot Total = Score + Bonus va chuan hoa Score_norm theo min-max.",
)

if {"Score", "Bonus"}.issubset(df.columns):
    df["Total"] = df["Score"] + df["Bonus"]
else:
    df["Total"] = np.nan
print(df[[c for c in ["Name", "Score", "Bonus", "Total"] if c in df.columns]].head())

if "Score" in df.columns and df["Score"].max() != df["Score"].min():
    score_min = df["Score"].min()
    score_max = df["Score"].max()
    df["Score_norm"] = (df["Score"] - score_min) / (score_max - score_min)
    print(f"\nDa tao Score_norm voi min={score_min:.2f}, max={score_max:.2f}")
else:
    df["Score_norm"] = np.nan
    print("\nKhong the tao Score_norm vi Score khong hop le.")

print(df[[c for c in ["Name", "Score", "Score_norm"] if c in df.columns]].head())


# BAI 5: PHAN TICH DU LIEU
section(
    "BAI 5: PHAN TICH DU LIEU",
    "Thong ke theo City/Class va lay top 3 sinh vien theo Total.",
)

if {"City", "Score", "ID"}.issubset(df.columns):
    city_analysis = (
        df.groupby("City")
        .agg(Mean_Score=("Score", "mean"), Count=("ID", "count"))
        .sort_values("Mean_Score", ascending=False)
    )
    print("Phan tich theo City:")
    print(city_analysis)

if {"Class", "Score"}.issubset(df.columns):
    class_analysis = df.groupby("Class").agg(Mean_Score=("Score", "mean"), Max_Score=("Score", "max"))
    print("\nPhan tich theo Class:")
    print(class_analysis)

if "Total" in df.columns:
    top3_cols = [c for c in ["Name", "Class", "Score", "Bonus", "Total"] if c in df.columns]
    top3 = df.nlargest(3, "Total")[top3_cols]
    print("\nTop 3 sinh vien co Total cao nhat:")
    print(top3)


# BAI 6: PHAT HIEN DU LIEU BAT THUONG
section(
    "BAI 6: PHAT HIEN DU LIEU BAT THUONG",
    "Loc cac dong co Score > 9.5 hoac Score < 5.",
)

if "Score" in df.columns:
    outliers = df[(df["Score"] > 9.5) | (df["Score"] < 5)]
    print(f"So luong outlier: {len(outliers)}")
    if len(outliers) > 0:
        show_cols = [c for c in ["ID", "Name", "Score", "City", "Class"] if c in df.columns]
        print(outliers[show_cols])
    else:
        print("Khong co outlier theo dieu kien da cho.")


# BAI 7: TRUC QUAN HOA
section(
    "BAI 7: TRUC QUAN HOA",
    "Ve bieu do cot so luong sinh vien theo City va luu PNG.",
)

if "City" in df.columns:
    plt.figure(figsize=(10, 6))
    city_counts = df["City"].value_counts()
    plt.bar(city_counts.index, city_counts.values, color="#3498db")
    plt.xlabel("Thanh pho", fontsize=12, fontweight="bold")
    plt.ylabel("So luong sinh vien", fontsize=12, fontweight="bold")
    plt.title("SO LUONG SINH VIEN THEO THANH PHO", fontsize=14, fontweight="bold")
    plt.grid(axis="y", alpha=0.3)

    for idx, value in enumerate(city_counts.values):
        plt.text(idx, value + 0.1, str(value), ha="center", fontweight="bold")

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Da luu bieu do: {OUTPUT_PNG}")


# BAI 8: KET QUA
section(
    "BAI 8: KET QUA",
    "In DataFrame sau xu ly va bang thong ke theo City.",
)

print("DataFrame sau khi xu ly:")
print(df.to_string(index=False))

if {"City", "Score"}.issubset(df.columns):
    mean_score_by_city = df.groupby("City")["Score"].mean().round(2)
    count_by_city = df.groupby("City").size()
    print("\nDiem trung binh theo City:")
    print(mean_score_by_city)
    print("\nSo luong theo City:")
    print(count_by_city)


# BAI 9: LUU DU LIEU
section(
    "BAI 9: LUU DU LIEU",
    "Luu DataFrame da lam sach ra file CSV.",
)

df.to_csv(OUTPUT_CSV, index=False)
print(f"Da luu file: {OUTPUT_CSV}")
print(f"So luong ban ghi: {len(df)}")
print(f"So luong cot: {len(df.columns)}")

print("\n" + "=" * 80)
print("HOAN THANH TAT CA CAC BAI TAP")
print("=" * 80)
print("CAC FILE DA TAO:")
print(f"1. {OUTPUT_CSV}")
print(f"2. {OUTPUT_PNG}")
print("=" * 80)
