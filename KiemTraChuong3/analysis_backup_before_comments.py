# ============================================================
# PHÂN TÍCH CHẤT LƯỢNG HỌC TẬP SINH VIÊN
# Dataset: students_cleaned_final.csv
# ============================================================

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- Cấu hình font & style ---
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'

# Palette màu nhất quán
COLOR_CITY   = ['#4C72B0', '#DD8452', '#55A868']
COLOR_CLASS  = ['#C44E52', '#8172B2', '#64B5CD']
COLOR_GRADE  = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']

# ============================================================
# PHẦN 1: KIỂM TRA & HIỂU DỮ LIỆU (10%)
# ============================================================
print("=" * 60)
print("PHẦN 1: KIỂM TRA & HIỂU DỮ LIỆU")
print("=" * 60)

# Đọc dữ liệu
df = pd.read_csv('students_cleaned_final.csv')

# Tạo cột Grade từ cột Total (chưa có trong dataset)
def assign_grade(total):
    if total >= 9:
        return 'Giỏi'
    elif total >= 8:
        return 'Khá'
    elif total >= 6.5:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Grade'] = df['Total'].apply(assign_grade)

# Thông tin cơ bản
print(f"\n Shape: {df.shape[0]} dòng × {df.shape[1]} cột")
print(f"\nCác cột: {df.columns.tolist()}")

print("\n--- df.info() ---")
df.info()

print("\n--- Missing values ---")
missing = df.isnull().sum()
print(missing)
print(f"→ Tổng missing: {missing.sum()} giá trị")

print("\n--- Thống kê mô tả ---")
print(df.describe().round(2))

# Nhận xét dữ liệu
print("\n Nhận xét:")
print("  - Không có missing values.")
print("  - Có bất thường: City = 'UNKNOWN' (1 sinh viên).")
print("  - Total có giá trị max = 11 (vượt thang 10 do Bonus).")
print("  - Có dữ liệu trùng lặp: Name='An' xuất hiện 3 lần cùng Score/Age.")


# ============================================================
# PHẦN 2: PHÂN TÍCH TỔNG QUAN (15%)
# ============================================================
print("\n" + "=" * 60)
print("PHẦN 2: PHÂN TÍCH TỔNG QUAN")
print("=" * 60)

# Thống kê số lượng sinh viên theo City & Class
count_city  = df['City'].value_counts()
count_class = df['Class'].value_counts()

print(f"\nSố sinh viên theo thành phố:\n{count_city}")
print(f"\nSố sinh viên theo lớp:\n{count_class}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart - City
axes[0].bar(count_city.index, count_city.values, color=COLOR_CITY, edgecolor='white', linewidth=1.2)
axes[0].set_title('Số lượng sinh viên theo Thành phố')
axes[0].set_xlabel('Thành phố')
axes[0].set_ylabel('Số sinh viên')
for i, v in enumerate(count_city.values):
    axes[0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

# Bar chart - Class
axes[1].bar(count_class.index, count_class.values, color=COLOR_CLASS, edgecolor='white', linewidth=1.2)
axes[1].set_title('Số lượng sinh viên theo Lớp')
axes[1].set_xlabel('Lớp')
axes[1].set_ylabel('Số sinh viên')
for i, v in enumerate(count_class.values):
    axes[1].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

plt.suptitle('PHẦN 2: Phân tích tổng quan sinh viên', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('p2_tong_quan.png', dpi=150, bbox_inches='tight')
plt.close()
print(" Đã lưu: p2_tong_quan.png")

print("\n Nhận xét:")
print(f"  - Thành phố nhiều sinh viên nhất: {count_city.idxmax()} ({count_city.max()} SV)")
print("  - Phân bố lớp tương đối cân bằng (KTPM1: 4, KTPM2: 4, KTPM3: 3 - gần bằng nhau).")
print("  - Có 1 SV thuộc City='UNKNOWN' → cần làm sạch thêm.")


# ============================================================
# PHẦN 3: PHÂN TÍCH ĐIỂM SỐ (15%)
# ============================================================
print("\n" + "=" * 60)
print("PHẦN 3: PHÂN TÍCH ĐIỂM SỐ")
print("=" * 60)

print(f"\nScore - Mean: {df['Score'].mean():.2f} | Median: {df['Score'].median():.2f}")
print(f"Score - Min: {df['Score'].min()} | Max: {df['Score'].max()}")

fig, ax = plt.subplots(figsize=(8, 5))

# Histogram điểm Score
n, bins, patches = ax.hist(df['Score'], bins=6, color='#4C72B0', edgecolor='white',
                           linewidth=1.2, alpha=0.85)
ax.axvline(df['Score'].mean(),   color='#e74c3c', linestyle='--', linewidth=1.8, label=f"Mean: {df['Score'].mean():.2f}")
ax.axvline(df['Score'].median(), color='#2ecc71', linestyle='--', linewidth=1.8, label=f"Median: {df['Score'].median():.2f}")

ax.set_title('Phân bố điểm Score của sinh viên')
ax.set_xlabel('Điểm Score')
ax.set_ylabel('Số sinh viên')
ax.legend()
plt.tight_layout()
plt.savefig('p3_histogram_score.png', dpi=150, bbox_inches='tight')
plt.close()
print(" Đã lưu: p3_histogram_score.png")

print("\n Nhận xét:")
print("  - Điểm tập trung chủ yếu từ 8 – 9 (vùng khá - giỏi).")
print("  - Có 1 sinh viên điểm thấp (5.5) → cần chú ý hỗ trợ.")
print("  - Mean ≈ Median → phân phối tương đối đối xứng.")


# ============================================================
# PHẦN 4: SO SÁNH NHÓM (15%)
# ============================================================
print("\n" + "=" * 60)
print("PHẦN 4: SO SÁNH NHÓM")
print("=" * 60)

mean_score_city  = df.groupby('City')['Score'].mean().sort_values(ascending=False)
mean_total_class = df.groupby('Class')['Total'].mean().sort_values(ascending=False)

print(f"\nMean Score theo City:\n{mean_score_city.round(2)}")
print(f"\nMean Total theo Class:\n{mean_total_class.round(2)}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart - Mean Score theo City
bars1 = axes[0].bar(mean_score_city.index, mean_score_city.values,
                    color=COLOR_CITY[:len(mean_score_city)], edgecolor='white')
axes[0].set_title('Mean Score theo Thành phố')
axes[0].set_xlabel('Thành phố')
axes[0].set_ylabel('Điểm trung bình')
axes[0].set_ylim(0, 11)
for bar, val in zip(bars1, mean_score_city.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f'{val:.2f}', ha='center', fontweight='bold')

# Bar chart - Mean Total theo Class
bars2 = axes[1].bar(mean_total_class.index, mean_total_class.values,
                    color=COLOR_CLASS[:len(mean_total_class)], edgecolor='white')
axes[1].set_title('Mean Total theo Lớp')
axes[1].set_xlabel('Lớp')
axes[1].set_ylabel('Tổng điểm trung bình')
axes[1].set_ylim(0, 13)
for bar, val in zip(bars2, mean_total_class.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f'{val:.2f}', ha='center', fontweight='bold')

plt.suptitle('PHẦN 4: So sánh nhóm', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('p4_so_sanh_nhom.png', dpi=150, bbox_inches='tight')
plt.close()
print(" Đã lưu: p4_so_sanh_nhom.png")

print("\n💡 Nhận xét:")
print(f"  - Thành phố học tốt nhất: {mean_score_city.idxmax()} (Mean Score = {mean_score_city.max():.2f})")
print(f"  - Lớp hiệu quả nhất: {mean_total_class.idxmax()} (Mean Total = {mean_total_class.max():.2f})")


# ============================================================
# PHẦN 5: PHÂN TÍCH MỐI QUAN HỆ (15%)
# ============================================================
print("\n" + "=" * 60)
print("PHẦN 5: PHÂN TÍCH MỐI QUAN HỆ")
print("=" * 60)

corr_age_score = df['Age'].corr(df['Score'])
print(f"\nHệ số tương quan Age & Score: {corr_age_score:.3f}")

fig, ax = plt.subplots(figsize=(8, 5))

# Màu theo City
city_colors = {'HCM': '#4C72B0', 'HN': '#DD8452', 'UNKNOWN': '#55A868'}
for city, group in df.groupby('City'):
    ax.scatter(group['Age'], group['Score'], label=city, s=90,
               color=city_colors.get(city, 'gray'), edgecolors='white', linewidth=0.8, alpha=0.85)

# Đường trend line
z = np.polyfit(df['Age'], df['Score'], 1)
p = np.poly1d(z)
age_range = np.linspace(df['Age'].min(), df['Age'].max(), 100)
ax.plot(age_range, p(age_range), '--', color='#e74c3c', linewidth=1.5, label=f'Trend (r={corr_age_score:.2f})')

ax.set_title('Mối quan hệ giữa Tuổi (Age) và Điểm (Score)')
ax.set_xlabel('Tuổi (Age)')
ax.set_ylabel('Điểm Score')
ax.legend()
plt.tight_layout()
plt.savefig('p5_scatter_age_score.png', dpi=150, bbox_inches='tight')
plt.close()
print(" Đã lưu: p5_scatter_age_score.png")

print("\n Nhận xét:")
print(f"  - Hệ số tương quan r = {corr_age_score:.2f} → mối quan hệ yếu.")
print("  - Tuổi KHÔNG ảnh hưởng rõ rệt đến kết quả học tập.")
print("  - Cả nhóm 20 tuổi lẫn 22 tuổi đều có điểm cao và thấp.")


# ============================================================
# PHẦN 6: PHÂN TÍCH HỌC LỰC (10%)
# ============================================================
print("\n" + "=" * 60)
print("PHẦN 6: PHÂN TÍCH HỌC LỰC")
print("=" * 60)

# Đảm bảo thứ tự Grade hợp lý
grade_order = ['Giỏi', 'Khá', 'Trung bình', 'Yếu']
count_grade = df['Grade'].value_counts().reindex(grade_order, fill_value=0)
print(f"\nPhân bố học lực:\n{count_grade}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar chart
axes[0].bar(count_grade.index, count_grade.values,
            color=COLOR_GRADE, edgecolor='white', linewidth=1.2)
axes[0].set_title('Phân bố học lực (Bar Chart)')
axes[0].set_xlabel('Học lực')
axes[0].set_ylabel('Số sinh viên')
for i, v in enumerate(count_grade.values):
    if v > 0:
        axes[0].text(i, v + 0.05, str(v), ha='center', fontweight='bold')

# Pie chart
wedges, texts, autotexts = axes[1].pie(
    count_grade[count_grade > 0],
    labels=count_grade[count_grade > 0].index,
    colors=[COLOR_GRADE[i] for i, v in enumerate(count_grade) if v > 0],
    autopct='%1.0f%%', startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
)
for at in autotexts:
    at.set_fontweight('bold')
axes[1].set_title('Phân bố học lực (Pie Chart)')

plt.suptitle('PHẦN 6: Phân bố học lực sinh viên', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('p6_hoc_luc.png', dpi=150, bbox_inches='tight')
plt.close()
print(" Đã lưu: p6_hoc_luc.png")

print("\n Nhận xét:")
print(f"  - Học lực Khá chiếm tỷ lệ cao nhất ({count_grade['Khá']} SV).")
print(f"  - Có {count_grade['Yếu']} SV xếp loại Yếu → cần theo dõi đặc biệt.")
print("  - Phân bố nghiêng về phía tích cực (Giỏi + Khá chiếm đa số).")


# ============================================================
# PHẦN 7: PHÂN TÍCH NÂNG CAO (10%)
# ============================================================
print("\n" + "=" * 60)
print("PHẦN 7: PHÂN TÍCH NÂNG CAO")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# --- 7.1 Boxplot Score theo City ---
cities = df['City'].unique()
data_box = [df[df['City'] == c]['Score'].values for c in cities]
bp = axes[0].boxplot(data_box, labels=cities, patch_artist=True, notch=False,
                     medianprops={'color': 'black', 'linewidth': 2})
for patch, color in zip(bp['boxes'], COLOR_CITY[:len(cities)]):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
axes[0].set_title('Boxplot Score theo City')
axes[0].set_xlabel('Thành phố')
axes[0].set_ylabel('Điểm Score')

# --- 7.2 Correlation heatmap ---
corr_cols = ['Age', 'Score', 'Bonus', 'Total']
corr_matrix = df[corr_cols].corr()
print(f"\nMa trận tương quan:\n{corr_matrix.round(2)}")

im = axes[1].imshow(corr_matrix, cmap='RdYlGn', vmin=-1, vmax=1)
axes[1].set_xticks(range(len(corr_cols)))
axes[1].set_yticks(range(len(corr_cols)))
axes[1].set_xticklabels(corr_cols, rotation=30)
axes[1].set_yticklabels(corr_cols)
axes[1].set_title('Correlation Matrix')
for i in range(len(corr_cols)):
    for j in range(len(corr_cols)):
        axes[1].text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                     ha='center', va='center', fontweight='bold',
                     color='black' if abs(corr_matrix.iloc[i, j]) < 0.7 else 'white')
plt.colorbar(im, ax=axes[1])

# --- 7.3 Top 5 sinh viên ---
top5 = df.nlargest(5, 'Total')[['Name', 'Class', 'City', 'Score', 'Total']].reset_index(drop=True)
print(f"\nTop 5 sinh viên điểm cao nhất:\n{top5}")

bars = axes[2].barh(top5['Name'] + ' (' + top5['Class'] + ')',
                    top5['Total'], color='#4C72B0', edgecolor='white')
axes[2].set_title('Top 5 Sinh viên điểm cao nhất')
axes[2].set_xlabel('Tổng điểm (Total)')
axes[2].set_xlim(0, 13)
for bar, val in zip(bars, top5['Total']):
    axes[2].text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                 f'{val}', va='center', fontweight='bold')

plt.suptitle('PHẦN 7: Phân tích nâng cao', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('p7_nang_cao.png', dpi=150, bbox_inches='tight')
plt.close()
print(" Đã lưu: p7_nang_cao.png")

print("\n💡 Nhận xét phần 7:")
print("  - Boxplot: HCM có dải điểm rộng hơn; UNKNOWN chỉ có 1 SV nên không đại diện.")
print("  - Tương quan Score-Total rất cao → Bonus đóng vai trò nhỏ nhưng có ý nghĩa.")
print("  - Top 5 dẫn đầu đều từ KTPM1 và KTPM3.")
print("  - Phát hiện bất thường: 'An' xuất hiện 3 lần với cùng Score/Age → dữ liệu trùng.")


# ============================================================
# PHẦN 8: DATA STORYTELLING (10%)
# ============================================================
print("\n" + "=" * 60)
print("PHẦN 8: DATA STORYTELLING – BÁO CÁO TỔNG KẾT")
print("=" * 60)

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
print(story)

print("\n HOÀN THÀNH! Các file biểu đồ đã lưu:")
print("   - p2_tong_quan.png")
print("   - p3_histogram_score.png")
print("   - p4_so_sanh_nhom.png")
print("   - p5_scatter_age_score.png")
print("   - p6_hoc_luc.png")
print("   - p7_nang_cao.png")