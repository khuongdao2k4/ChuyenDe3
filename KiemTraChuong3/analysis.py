# ============================================================
# PHÂN TÍCH CHẤT LƯỢNG HỌC TẬP SINH VIÊN
# Dataset: students_cleaned_final.csv
# ============================================================

# Import thu vien `pandas` de su dung trong chuong trinh.
import pandas as pd
# Import thu vien `matplotlib` de su dung trong chuong trinh.
import matplotlib
# Dat backend `Agg` de ve va luu hinh khong can giao dien do hoa.
matplotlib.use('Agg')
# Import thu vien `matplotlib.pyplot` de su dung trong chuong trinh.
import matplotlib.pyplot as plt
# Import thu vien `matplotlib.patches` de su dung trong chuong trinh.
import matplotlib.patches as mpatches
# Import thu vien `numpy` de su dung trong chuong trinh.
import numpy as np

# --- Cấu hình font & style ---
# Dat cau hinh hien thi mac dinh cho toan bo bieu do.
plt.rcParams['figure.figsize'] = (8, 5)
# Dat cau hinh hien thi mac dinh cho toan bo bieu do.
plt.rcParams['axes.titlesize'] = 14
# Dat cau hinh hien thi mac dinh cho toan bo bieu do.
plt.rcParams['axes.labelsize'] = 12
# Dat cau hinh hien thi mac dinh cho toan bo bieu do.
plt.rcParams['axes.titleweight'] = 'bold'

# Palette màu nhất quán
# Khai bao bang mau dung lai o nhieu bieu do de giu nhat quan.
COLOR_CITY   = ['#4C72B0', '#DD8452', '#55A868']
# Khai bao bang mau dung lai o nhieu bieu do de giu nhat quan.
COLOR_CLASS  = ['#C44E52', '#8172B2', '#64B5CD']
# Khai bao bang mau dung lai o nhieu bieu do de giu nhat quan.
COLOR_GRADE  = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']

# ============================================================
# PHẦN 1: KIỂM TRA & HIỂU DỮ LIỆU (10%)
# ============================================================
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("PHẦN 1: KIỂM TRA & HIỂU DỮ LIỆU")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)

# Đọc dữ liệu
# Doc file CSV vao DataFrame `df` de bat dau phan tich.
df = pd.read_csv('students_cleaned_final.csv')

# Tạo cột Grade từ cột Total (chưa có trong dataset)
# Dinh nghia ham `assign_grade` de tai su dung logic phan loai.
def assign_grade(total):
    # Kiem tra dieu kien `if` va xu ly nhanh dau tien dung.
    if total >= 9:
        # Tra ket qua tu ham hien tai cho noi goi ham.
        return 'Giỏi'
    # Kiem tra them mot nhanh dieu kien `elif` neu nhanh truoc khong dung.
    elif total >= 8:
        # Tra ket qua tu ham hien tai cho noi goi ham.
        return 'Khá'
    # Kiem tra them mot nhanh dieu kien `elif` neu nhanh truoc khong dung.
    elif total >= 6.5:
        # Tra ket qua tu ham hien tai cho noi goi ham.
        return 'Trung bình'
    # Xu ly nhanh mac dinh khi cac dieu kien tren deu sai.
    else:
        # Tra ket qua tu ham hien tai cho noi goi ham.
        return 'Yếu'

# Tao/cap nhat cot moi bang cach ap dung ham len tung gia tri.
df['Grade'] = df['Total'].apply(assign_grade)

# Thông tin cơ bản
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\n Shape: {df.shape[0]} dòng × {df.shape[1]} cột")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nCác cột: {df.columns.tolist()}")

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n--- df.info() ---")
# Goi ham/phuong thuc de xu ly du lieu hoac tao bieu do.
df.info()

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n--- Missing values ---")
# Tinh so gia tri thieu cua tung cot trong DataFrame.
missing = df.isnull().sum()
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(missing)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"→ Tổng missing: {missing.sum()} giá trị")

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n--- Thống kê mô tả ---")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(df.describe().round(2))

# Nhận xét dữ liệu
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n Nhận xét:")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Không có missing values.")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Có bất thường: City = 'UNKNOWN' (1 sinh viên).")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Total có giá trị max = 11 (vượt thang 10 do Bonus).")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Có dữ liệu trùng lặp: Name='An' xuất hiện 3 lần cùng Score/Age.")


# ============================================================
# PHẦN 2: PHÂN TÍCH TỔNG QUAN (15%)
# ============================================================
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n" + "=" * 60)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("PHẦN 2: PHÂN TÍCH TỔNG QUAN")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)

# Thống kê số lượng sinh viên theo City & Class
# Dem so luong ban ghi theo nhom de phuc vu thong ke tong quan.
count_city  = df['City'].value_counts()
# Dem so luong ban ghi theo nhom de phuc vu thong ke tong quan.
count_class = df['Class'].value_counts()

# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nSố sinh viên theo thành phố:\n{count_city}")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nSố sinh viên theo lớp:\n{count_class}")

# Tao figure va mot hoac nhieu truc ve de ve bieu do.
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart - City
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].bar(count_city.index, count_city.values, color=COLOR_CITY, edgecolor='white', linewidth=1.2)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_title('Số lượng sinh viên theo Thành phố')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_xlabel('Thành phố')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_ylabel('Số sinh viên')
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for i, v in enumerate(count_city.values):
    # Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
    axes[0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

# Bar chart - Class
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].bar(count_class.index, count_class.values, color=COLOR_CLASS, edgecolor='white', linewidth=1.2)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_title('Số lượng sinh viên theo Lớp')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_xlabel('Lớp')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_ylabel('Số sinh viên')
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for i, v in enumerate(count_class.values):
    # Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
    axes[1].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

# Dat tieu de tong cho toan bo figure.
plt.suptitle('PHẦN 2: Phân tích tổng quan sinh viên', fontsize=15, fontweight='bold', y=1.02)
# Tu dong can chinh khoang cach de tranh chong lap chu/nhan.
plt.tight_layout()
# Luu bieu do hien tai thanh file anh de nop bao cao.
plt.savefig('p2_tong_quan.png', dpi=150, bbox_inches='tight')
# Dong figure hien tai de giai phong bo nho.
plt.close()
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(" Đã lưu: p2_tong_quan.png")

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n Nhận xét:")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"  - Thành phố nhiều sinh viên nhất: {count_city.idxmax()} ({count_city.max()} SV)")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Phân bố lớp tương đối cân bằng (KTPM1: 4, KTPM2: 4, KTPM3: 3 - gần bằng nhau).")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Có 1 SV thuộc City='UNKNOWN' → cần làm sạch thêm.")


# ============================================================
# PHẦN 3: PHÂN TÍCH ĐIỂM SỐ (15%)
# ============================================================
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n" + "=" * 60)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("PHẦN 3: PHÂN TÍCH ĐIỂM SỐ")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)

# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nScore - Mean: {df['Score'].mean():.2f} | Median: {df['Score'].median():.2f}")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"Score - Min: {df['Score'].min()} | Max: {df['Score'].max()}")

# Tao figure va mot hoac nhieu truc ve de ve bieu do.
fig, ax = plt.subplots(figsize=(8, 5))

# Histogram điểm Score
# Ve histogram va lay thong tin bin/patch de tuong tac khi can.
n, bins, patches = ax.hist(df['Score'], bins=6, color='#4C72B0', edgecolor='white',
                           # Truyen gia tri cho tham so `linewidth` trong loi goi ham.
                           linewidth=1.2, alpha=0.85)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.axvline(df['Score'].mean(),   color='#e74c3c', linestyle='--', linewidth=1.8, label=f"Mean: {df['Score'].mean():.2f}")
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.axvline(df['Score'].median(), color='#2ecc71', linestyle='--', linewidth=1.8, label=f"Median: {df['Score'].median():.2f}")

# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.set_title('Phân bố điểm Score của sinh viên')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.set_xlabel('Điểm Score')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.set_ylabel('Số sinh viên')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.legend()
# Tu dong can chinh khoang cach de tranh chong lap chu/nhan.
plt.tight_layout()
# Luu bieu do hien tai thanh file anh de nop bao cao.
plt.savefig('p3_histogram_score.png', dpi=150, bbox_inches='tight')
# Dong figure hien tai de giai phong bo nho.
plt.close()
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(" Đã lưu: p3_histogram_score.png")

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n Nhận xét:")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Điểm tập trung chủ yếu từ 8 – 9 (vùng khá - giỏi).")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Có 1 sinh viên điểm thấp (5.5) → cần chú ý hỗ trợ.")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Mean ≈ Median → phân phối tương đối đối xứng.")


# ============================================================
# PHẦN 4: SO SÁNH NHÓM (15%)
# ============================================================
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n" + "=" * 60)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("PHẦN 4: SO SÁNH NHÓM")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)

# Tinh diem trung binh theo nhom de so sanh giua cac doi tuong.
mean_score_city  = df.groupby('City')['Score'].mean().sort_values(ascending=False)
# Tinh diem trung binh theo nhom de so sanh giua cac doi tuong.
mean_total_class = df.groupby('Class')['Total'].mean().sort_values(ascending=False)

# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nMean Score theo City:\n{mean_score_city.round(2)}")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nMean Total theo Class:\n{mean_total_class.round(2)}")

# Tao figure va mot hoac nhieu truc ve de ve bieu do.
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart - Mean Score theo City
# Tao doi tuong cot de co the gan nhan gia tri len tung cot.
bars1 = axes[0].bar(mean_score_city.index, mean_score_city.values,
                    # Truyen gia tri cho tham so `color` trong loi goi ham.
                    color=COLOR_CITY[:len(mean_score_city)], edgecolor='white')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_title('Mean Score theo Thành phố')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_xlabel('Thành phố')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_ylabel('Điểm trung bình')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_ylim(0, 11)
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for bar, val in zip(bars1, mean_score_city.values):
    # Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 # Truyen gia tri cho tham so `ha` trong loi goi ham.
                 f'{val:.2f}', ha='center', fontweight='bold')

# Bar chart - Mean Total theo Class
# Tao doi tuong cot de co the gan nhan gia tri len tung cot.
bars2 = axes[1].bar(mean_total_class.index, mean_total_class.values,
                    # Truyen gia tri cho tham so `color` trong loi goi ham.
                    color=COLOR_CLASS[:len(mean_total_class)], edgecolor='white')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_title('Mean Total theo Lớp')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_xlabel('Lớp')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_ylabel('Tổng điểm trung bình')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_ylim(0, 13)
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for bar, val in zip(bars2, mean_total_class.values):
    # Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 # Truyen gia tri cho tham so `ha` trong loi goi ham.
                 f'{val:.2f}', ha='center', fontweight='bold')

# Dat tieu de tong cho toan bo figure.
plt.suptitle('PHẦN 4: So sánh nhóm', fontsize=15, fontweight='bold', y=1.02)
# Tu dong can chinh khoang cach de tranh chong lap chu/nhan.
plt.tight_layout()
# Luu bieu do hien tai thanh file anh de nop bao cao.
plt.savefig('p4_so_sanh_nhom.png', dpi=150, bbox_inches='tight')
# Dong figure hien tai de giai phong bo nho.
plt.close()
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(" Đã lưu: p4_so_sanh_nhom.png")

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n Nhận xét:")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"  - Thành phố học tốt nhất: {mean_score_city.idxmax()} (Mean Score = {mean_score_city.max():.2f})")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"  - Lớp hiệu quả nhất: {mean_total_class.idxmax()} (Mean Total = {mean_total_class.max():.2f})")


# ============================================================
# PHẦN 5: PHÂN TÍCH MỐI QUAN HỆ (15%)
# ============================================================
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n" + "=" * 60)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("PHẦN 5: PHÂN TÍCH MỐI QUAN HỆ")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)

# Tinh he so tuong quan giua tuoi va diem Score.
corr_age_score = df['Age'].corr(df['Score'])
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nHệ số tương quan Age & Score: {corr_age_score:.3f}")

# Tao figure va mot hoac nhieu truc ve de ve bieu do.
fig, ax = plt.subplots(figsize=(8, 5))

# Màu theo City
# Khai bao bang mau cho tung thanh pho de ve scatter de nhin.
city_colors = {'HCM': '#4C72B0', 'HN': '#DD8452', 'UNKNOWN': '#55A868'}
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for city, group in df.groupby('City'):
    # Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
    ax.scatter(group['Age'], group['Score'], label=city, s=90,
               # Truyen gia tri cho tham so `color` trong loi goi ham.
               color=city_colors.get(city, 'gray'), edgecolors='white', linewidth=0.8, alpha=0.85)

# Đường trend line
# Fit duong thang hoi quy bac 1 cho cap du lieu Age-Score.
z = np.polyfit(df['Age'], df['Score'], 1)
# Chuyen he so hoi quy thanh ham da thuc de de tinh gia tri du doan.
p = np.poly1d(z)
# Tao day tuoi lien tuc de ve duong trend line muot hon.
age_range = np.linspace(df['Age'].min(), df['Age'].max(), 100)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.plot(age_range, p(age_range), '--', color='#e74c3c', linewidth=1.5, label=f'Trend (r={corr_age_score:.2f})')

# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.set_title('Mối quan hệ giữa Tuổi (Age) và Điểm (Score)')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.set_xlabel('Tuổi (Age)')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.set_ylabel('Điểm Score')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
ax.legend()
# Tu dong can chinh khoang cach de tranh chong lap chu/nhan.
plt.tight_layout()
# Luu bieu do hien tai thanh file anh de nop bao cao.
plt.savefig('p5_scatter_age_score.png', dpi=150, bbox_inches='tight')
# Dong figure hien tai de giai phong bo nho.
plt.close()
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(" Đã lưu: p5_scatter_age_score.png")

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n Nhận xét:")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"  - Hệ số tương quan r = {corr_age_score:.2f} → mối quan hệ yếu.")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Tuổi KHÔNG ảnh hưởng rõ rệt đến kết quả học tập.")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Cả nhóm 20 tuổi lẫn 22 tuổi đều có điểm cao và thấp.")


# ============================================================
# PHẦN 6: PHÂN TÍCH HỌC LỰC (10%)
# ============================================================
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n" + "=" * 60)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("PHẦN 6: PHÂN TÍCH HỌC LỰC")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)

# Đảm bảo thứ tự Grade hợp lý
# Khai bao thu tu hoc luc mong muon khi thong ke/ve bieu do.
grade_order = ['Giỏi', 'Khá', 'Trung bình', 'Yếu']
# Dem so luong sinh vien theo tung muc hoc luc.
count_grade = df['Grade'].value_counts().reindex(grade_order, fill_value=0)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nPhân bố học lực:\n{count_grade}")

# Tao figure va mot hoac nhieu truc ve de ve bieu do.
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].bar(count_grade.index, count_grade.values,
            # Truyen gia tri cho tham so `color` trong loi goi ham.
            color=COLOR_GRADE, edgecolor='white', linewidth=1.2)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_title('Phân bố học lực (Bar Chart)')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_xlabel('Học lực')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_ylabel('Số sinh viên')
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for i, v in enumerate(count_grade.values):
    # Kiem tra dieu kien `if` va xu ly nhanh dau tien dung.
    if v > 0:
        # Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
        axes[0].text(i, v + 0.05, str(v), ha='center', fontweight='bold')

# Pie chart
# Ve pie chart va lay ve cac doi tuong text de chinh dinh dang.
wedges, texts, autotexts = axes[1].pie(
    # Dem so luong sinh vien theo tung muc hoc luc.
    count_grade[count_grade > 0],
    # Truyen gia tri cho tham so `labels` trong loi goi ham.
    labels=count_grade[count_grade > 0].index,
    # Truyen gia tri cho tham so `colors` trong loi goi ham.
    colors=[COLOR_GRADE[i] for i, v in enumerate(count_grade) if v > 0],
    # Truyen gia tri cho tham so `autopct` trong loi goi ham.
    autopct='%1.0f%%', startangle=90,
    # Truyen gia tri cho tham so `wedgeprops` trong loi goi ham.
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
# Dong nay dong ngoac cua cau lenh da mo o phia tren.
)
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for at in autotexts:
    # Goi ham/phuong thuc de xu ly du lieu hoac tao bieu do.
    at.set_fontweight('bold')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_title('Phân bố học lực (Pie Chart)')

# Dat tieu de tong cho toan bo figure.
plt.suptitle('PHẦN 6: Phân bố học lực sinh viên', fontsize=15, fontweight='bold', y=1.02)
# Tu dong can chinh khoang cach de tranh chong lap chu/nhan.
plt.tight_layout()
# Luu bieu do hien tai thanh file anh de nop bao cao.
plt.savefig('p6_hoc_luc.png', dpi=150, bbox_inches='tight')
# Dong figure hien tai de giai phong bo nho.
plt.close()
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(" Đã lưu: p6_hoc_luc.png")

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n Nhận xét:")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"  - Học lực Khá chiếm tỷ lệ cao nhất ({count_grade['Khá']} SV).")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"  - Có {count_grade['Yếu']} SV xếp loại Yếu → cần theo dõi đặc biệt.")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Phân bố nghiêng về phía tích cực (Giỏi + Khá chiếm đa số).")


# ============================================================
# PHẦN 7: PHÂN TÍCH NÂNG CAO (10%)
# ============================================================
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n" + "=" * 60)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("PHẦN 7: PHÂN TÍCH NÂNG CAO")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)

# Tao figure va mot hoac nhieu truc ve de ve bieu do.
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# --- 7.1 Boxplot Score theo City ---
# Gan ket qua tinh toan vao bien `cities` de dung cho buoc tiep theo.
cities = df['City'].unique()
# Gan ket qua tinh toan vao bien `data_box` de dung cho buoc tiep theo.
data_box = [df[df['City'] == c]['Score'].values for c in cities]
# Ve boxplot cho tung nhom de so sanh phan bo diem.
bp = axes[0].boxplot(data_box, labels=cities, patch_artist=True, notch=False,
                     # Truyen gia tri cho tham so `medianprops` trong loi goi ham.
                     medianprops={'color': 'black', 'linewidth': 2})
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for patch, color in zip(bp['boxes'], COLOR_CITY[:len(cities)]):
    # Goi ham/phuong thuc de xu ly du lieu hoac tao bieu do.
    patch.set_facecolor(color)
    # Goi ham/phuong thuc de xu ly du lieu hoac tao bieu do.
    patch.set_alpha(0.75)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_title('Boxplot Score theo City')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_xlabel('Thành phố')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[0].set_ylabel('Điểm Score')

# --- 7.2 Correlation heatmap ---
# Chon cac cot so de tinh ma tran tuong quan.
corr_cols = ['Age', 'Score', 'Bonus', 'Total']
# Tinh ma tran tuong quan giua cac cot da chon.
corr_matrix = df[corr_cols].corr()
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nMa trận tương quan:\n{corr_matrix.round(2)}")

# Ve heatmap tu ma tran tuong quan.
im = axes[1].imshow(corr_matrix, cmap='RdYlGn', vmin=-1, vmax=1)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_xticks(range(len(corr_cols)))
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_yticks(range(len(corr_cols)))
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_xticklabels(corr_cols, rotation=30)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_yticklabels(corr_cols)
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[1].set_title('Correlation Matrix')
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for i in range(len(corr_cols)):
    # Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
    for j in range(len(corr_cols)):
        # Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
        axes[1].text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                     # Truyen gia tri cho tham so `ha` trong loi goi ham.
                     ha='center', va='center', fontweight='bold',
                     # Truyen gia tri cho tham so `color` trong loi goi ham.
                     color='black' if abs(corr_matrix.iloc[i, j]) < 0.7 else 'white')
# Goi ham cua matplotlib de cau hinh hoac hien thi bieu do.
plt.colorbar(im, ax=axes[1])

# --- 7.3 Top 5 sinh viên ---
# Lay 5 sinh vien co tong diem cao nhat de trinh bay.
top5 = df.nlargest(5, 'Total')[['Name', 'Class', 'City', 'Score', 'Total']].reset_index(drop=True)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(f"\nTop 5 sinh viên điểm cao nhất:\n{top5}")

# Tao doi tuong cot de co the gan nhan gia tri len tung cot.
bars = axes[2].barh(top5['Name'] + ' (' + top5['Class'] + ')',
                    # Truyen gia tri cho tham so `color` trong loi goi ham.
                    top5['Total'], color='#4C72B0', edgecolor='white')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[2].set_title('Top 5 Sinh viên điểm cao nhất')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[2].set_xlabel('Tổng điểm (Total)')
# Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
axes[2].set_xlim(0, 13)
# Lap qua tung phan tu de ve nhan, xu ly, hoac in ket qua.
for bar, val in zip(bars, top5['Total']):
    # Thuc hien thao tac ve/gan nhan/gan tieu de tren truc bieu do.
    axes[2].text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                 # Truyen gia tri cho tham so `va` trong loi goi ham.
                 f'{val}', va='center', fontweight='bold')

# Dat tieu de tong cho toan bo figure.
plt.suptitle('PHẦN 7: Phân tích nâng cao', fontsize=15, fontweight='bold', y=1.02)
# Tu dong can chinh khoang cach de tranh chong lap chu/nhan.
plt.tight_layout()
# Luu bieu do hien tai thanh file anh de nop bao cao.
plt.savefig('p7_nang_cao.png', dpi=150, bbox_inches='tight')
# Dong figure hien tai de giai phong bo nho.
plt.close()
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(" Đã lưu: p7_nang_cao.png")

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n Nhận xét phần 7:")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Boxplot: HCM có dải điểm rộng hơn; UNKNOWN chỉ có 1 SV nên không đại diện.")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Tương quan Score-Total rất cao → Bonus đóng vai trò nhỏ nhưng có ý nghĩa.")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Top 5 dẫn đầu đều từ KTPM1 và KTPM3.")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("  - Phát hiện bất thường: 'An' xuất hiện 3 lần với cùng Score/Age → dữ liệu trùng.")


# ============================================================
# PHẦN 8: DATA STORYTELLING (10%)
# ============================================================
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n" + "=" * 60)
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("PHẦN 8: DATA STORYTELLING – BÁO CÁO TỔNG KẾT")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("=" * 60)

# Khai bao chuoi bao cao tong ket de in ra cuoi chuong trinh.
story = """
╔══════════════════════════════════════════════════════════╗
║         BÁO CÁO PHÂN TÍCH CHẤT LƯỢNG HỌC TẬP             ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1. TỔNG QUAN                                            ║
║     Dữ liệu gồm 12 sinh viên, 3 lớp (KTPM1–3), đến       ║
║     từ HCM, HN và 1 trường hợp UNKNOWN.                  ║
║     Điểm trung bình Score = 8.0 → chất lượng khá.        ║
║                                                          ║
║  2. NHÓM NỔI BẬT                                         ║
║     • HCM có nhiều SV nhất (6 SV) & Mean Score cao.      ║
║     • KTPM3 đạt Mean Total cao nhất → lớp hiệu quả nhất. ║
║     • Top điểm: Hoa & Fuong (KTPM3, HCM) – Total ≥ 11.   ║
║                                                          ║
║  3. VẤN ĐỀ TỒN TẠI                                       ║
║     • 1 SV điểm Yếu (Lan, Total=5.5) cần hỗ trợ gấp.     ║
║     • Tên 'An' trùng 3 lần → nghi ngờ lỗi nhập liệu.     ║
║     • City='UNKNOWN' cần xác minh & làm sạch.            ║
║     • Tập dữ liệu nhỏ (12 SV) → kết quả chưa đủ đại diện ║
║                                                          ║
║  4. ĐỀ XUẤT CẢI THIỆN                                    ║
║     • Xác minh & loại bỏ dữ liệu trùng lặp (Name='An').  ║
║     • Thu thập thêm dữ liệu (mục tiêu ≥ 100 SV).         ║
║     • Hỗ trợ riêng SV điểm yếu bằng tutoring program.    ║
║     • Nhân rộng mô hình KTPM3 sang các lớp khác.         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
# In thong tin ra man hinh de theo doi ket qua phan tich.
print(story)

# In thong tin ra man hinh de theo doi ket qua phan tich.
print("\n HOÀN THÀNH! Các file biểu đồ đã lưu:")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("   - p2_tong_quan.png")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("   - p3_histogram_score.png")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("   - p4_so_sanh_nhom.png")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("   - p5_scatter_age_score.png")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("   - p6_hoc_luc.png")
# In thong tin ra man hinh de theo doi ket qua phan tich.
print("   - p7_nang_cao.png")