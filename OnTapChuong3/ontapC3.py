# =============================================================================
# THỰC HÀNH NUMPY NÂNG CAO – THỐNG KÊ, TUYẾN TÍNH, RANDOM
# =============================================================================
# File này chứa lời giải đầy đủ cho 6 bài thực hành NumPy nâng cao.
# Mỗi dòng code đều được chú thích chi tiết bằng tiếng Việt.
# =============================================================================

import numpy as np                  # Nhập thư viện NumPy và đặt bí danh là 'np'
import matplotlib.pyplot as plt     # Nhập thư viện Matplotlib để vẽ đồ thị
import pandas as pd                 # Nhập thư viện Pandas để xử lý DataFrame (Bài 6)

from pathlib import Path            # Lam viec voi duong dan da nen tang


# =============================================================================
# BÀI 1. THỐNG KÊ MÔ TẢ TRÊN DỮ LIỆU ĐIỂM SINH VIÊN
# =============================================================================
print("=" * 60)
print("BÀI 1. THỐNG KÊ MÔ TẢ TRÊN DỮ LIỆU ĐIỂM SINH VIÊN")
print("=" * 60)

# --- Tạo ma trận điểm ---
# np.array() tạo một mảng NumPy từ danh sách Python lồng nhau.
# Kết quả là ma trận 5 hàng x 4 cột:
#   - Mỗi hàng = 1 sinh viên (5 sinh viên)
#   - Mỗi cột  = 1 môn học   (4 môn)
scores = np.array([
    [7.5, 8.0, 6.5, 9.0],   # Sinh viên 0
    [6.0, 7.0, 7.5, 8.0],   # Sinh viên 1
    [8.5, 9.0, 8.0, 9.5],   # Sinh viên 2
    [5.5, 6.0, 6.5, 7.0],   # Sinh viên 3
    [9.0, 8.5, 9.5, 8.0],   # Sinh viên 4
])

# 1. In ra ma trận điểm
print("\n1. Ma trận điểm (5 sinh viên x 4 môn):")
print(scores)                        # In toàn bộ ma trận ra màn hình

# 2. Điểm trung bình toàn bộ ma trận
# np.mean() không có tham số axis sẽ tính trung bình TẤT CẢ phần tử.
print("\n2. Điểm trung bình toàn bộ:", np.mean(scores))

# 3. Điểm trung bình theo từng sinh viên (theo hàng)
# axis=1 → cộng/tính dọc theo chiều cột (tức là gộp các cột lại)
# → mỗi hàng (mỗi sinh viên) ra 1 giá trị trung bình.
print("\n3. Điểm trung bình từng sinh viên:", np.mean(scores, axis=1))

# 4. Điểm trung bình theo từng môn (theo cột)
# axis=0 → cộng/tính dọc theo chiều hàng (tức là gộp các hàng lại)
# → mỗi cột (mỗi môn) ra 1 giá trị trung bình.
print("\n4. Điểm trung bình từng môn:", np.mean(scores, axis=0))

# 5. Điểm cao nhất và thấp nhất
# np.max() / np.min() không có axis → tìm trên toàn bộ ma trận.
print("\n5. Điểm cao nhất:", np.max(scores))
print("   Điểm thấp nhất:", np.min(scores))

# 6. Độ lệch chuẩn theo từng môn
# np.std() với axis=0 tính độ lệch chuẩn của từng cột (từng môn).
# Độ lệch chuẩn lớn = điểm sinh viên trong môn đó chênh lệch nhau nhiều.
print("\n6. Độ lệch chuẩn từng môn:", np.std(scores, axis=0))

# 7. Sinh viên có điểm trung bình cao nhất
# Bước 1: tính điểm TB từng sinh viên (axis=1).
avg_students = np.mean(scores, axis=1)
# np.argmax() trả về CHỈ SỐ (index) của phần tử lớn nhất trong mảng.
best_student = np.argmax(avg_students)
print("\n7. Điểm TB từng sinh viên:", avg_students)
print("   Sinh viên có điểm TB cao nhất là vị trí index:", best_student,
      f"(điểm TB = {avg_students[best_student]:.2f})")


# =============================================================================
# BÀI 2. CHUẨN HÓA DỮ LIỆU BẰNG BROADCASTING
# =============================================================================
print("\n" + "=" * 60)
print("BÀI 2. CHUẨN HÓA DỮ LIỆU BẰNG BROADCASTING")
print("=" * 60)

# 1. Vector trung bình từng môn (axis=0 → tính theo cột)
# Kết quả là mảng 1-D có 4 phần tử, mỗi phần tử là TB của 1 môn.
mean_col = np.mean(scores, axis=0)
print("\n1. Trung bình từng môn:", mean_col)

# 2. Vector độ lệch chuẩn từng môn (axis=0)
std_col = np.std(scores, axis=0)
print("2. Độ lệch chuẩn từng môn:", std_col)

# 3. Chuẩn hóa Z-score bằng Broadcasting
# Broadcasting: NumPy tự động "mở rộng" mean_col (shape 4,) và std_col (shape 4,)
# để khớp với scores (shape 5x4). Phép trừ và chia diễn ra theo từng cột.
# Công thức Z-score: z = (x - mean) / std
# Sau chuẩn hóa: TB mỗi cột ≈ 0, độ lệch chuẩn mỗi cột ≈ 1.
z_scores = (scores - mean_col) / std_col

# 4. In ma trận đã chuẩn hóa, làm tròn 2 chữ số thập phân
# np.round(array, 2) làm tròn mỗi phần tử đến 2 chữ số sau dấu phẩy.
print("\n4. Ma trận Z-score (làm tròn 2 chữ số):")
print(np.round(z_scores, 2))

# 5. Kiểm tra trung bình các cột sau chuẩn hóa (phải ≈ 0)
# Do sai số dấu phẩy động (floating-point), kết quả thường là số rất nhỏ ~1e-16.
print("\n5. TB các cột sau chuẩn hóa Z-score:", np.mean(z_scores, axis=0))

# --- Yêu cầu mở rộng: Chuẩn hóa Min-Max về khoảng [0, 1] ---
# Công thức: x_norm = (x - x_min) / (x_max - x_min)
# Sau chuẩn hóa: mỗi cột có giá trị nhỏ nhất = 0, lớn nhất = 1.
min_col = np.min(scores, axis=0)     # Giá trị nhỏ nhất của mỗi môn
max_col = np.max(scores, axis=0)     # Giá trị lớn nhất của mỗi môn
minmax_scores = (scores - min_col) / (max_col - min_col)  # Broadcasting
print("\n[Mở rộng] Ma trận chuẩn hóa Min-Max [0,1] (làm tròn 2 chữ số):")
print(np.round(minmax_scores, 2))


# =============================================================================
# BÀI 3. PHÂN TÍCH DOANH THU BẰNG PHÉP TOÁN MA TRẬN
# =============================================================================
print("\n" + "=" * 60)
print("BÀI 3. PHÂN TÍCH DOANH THU BẰNG PHÉP TOÁN MA TRẬN")
print("=" * 60)

# Ma trận số lượng: 3 sản phẩm x 4 ngày
# Hàng 0 = Sản phẩm A, Hàng 1 = Sản phẩm B, Hàng 2 = Sản phẩm C
quantity = np.array([
    [10, 12, 9, 14],   # Sản phẩm A
    [5,  7,  8,  6],   # Sản phẩm B
    [20, 18, 25, 22],  # Sản phẩm C
])

# Giá của mỗi sản phẩm (đơn vị: VNĐ), mảng 1-D có 3 phần tử.
price = np.array([15000, 25000, 10000])

# 1. Doanh thu từng sản phẩm theo từng ngày
# price.reshape(3, 1) biến mảng shape (3,) thành shape (3, 1).
# Khi nhân với quantity shape (3, 4), Broadcasting tự mở rộng cột:
# mỗi hàng (sản phẩm) được nhân với giá tương ứng.
revenue = quantity * price.reshape(3, 1)
print("\n1. Doanh thu từng sản phẩm theo từng ngày (VNĐ):")
print(revenue)

# 2. Tổng doanh thu của từng sản phẩm (cộng theo chiều cột → axis=1)
# → cộng tất cả ngày lại, còn lại 1 giá trị cho mỗi sản phẩm.
sum_product = np.sum(revenue, axis=1)
print("\n2. Tổng doanh thu từng sản phẩm (VNĐ):", sum_product)

# 3. Tổng doanh thu của từng ngày (cộng theo chiều hàng → axis=0)
# → cộng tất cả sản phẩm lại, còn lại 1 giá trị cho mỗi ngày.
sum_day = np.sum(revenue, axis=0)
print("\n3. Tổng doanh thu từng ngày (VNĐ):", sum_day)

# 4. Ngày có doanh thu cao nhất
# np.argmax() trả về index (0-based), +1 để ra số ngày (1-based).
best_day = np.argmax(sum_day) + 1
print(f"\n4. Ngày có doanh thu cao nhất: Ngày {best_day} ({sum_day[best_day-1]:,} VNĐ)")

# 5. Tỷ trọng doanh thu của từng sản phẩm (%)
# Chia doanh thu từng sản phẩm cho tổng doanh thu của tất cả sản phẩm.
ratio = sum_product / np.sum(sum_product)  # Kết quả là tỷ lệ [0,1]
print("\n5. Tỷ trọng doanh thu từng sản phẩm (%):",
      np.round(ratio * 100, 2))            # Nhân 100 để ra %, làm tròn 2 chữ số


# =============================================================================
# BÀI 4. ĐẠI SỐ TUYẾN TÍNH CƠ BẢN VỚI NUMPY
# =============================================================================
print("\n" + "=" * 60)
print("BÀI 4. ĐẠI SỐ TUYẾN TÍNH CƠ BẢN VỚI NUMPY")
print("=" * 60)

# Định nghĩa hai ma trận vuông 2x2
A = np.array([
    [2, 1],
    [1, 3],
])

B = np.array([
    [4, 2],
    [1, 5],
])

# 1. Tính A + B
# Phép cộng ma trận: cộng từng phần tử tương ứng.
print("\n1. A + B =\n", A + B)

# 2. Tính A - B
# Phép trừ ma trận: trừ từng phần tử tương ứng.
print("\n2. A - B =\n", A - B)

# 3. Tích ma trận A @ B
# Toán tử @ trong Python (NumPy) thực hiện nhân ma trận (dot product).
# Khác với A * B là nhân từng phần tử (element-wise).
print("\n3. A @ B (tích ma trận) =\n", A @ B)

# 4. Định thức của ma trận A
# np.linalg.det() tính định thức (determinant) của ma trận vuông.
# Định thức ≠ 0 → ma trận khả nghịch; Định thức = 0 → không khả nghịch.
det_A = np.linalg.det(A)
print(f"\n4. det(A) = {det_A:.4f}")

# 5. Ma trận nghịch đảo của A
# np.linalg.inv() tính ma trận nghịch đảo A^-1.
# Tính chất: A @ A^-1 = I (ma trận đơn vị).
inv_A = np.linalg.inv(A)
print("\n5. A^-1 =\n", inv_A)

# Kiểm tra: A @ A^-1 phải bằng ma trận đơn vị I
print("   Kiểm tra A @ A^-1 (phải ≈ ma trận đơn vị):\n", np.round(A @ inv_A, 10))

# 6. Giải hệ phương trình: 2x + y = 5  và  x + 3y = 7
# Dạng ma trận: A @ x = b, với A là ma trận hệ số, b là vế phải.
# np.linalg.solve(A, b) tính nghiệm x = A^-1 @ b một cách ổn định số học.
b = np.array([5, 7])           # Vế phải của hệ phương trình
solution = np.linalg.solve(A, b)  # Trả về mảng [x, y]
print(f"\n6. Nghiệm hệ phương trình: x = {solution[0]:.4f}, y = {solution[1]:.4f}")

# --- Yêu cầu mở rộng: kiểm tra lại nghiệm ---
# Thay nghiệm vào: A @ solution phải = b
check = A @ solution           # Tính lại vế trái
print("   Kiểm tra A @ nghiệm (phải = [5, 7]):", check)

# Giải thích khi nào ma trận không khả nghịch
print("\n   [Ghi chú] Ma trận KHÔNG khả nghịch khi det = 0,")
print("   tức là các phương trình trong hệ phụ thuộc tuyến tính nhau.")


# =============================================================================
# BÀI 5. MÔ PHỎNG RANDOM WALK
# =============================================================================
print("\n" + "=" * 60)
print("BÀI 5. MÔ PHỎNG RANDOM WALK")
print("=" * 60)

# Đặt seed để kết quả tái lập được (reproducible).
# Seed giống nhau → dãy số ngẫu nhiên giống nhau mỗi lần chạy.
np.random.seed(42)

# 1. Tạo 100 bước ngẫu nhiên, mỗi bước là +1 hoặc -1
# np.random.choice([-1, 1], size=100): chọn ngẫu nhiên 100 giá trị
# từ tập {-1, 1} với xác suất đều nhau (50/50).
steps = np.random.choice([-1, 1], size=100)

# 2. Tính vị trí sau mỗi bước
# np.cumsum() tính tổng tích lũy (cumulative sum).
# Ví dụ: steps = [1, -1, 1, 1] → walk = [1, 0, 1, 2]
walk = np.cumsum(steps)

# 3. In 10 giá trị đầu tiên
# walk[:10] lấy slice từ index 0 đến 9 (10 phần tử đầu tiên).
print("\n3. 10 vị trí đầu tiên:", walk[:10])

# 4. Vẽ đồ thị random walk
plt.figure(figsize=(10, 4))          # Tạo cửa sổ đồ thị kích thước 10x4 inch
plt.plot(walk, color='steelblue', linewidth=1.5)  # Vẽ đường đi
plt.axhline(0, color='red', linestyle='--', linewidth=0.8)  # Đường chuẩn y=0
plt.title("Random Walk 1 chiều (100 bước)")  # Tiêu đề đồ thị
plt.xlabel("Bước")                   # Nhãn trục X
plt.ylabel("Vị trí")                 # Nhãn trục Y
plt.grid(True, alpha=0.3)            # Hiển thị lưới với độ trong suốt 30%
plt.tight_layout()                   # Tự căn chỉnh bố cục
# Luu anh vao thu muc outputs cung cap voi script (tu tao neu chua co)
output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "random_walk.png"
plt.savefig(output_path, dpi=150)
plt.show()                           # Hiển thị đồ thị

# 5. Vị trí cuối cùng, lớn nhất, nhỏ nhất
# walk[-1]: phần tử cuối cùng (vị trí sau 100 bước)
print("5. Vị trí cuối cùng:", walk[-1])
print("   Vị trí lớn nhất đạt được:", np.max(walk))   # Cao nhất trong toàn bộ hành trình
print("   Vị trí nhỏ nhất đạt được:", np.min(walk))   # Thấp nhất trong toàn bộ hành trình

# --- Yêu cầu nâng cao: 100 random walk đồng thời ---
print("\n--- Nâng cao: Mô phỏng 100 random walk ---")

# Tạo ma trận bước: 100 walk x 100 bước, mỗi ô là +1 hoặc -1
steps_many = np.random.choice([-1, 1], size=(100, 100))

# np.cumsum(axis=1): tính cumsum theo chiều cột (dọc theo từng walk)
# Kết quả: ma trận 100x100 các vị trí tích lũy
walks_many = np.cumsum(steps_many, axis=1)

# Vị trí cuối cùng của mỗi walk: lấy cột cuối (index -1)
final_positions = walks_many[:, -1]     # Shape (100,)

# Đếm số walk kết thúc ở vị trí dương (> 0)
# np.sum(bool_array) đếm số True trong mảng boolean
print("Số walk kết thúc dương:", np.sum(final_positions > 0))

# Đếm số walk từng chạm ngưỡng |position| >= 10 tại bất kỳ bước nào
# np.abs() lấy giá trị tuyệt đối từng phần tử
# np.any(condition, axis=1): True nếu có ÍT NHẤT 1 phần tử thỏa điều kiện trên hàng đó
hit_10 = np.any(np.abs(walks_many) >= 10, axis=1)
print("Số walk từng chạm ngưỡng |10|:", np.sum(hit_10))

# --- Nhận xét ngắn ---
print("""
[Nhận xét]
- Random walk KHÔNG có xu hướng cố định về 1 hướng (không có "drift").
  Vị trí cuối cùng xoay quanh 0 do tính đối xứng +1/-1.
- Cần đặt seed để kết quả tái lập được khi kiểm tra hay báo cáo lại.
- Broadcasting trong Bài 2 giúp chuẩn hóa toàn bộ ma trận chỉ bằng
  1 phép tính, thay vì phải dùng vòng lặp qua từng cột, tiết kiệm
  thời gian và code ngắn gọn hơn.
""")


# =============================================================================
# BÀI 6. XÂY DỰNG QUY TRÌNH THU THẬP VÀ CHUẨN HÓA DỮ LIỆU NGHIÊN CỨU
# =============================================================================
print("=" * 60)
print("BÀI 6. XỬ LÝ VÀ CHUẨN HÓA DỮ LIỆU NGHIÊN CỨU")
print("=" * 60)

# -----------------------------------------------
# PHẦN 1: Mô tả quy trình thu thập dữ liệu
# -----------------------------------------------
print("""
[Phần 1 – Quy trình thu thập dữ liệu]
  1. Xác định mục tiêu: phân tích ảnh hưởng giờ tự học & MXH đến điểm TB.
  2. Đối tượng: sinh viên năm 2 và năm 3.
  3. Thiết kế phiếu: MaSV, Tuổi, GioiTinh, GioTuHoc, GioMangXaHoi, DiemTB.
  4. Thu thập: Google Form / Excel / CSV.
  5. Kiểm tra chất lượng: dữ liệu thiếu, trùng, không đồng nhất, ngoại lệ.
  6. Chuẩn hóa và lưu dữ liệu sạch để phân tích tiếp.
""")

# -----------------------------------------------
# PHẦN 2: Dữ liệu thô ban đầu
# -----------------------------------------------
# Tạo dictionary chứa dữ liệu thô với các vấn đề cố tình:
#   - SV03 bị trùng lặp (xuất hiện 2 lần)
#   - Có giá trị None (thiếu dữ liệu)
#   - GioiTinh không thống nhất: "nu" vs "Nữ"
#   - Tuổi 35 bất thường (> 30)
#   - GioTuHoc = -1 bất thường (không thể âm)
#   - GioMangXaHoi = 20 bất thường (> 12 giờ/ngày)
#   - DiemTB = 4.5 bất thường (thang điểm 4.0)
data = {
    "MaSV":         ["SV01", "SV02", "SV03", "SV03", "SV05", "SV06", "SV07", "SV08"],
    "Tuoi":         [20, 21, 19, 19, None, 22, 35, 20],
    "GioiTinh":     ["Nam", "Nữ", "nu", "nu", "Nam", "Nữ", "Nam", None],
    "GioTuHoc":     [2.5, 3, None, 4, 2, 10, -1, 3.5],
    "GioMangXaHoi": [4, 5, 3.5, 3.5, 20, 2, 5, None],
    "DiemTB":       [3.1, 2.8, 3.5, 3.5, 2.0, 3.8, 4.5, None],
}

# pd.DataFrame(data): tạo bảng dữ liệu dạng bảng (DataFrame) từ dictionary.
df = pd.DataFrame(data)
print("[Phần 2] Dữ liệu thô ban đầu:")
print(df)

# -----------------------------------------------
# PHẦN 3: Xử lý và làm sạch dữ liệu
# -----------------------------------------------
print("\n[Phần 3] Xử lý dữ liệu\n")

# 1. Kích thước và số lượng giá trị thiếu
# df.shape trả về (số hàng, số cột)
print("1. Kích thước bộ dữ liệu:", df.shape)

# df.isnull() tạo DataFrame boolean: True nơi có giá trị None/NaN
# .sum() đếm số True theo từng cột → số giá trị thiếu mỗi cột
print("   Dữ liệu thiếu theo từng cột:\n", df.isnull().sum())

# 2–3. Xóa bản ghi trùng lặp theo cột MaSV
# drop_duplicates(subset="MaSV"): giữ lần xuất hiện đầu tiên, xóa các hàng trùng MaSV.
df = df.drop_duplicates(subset="MaSV")
print("\n2-3. Sau khi xóa bản ghi trùng (SV03 chỉ còn 1 lần):")
print(df[["MaSV", "GioiTinh", "Tuoi"]])

# 4. Chuẩn hóa cột GioiTinh về các giá trị thống nhất
# .replace(dict): thay thế các giá trị theo ánh xạ trong dict.
df["GioiTinh"] = df["GioiTinh"].replace({
    "nu": "Nữ",   # Sửa chính tả "nu" → "Nữ"
    "Nữ": "Nữ",   # Giữ nguyên "Nữ"
    "Nam": "Nam", # Giữ nguyên "Nam"
})
# .fillna("Không rõ"): điền giá trị "Không rõ" vào chỗ None còn lại
df["GioiTinh"] = df["GioiTinh"].fillna("Không rõ")
print("\n4. Cột GioiTinh sau khi chuẩn hóa:", df["GioiTinh"].values)

# 5. Điền dữ liệu thiếu bằng giá trị trung bình của từng cột số
# .mean() tính trung bình (bỏ qua NaN), .fillna(mean) điền vào chỗ NaN.
df["Tuoi"]         = df["Tuoi"].fillna(df["Tuoi"].mean())
df["GioTuHoc"]     = df["GioTuHoc"].fillna(df["GioTuHoc"].mean())
df["GioMangXaHoi"] = df["GioMangXaHoi"].fillna(df["GioMangXaHoi"].mean())
df["DiemTB"]       = df["DiemTB"].fillna(df["DiemTB"].mean())
print("\n5. Sau khi điền giá trị thiếu bằng trung bình:")
print(df[["MaSV", "Tuoi", "GioTuHoc", "GioMangXaHoi", "DiemTB"]])

# 6–7. Phát hiện và xử lý dữ liệu bất thường
# df.loc[condition, column] = value: thay giá trị tại các hàng thỏa condition.
# Thay bằng trung bình hợp lý của cột (đã loại bỏ giá trị bất thường).

print("\n6-7. Xử lý dữ liệu bất thường:")

# Tuổi > 30 → bất thường (sinh viên đại học thường 18-25)
print("  - Tuổi > 30:", df[df["Tuoi"] > 30][["MaSV", "Tuoi"]].values)
df.loc[df["Tuoi"] > 30, "Tuoi"] = df["Tuoi"].mean()

# GioTuHoc < 0 → bất thường (giờ không thể âm)
print("  - GioTuHoc < 0:", df[df["GioTuHoc"] < 0][["MaSV", "GioTuHoc"]].values)
df.loc[df["GioTuHoc"] < 0, "GioTuHoc"] = df["GioTuHoc"].mean()

# GioMangXaHoi > 12 → bất thường (1 ngày chỉ có 24h)
print("  - GioMXH > 12:", df[df["GioMangXaHoi"] > 12][["MaSV", "GioMangXaHoi"]].values)
df.loc[df["GioMangXaHoi"] > 12, "GioMangXaHoi"] = df["GioMangXaHoi"].mean()

# DiemTB > 4.0 → bất thường (thang điểm 4.0 tối đa)
print("  - DiemTB > 4.0:", df[df["DiemTB"] > 4.0][["MaSV", "DiemTB"]].values)
df.loc[df["DiemTB"] > 4.0, "DiemTB"] = df["DiemTB"].mean()

# 8. Bộ dữ liệu sạch sau xử lý
print("\n8. Dữ liệu sau khi làm sạch hoàn toàn:")
print(df.to_string(index=False))     # In đẹp, không hiển thị index mặc định

# 9–10. Chuẩn hóa Min-Max và Z-score
cols = ["Tuoi", "GioTuHoc", "GioMangXaHoi", "DiemTB"]  # Các cột cần chuẩn hóa

# --- Min-Max Normalization ---
# Đưa dữ liệu về khoảng [0, 1]
# Công thức: x_norm = (x - x_min) / (x_max - x_min)
df_minmax = df.copy()               # Tạo bản sao để không thay đổi df gốc
for col in cols:
    col_min = df[col].min()         # Giá trị nhỏ nhất của cột
    col_max = df[col].max()         # Giá trị lớn nhất của cột
    df_minmax[col] = (df[col] - col_min) / (col_max - col_min)  # Công thức Min-Max

# --- Z-score Standardization ---
# Chuẩn hóa về phân phối chuẩn (TB=0, std=1)
# Công thức: z = (x - mean) / std
df_zscore = df.copy()               # Tạo bản sao khác
for col in cols:
    col_mean = df[col].mean()       # Trung bình của cột
    col_std  = df[col].std()        # Độ lệch chuẩn của cột
    df_zscore[col] = (df[col] - col_mean) / col_std  # Công thức Z-score

print("\n9. Dữ liệu sau chuẩn hóa Min-Max [0,1]:")
print(df_minmax[cols].round(4).to_string(index=False))

print("\n10. Dữ liệu sau chuẩn hóa Z-score:")
print(df_zscore[cols].round(4).to_string(index=False))

# 11. So sánh và nhận xét
print("""
11. [Nhận xét So sánh Trước và Sau Chuẩn Hóa]
──────────────────────────────────────────────
• Trước chuẩn hóa: các biến có đơn vị và thang đo khác nhau
  (Tuoi: 19-22, GioTuHoc: 2-10, DiemTB: 2-3.8), khó so sánh trực tiếp.

• Sau Min-Max [0,1]: tất cả giá trị nằm trong [0,1].
  Phù hợp khi thuật toán cần khoảng giá trị xác định (ví dụ: neural network).
  Nhược điểm: nhạy cảm với outlier (1 điểm cực trị kéo cả cột).

• Sau Z-score: trung bình ≈ 0, độ lệch chuẩn = 1.
  Phù hợp khi dữ liệu có phân phối chuẩn, dùng cho PCA, hồi quy, clustering.
  Ít bị ảnh hưởng bởi outlier hơn Min-Max.

• Khi nào dùng Min-Max: khi biết rõ khoảng giá trị hợp lệ & không có nhiều outlier.
• Khi nào dùng Z-score: khi so sánh các biến có phân phối chuẩn, hoặc trước PCA/SVM.
""")

print("=" * 60)
print(" HOÀN THÀNH TẤT CẢ 6 BÀI THỰC HÀNH NUMPY NÂNG CAO")
print("=" * 60)
