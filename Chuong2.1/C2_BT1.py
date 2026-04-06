"""
CHUONG 2.1 - C2_BT1.py

Yeu cau chung:
- Moi phan can ghi ro slide nao.
- Khi chay can in ro "Yeu cau" cua slide do.
- Logic NumPy/Pandas giong noi dung bai giang.
"""

import sys
import numpy as np
import pandas as pd


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def section(title: str, requirement: str | None = None) -> None:
    print(f"\n=== {title} ===")
    if requirement:
        print(f"Yeu cau: {requirement}")


# ===== PHAN 1: NUMPY =====

# Slide 12: 1D va 2D
section("Slide 12 - Mang 1D va 2D", "Tao mang 1D, 2D va in ket qua.")
a = np.array([4, 6, 7, 5])
c = np.array([(4, 6, 7), (7, 4, 2)])
print("a:", a)
print("c:\n", c)

# Slide 13: 3D
section("Slide 13 - Mang 3D", "Tao mang 3 chieu.")
c3 = np.array([[(4, 6, 7), (7, 4, 2)], [(4, 5, 1), (8, 4, 3)]])
print(c3)

# Slide 14: zeros & ones
section("Slide 14 - zeros va ones", "Khoi tao mang toan 0 va toan 1.")
zero = np.zeros((5, 3))
one = np.ones((3, 2))
print("zeros:\n", zero)
print("ones:\n", one)

# Slide 15: eye & random
section("Slide 15 - eye va random", "Tao ma tran don vi va mang random.")
arr_eye = np.eye(4)
arr_rand = np.random.random((4, 3))
print("eye:\n", arr_eye)
print("random:\n", arr_rand)

# Slide 16: randint
section("Slide 16 - randint", "Sinh so ngau nhien cho mang 1D va 2D.")
arr_randint = np.random.randint(5, 10, size=6)
arr_randint2 = np.random.randint(2, 5, size=(3, 4))
print("randint 1D:", arr_randint)
print("randint 2D:\n", arr_randint2)

# Slide 17: arange & linspace
section("Slide 17 - arange va linspace", "Tao day so cach deu bang 2 cach.")
d = np.arange(6, 20, 2)
d2 = np.linspace(6, 10, 5)
print("arange d:", d)
print("linspace d2:", d2)

# Slide 20: thong tin mang
section("Slide 20 - Thuoc tinh mang", "In shape, size, ndim cua mang.")
print("shape/size/ndim:", a.shape, a.size, a.ndim)

# Slide 21: ep kieu
section("Slide 21 - Ep kieu", "Ep kieu mang float sang int16.")
d_int = d2.astype(np.int16)
print(d_int)

# Slide 23: truy cap vector
section("Slide 23 - Truy cap vector", "Lay phan tu dau/cuoi va cat mang.")
print("first/last/slice:", d[0], d[-1], d[:5])

# Slide 24: truy cap ma tran
section("Slide 24 - Truy cap ma tran", "Lay phan tu, cot, dong trong ma tran.")
mat = np.random.randint(1, 10, size=(5, 4))
print("mat[0,0]:", mat[0, 0])
print("cot 0:", mat[:, 0])
print("dong 0:", mat[0, :])


# ===== PHAN 2: PANDAS =====

# Slide 29: Series
section("Slide 29 - Series", "Tao va in pandas Series.")
sr = pd.Series([1232, 3234, 3250, 2222])
print(sr)

# Slide 30: DataFrame
section("Slide 30 - DataFrame", "Tao va in pandas DataFrame.")
df = pd.DataFrame([[4324, 1242], [6788, 7334]], columns=["Pandas", "NumPy"])
print(df)

# Slide 33: dropna Series
section("Slide 33 - dropna Series", "Loai bo gia tri thieu trong Series.")
population = pd.Series({"TP.HCM": 8993, "Hanoi": 8053, "Lam Dong": np.nan})
population_clean = population.dropna()
print("population:\n", population)
print("population_clean:\n", population_clean)

# Slide 34-36: dropna DataFrame
section("Slide 34-36 - dropna DataFrame", "Loai bo dong chua NaN trong DataFrame.")
df_na = pd.DataFrame([{"a": 1, "b": 2}, {"b": 3}])
df_clean = df_na.dropna()
print("df_na:\n", df_na)
print("df_clean:\n", df_clean)

# Slide 37-38: fillna
section("Slide 37-38 - fillna", "Thay NaN bang gia tri mac dinh.")
df_fill = df_na.fillna(0)
print(df_fill)

# Slide 39-41: duplicates
section("Slide 39-41 - drop_duplicates", "Loai bo dong bi trung lap.")
df_dup = pd.DataFrame({"Name": ["An", "An", "Binh"], "Score": [8, 8, 9]})
df_unique = df_dup.drop_duplicates()
print("df_dup:\n", df_dup)
print("df_unique:\n", df_unique)

# Slide 44: groupby
section("Slide 44 - GroupBy mean", "Nhom du lieu va tinh trung binh.")
df_group = pd.DataFrame({"key1": ["a", "a", "b"], "data": [1, 2, 3]})
print(df_group.groupby("key1").mean())

# Slide 46: agg
section("Slide 46 - GroupBy agg", "Nhom du lieu va tinh mean/std.")
print(df_group.groupby("key1").agg(["mean", "std"]))

# Slide 47: agg nhieu cot
section("Slide 47 - Agg nhieu cot", "Dung ham tong hop khac nhau cho tung cot.")
df_multi = pd.DataFrame({"key1": ["a", "a", "b"], "data1": [1, 2, 3], "data2": [4, 5, 6]})
print(df_multi.groupby("key1").agg({"data1": "max", "data2": "sum"}))

# Slide 48: pivot table
section("Slide 48 - Pivot table", "Tao bang tong hop bang pivot_table.")
print(df_multi.pivot_table(index="key1"))

# Slide 51-52: merge
section("Slide 51-52 - Merge inner", "Noi 2 DataFrame theo cot key.")
df1 = pd.DataFrame({"key": ["a", "b"], "data1": [1, 2]})
df2 = pd.DataFrame({"key": ["a", "b"], "data2": [3, 4]})
print(pd.merge(df1, df2, on="key"))

# Slide 54: outer join
section("Slide 54 - Outer join", "Noi DataFrame theo kieu outer.")
print(pd.merge(df1, df2, how="outer"))

# Slide 55: suffixes
section("Slide 55 - Merge suffixes", "Noi DataFrame va dat hau to cho cot trung ten.")
left = pd.DataFrame({"key": ["a", "b"], "val": [1, 2]})
right = pd.DataFrame({"key": ["a", "b"], "val": [3, 4]})
print(pd.merge(left, right, on="key", suffixes=("_l", "_r")))

# Slide 57: DataFrame -> NumPy
section("Slide 57 - DataFrame sang NumPy", "Lay mang NumPy tu DataFrame.")
print(df.values)

# Slide 60: Feature Engineering
section("Slide 60 - Feature engineering", "Tao cot ty le tu cot births.")
names = pd.DataFrame({"name": ["Anna", "Mary"], "births": [100, 200]})
names["prop"] = names["births"] / names["births"].sum()
print(names)

# Slide 61: Weighted average
section("Slide 61 - Weighted average", "Tinh trung binh co trong so.")
df_w = pd.DataFrame({"data": [1, 2, 3], "weights": [0.2, 0.3, 0.5]})
print("input:\n", df_w)
print("weighted average:", np.average(df_w["data"], weights=df_w["weights"]))

# Slide 62-63: Demean
section("Slide 62-63 - Demean", "Tru di gia tri trung binh theo nhom.")
df_dm = pd.DataFrame({"key": ["a", "a", "b"], "col": [1, 2, 3]})
df_dm["demean"] = df_dm["col"] - df_dm.groupby("key")["col"].transform("mean")
print(df_dm)

# Slide 64: Dummy variables
section("Slide 64 - Dummy variables", "Ma hoa bien phan loai thanh cot 0/1.")
df_dummy = pd.DataFrame({"key": ["a", "b", "a"]})
print(pd.get_dummies(df_dummy["key"]))
