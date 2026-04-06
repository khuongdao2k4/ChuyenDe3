"""
CHUONG 2.1 - C2_slide12.py

Muc tieu:
- Code chay duoc
- Co chu thich ro tung phan
- Khi chay se in ro "Yeu cau" cua tung bai
"""

import sys
import numpy as np


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def task_header(task_name: str, requirement: str) -> None:
    print(f"\n===== {task_name} =====")
    print(f"Yeu cau: {requirement}")


print("CHAY FILE: C2_slide12.py")
print("Tong quan de bai: Thuc hanh tao mang, thong ke, indexing, dieu kien voi NumPy.")


# BAI 1
task_header(
    "BAI 1: TAO VA KIEM TRA MANG",
    "Tao vector 1D va ma tran 3x3, sau do in shape/ndim/dtype.",
)

vector = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print("Vector:", vector)
print("Shape:", vector.shape)
print("So chieu (ndim):", vector.ndim)
print("Kieu du lieu (dtype):", vector.dtype)

print("\nMa tran 3x3:")
print(matrix)
print("Shape:", matrix.shape)
print("So chieu (ndim):", matrix.ndim)
print("Kieu du lieu (dtype):", matrix.dtype)


# BAI 2
task_header(
    "BAI 2: KHOI TAO DAC BIET",
    "Tao ma tran zeros(3x4), ones(2x3), eye(4x4).",
)

zeros_matrix = np.zeros((3, 4))
ones_matrix = np.ones((2, 3))
identity_matrix = np.eye(4)

print("Ma tran toan 0 (3x4):\n", zeros_matrix)
print("Ma tran toan 1 (2x3):\n", ones_matrix)
print("Ma tran don vi (4x4):\n", identity_matrix)


# BAI 3
task_header(
    "BAI 3: TAO DAY SO",
    "Tao mang tu 0 den 20 buoc 2, tinh tong va trung binh.",
)

arr = np.arange(0, 21, 2)
print("Mang:", arr)
print("Tong:", np.sum(arr))
print("Trung binh:", np.mean(arr))


# BAI 4
task_header(
    "BAI 4: RANDOM + THONG KE",
    "Tao ma tran random 5x5 va tinh max/min/mean/std.",
)

random_matrix = np.random.rand(5, 5)
print("Ma tran random (5x5):\n", random_matrix)
print("Gia tri lon nhat (max):", np.max(random_matrix))
print("Gia tri nho nhat (min):", np.min(random_matrix))
print("Trung binh (mean):", np.mean(random_matrix))
print("Do lech chuan (std):", np.std(random_matrix))


# BAI 5
task_header(
    "BAI 5: INDEXING",
    "Lay dong 2, cot 3, va phan tu (2,2) cua ma tran 3x3.",
)

a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("Ma tran a:\n", a)
print("Dong 2:", a[1])
print("Cot 3:", a[:, 2])
print("Phan tu (2,2):", a[1, 1])


# BAI 6
task_header(
    "BAI 6: DIEU KIEN + WHERE",
    "Loc gia tri > 5 va in vi tri cua chung trong ma tran.",
)

greater_than_5 = a[a > 5]
print("Cac phan tu > 5:", greater_than_5)

positions = np.where(a > 5)
print("Vi tri cac phan tu > 5 (hang, cot):")
for row_idx, col_idx in zip(positions[0], positions[1]):
    print(f"({row_idx}, {col_idx})")
