# -*- coding: utf-8 -*-
"""
CHƯƠNG 3: TRỰC QUAN HÓA VÀ PHÂN TÍCH DỮ LIỆU
Các ví dụ code từ Slide 9 trở đi.

Mục tiêu:
- Font hiển thị tiếng Việt có dấu trên biểu đồ.
- Mỗi ví dụ có chú thích rõ đang thuộc slide nào.
- Khi chạy, in rõ yêu cầu của từng slide.
"""

import os
import sys
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from numpy.random import randn

warnings.filterwarnings("ignore")

# Bảo đảm in được tiếng Việt trong terminal.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Cấu hình font ưu tiên cho tiếng Việt có dấu.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "DejaVu Sans",
    "Arial",
    "Tahoma",
    "Noto Sans",
    "Liberation Sans",
]
plt.rcParams["axes.unicode_minus"] = False

# Đường dẫn lưu ảnh (cùng thư mục với script).
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def save(filename: str) -> str:
    """Trả về đường dẫn đầy đủ để lưu ảnh đầu ra."""
    return os.path.join(OUTPUT_DIR, filename)


SLIDE_REQUIREMENTS = [
    ("9", "Import Matplotlib, tạo line plot cơ bản và lưu ảnh."),
    ("13-14", "Tạo figure nhiều vùng (subplots) và vẽ dữ liệu lên một vùng."),
    ("15", "Tùy chỉnh màu sắc, marker, linestyle của biểu đồ đường."),
    ("17-18", "Đặt vạch chia (ticks), nhãn trục và tiêu đề."),
    ("19", "Thêm chú thích (legend) cho nhiều đường dữ liệu."),
    ("20", "Lưu biểu đồ ra nhiều định dạng (SVG, PNG)."),
    ("21-22", "Thiết lập tham số mặc định của Matplotlib (rcParams)."),
    ("28-29", "Vẽ biểu đồ đường doanh số theo tháng."),
    ("30-31", "Tùy chỉnh chi tiết biểu đồ đường với nhiều ví dụ."),
    ("33-34", "Vẽ biểu đồ cột và hiển thị giá trị trên cột."),
    ("35", "Vẽ biểu đồ cột ngang và hiển thị giá trị."),
    ("37-39", "Vẽ histogram phân phối dữ liệu và ghi tần suất."),
    ("42", "Vẽ scatter plot thể hiện quan hệ giữa hai biến."),
    ("45", "Mô phỏng Facet Grid theo nhóm dữ liệu."),
]


def show_slide_header(slide_no: str, requirement: str) -> None:
    """In tiêu đề slide và yêu cầu của slide đó."""
    print(f"\n=== SLIDE {slide_no} ===")
    print(f"Yêu cầu: {requirement}")


def print_all_requirements() -> None:
    """In danh sách yêu cầu của tất cả slide khi bắt đầu chạy."""
    print("\nTỔNG HỢP YÊU CẦU TỪNG SLIDE:")
    for slide_no, requirement in SLIDE_REQUIREMENTS:
        print(f"- Slide {slide_no}: {requirement}")


  
# Slide 9
  
def slide_9_example() -> None:
    """Slide 9: Import Matplotlib và vẽ biểu đồ đường đơn giản."""
    show_slide_header("9", "Import Matplotlib, tạo line plot cơ bản và lưu ảnh.")
    data = np.arange(10)
    print("Dữ liệu:", data)

    plt.figure(figsize=(8, 5))
    plt.plot(data)
    plt.title("Hình 9.1 - Biểu đồ đường cơ bản (Slide 9)")
    plt.xlabel("Chỉ số")
    plt.ylabel("Giá trị")
    plt.grid(True, alpha=0.3)
    plt.savefig(save("slide9_simple_plot.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 13-14
  
def slide_13_14_subplots() -> None:
    """Slide 13-14: Tạo figure và các subplot."""
    show_slide_header("13-14", "Tạo figure nhiều vùng (subplots).")

    fig = plt.figure(figsize=(10, 8))
    fig.add_subplot(2, 2, 1)
    fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    print("Đã tạo 3 vùng biểu đồ trong lưới 2x2.")

    ax3.plot(np.random.randn(50).cumsum(), "k--")
    plt.suptitle("Slide 13-14: Figures và Subplots", fontsize=14)
    plt.savefig(save("slide13_14_subplots.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 15
  
def slide_15_customize_appearance() -> None:
    """Slide 15: Tùy chỉnh hình thức biểu đồ."""
    show_slide_header("15", "Tùy chỉnh màu sắc, marker, linestyle.")

    x = np.arange(10)
    y = np.random.randn(10).cumsum()
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    axes[0].plot(x, y, color="red", linewidth=2, label="Màu đỏ")
    axes[0].set_title("Tùy chỉnh màu sắc")
    axes[0].legend()

    axes[1].plot(x, y, marker="o", markersize=6, color="blue", label="Marker tròn")
    axes[1].set_title("Tùy chỉnh marker")
    axes[1].legend()

    axes[2].plot(x, y, linestyle="--", color="green", linewidth=2, label="Nét đứt")
    axes[2].set_title("Tùy chỉnh linestyle")
    axes[2].legend()

    plt.suptitle("Slide 15: Tùy chỉnh hình thức biểu đồ", fontsize=14)
    plt.tight_layout()
    plt.savefig(save("slide15_customize.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 17-18
  
def slide_17_18_ticks_labels() -> None:
    """Slide 17-18: Vạch chia, nhãn trục, tiêu đề."""
    show_slide_header("17-18", "Đặt ticks, nhãn trục và tiêu đề.")

    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(np.random.randn(1000).cumsum())

    ax.set_xticks([0, 250, 500, 750, 1000])
    ax.set_xticklabels(["Mốc 1", "Mốc 2", "Mốc 3", "Mốc 4", "Mốc 5"], rotation=30)
    ax.set_title("Slide 17-18: Biểu đồ có ticks và labels")
    ax.set_xlabel("Giai đoạn")
    ax.set_ylabel("Giá trị")

    plt.savefig(save("slide17_18_ticks.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 19
  
def slide_19_legend() -> None:
    """Slide 19: Chú thích (legend)."""
    show_slide_header("19", "Thêm legend cho nhiều đường dữ liệu.")

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(randn(1000).cumsum(), "k", label="Đường 1")
    ax.plot(randn(1000).cumsum(), "k--", label="Đường 2")
    ax.plot(randn(1000).cumsum(), "k.", label="Đường 3")
    ax.legend(loc="upper left")
    ax.set_title("Slide 19: Ví dụ thêm chú thích (legend)")

    plt.savefig(save("slide19_legend.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 20
  
def slide_20_save_figure() -> None:
    """Slide 20: Lưu biểu đồ ra file."""
    show_slide_header("20", "Lưu biểu đồ ra SVG và PNG.")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(np.arange(5), np.random.randn(5).cumsum())
    axes[0].set_title("Ví dụ lưu SVG")

    axes[1].plot(np.arange(5), np.random.randn(5).cumsum())
    axes[1].set_title("Ví dụ lưu PNG (DPI cao)")

    plt.suptitle("Slide 20: Lưu biểu đồ ra file", fontsize=14)
    plt.tight_layout()
    plt.savefig(save("slide20_example.svg"))
    plt.savefig(save("slide20_example.png"), dpi=400, bbox_inches="tight")
    plt.close()
    print("Đã lưu: slide20_example.svg và slide20_example.png")


  
# Slide 21-22
  
def slide_21_22_rc_parameters() -> None:
    """Slide 21-22: Thiết lập tham số mặc định Matplotlib."""
    show_slide_header("21-22", "Thiết lập rcParams cho biểu đồ.")

    plt.rc("figure", figsize=(10, 6))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(np.arange(10), np.random.randn(10).cumsum())
    ax.set_title("Slide 21-22: Thiết lập tham số Matplotlib")

    plt.savefig(save("slide21_22_rc_params.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 28-29
  
def slide_28_29_line_plot() -> None:
    """Slide 28-29: Biểu đồ đường doanh số."""
    show_slide_header("28-29", "Vẽ biểu đồ đường doanh số 6 tháng.")

    data = {"thang": [1, 2, 3, 4, 5, 6], "doanh_so": [300, 350, 600, 700, 400, 500]}
    df = pd.DataFrame(data)
    print("DataFrame:")
    print(df)

    plt.figure(figsize=(10, 6))
    plt.plot(df["thang"], df["doanh_so"], marker="o", linewidth=2, label="Doanh số")
    plt.title("Slide 28-29: Doanh số 6 tháng đầu năm")
    plt.xlabel("Tháng")
    plt.ylabel("Doanh số")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(save("slide28_29_line_plot.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 30-31
  
def slide_30_31_customize_line_plot() -> None:
    """Slide 30-31: Tùy chỉnh biểu đồ đường."""
    show_slide_header("30-31", "Tùy chỉnh line plot: màu, linewidth, linestyle, marker.")

    data = {"thang": [1, 2, 3, 4, 5, 6], "doanh_so": [300, 350, 600, 700, 400, 500]}
    df = pd.DataFrame(data)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    axes[0, 0].plot(df["thang"], df["doanh_so"], color="red", linewidth=2)
    axes[0, 0].set_title("color='red'")

    axes[0, 1].plot(df["thang"], df["doanh_so"], color="green", linewidth=5)
    axes[0, 1].set_title("linewidth=5")

    axes[1, 0].plot(df["thang"], df["doanh_so"], linestyle="--", color="blue", linewidth=2)
    axes[1, 0].set_title("linestyle='--'")

    axes[1, 1].plot(df["thang"], df["doanh_so"], marker="^", color="purple", markersize=8, linewidth=2)
    axes[1, 1].set_title("marker='^'")

    for ax in axes.flat:
        ax.set_xlabel("Tháng")
        ax.set_ylabel("Doanh số")
        ax.grid(True, alpha=0.3)

    plt.suptitle("Slide 30-31: Tùy chỉnh biểu đồ đường", fontsize=14)
    plt.tight_layout()
    plt.savefig(save("slide30_31_customize_line.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 33-34
  
def slide_33_34_bar_plot() -> None:
    """Slide 33-34: Biểu đồ cột có hiển thị giá trị."""
    show_slide_header("33-34", "Vẽ bar plot và hiển thị giá trị trên cột.")

    data = {"thang": [1, 2, 3, 4, 5, 6], "doanh_so": [300, 350, 600, 700, 400, 500]}
    df = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))
    plt.bar(df["thang"], df["doanh_so"], color="skyblue", edgecolor="black", linewidth=2)
    for x, y in zip(df["thang"], df["doanh_so"]):
        plt.text(x, y + 10, str(y), ha="center")

    plt.title("Slide 33-34: Biểu đồ cột doanh số")
    plt.xlabel("Tháng")
    plt.ylabel("Doanh số bán hàng")
    plt.grid(axis="y", alpha=0.3)
    plt.savefig(save("slide33_34_bar_plot.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 35
  
def slide_35_horizontal_bar() -> None:
    """Slide 35: Biểu đồ cột ngang."""
    show_slide_header("35", "Vẽ horizontal bar plot và hiển thị giá trị.")

    data = {"thang": [1, 2, 3, 4, 5, 6], "doanh_so": [300, 350, 600, 700, 400, 500]}
    df = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))
    plt.barh(df["thang"], df["doanh_so"], color="skyblue", edgecolor="black", linewidth=2)
    for x, y in zip(df["doanh_so"], df["thang"]):
        plt.text(x + 10, y, str(x), va="center")

    plt.title("Slide 35: Biểu đồ cột ngang doanh số")
    plt.xlabel("Doanh số")
    plt.ylabel("Tháng")
    plt.grid(axis="x", alpha=0.3)
    plt.savefig(save("slide35_horizontal_bar.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 37-39
  
def slide_37_39_histogram() -> None:
    """Slide 37-39: Histogram phân phối dữ liệu."""
    show_slide_header("37-39", "Vẽ histogram và ghi tần suất trên từng cột.")

    np.random.seed(0)
    scores = np.random.normal(loc=6.5, scale=1.2, size=1000)
    scores = np.clip(scores, 0, 10)
    print(f"Tạo {len(scores)} điểm thi giả lập.")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(scores, bins=20, color="skyblue", edgecolor="black")
    axes[0].set_title("Slide 37-38: Phổ điểm THPT")
    axes[0].set_xlabel("Điểm")
    axes[0].set_ylabel("Số thí sinh")
    axes[0].grid(axis="y", alpha=0.3)

    counts, bins, _ = axes[1].hist(scores, bins=10, color="skyblue", edgecolor="black")
    for count, left, right in zip(counts, bins[:-1], bins[1:]):
        x = (left + right) / 2
        axes[1].text(x, count, int(count), ha="center", va="bottom")

    axes[1].set_title("Slide 39: Histogram có hiển thị tần suất")
    axes[1].set_xlabel("Điểm")
    axes[1].set_ylabel("Số thí sinh")
    axes[1].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(save("slide37_39_histogram.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 42
  
def slide_42_scatter_plot() -> None:
    """Slide 42: Scatter plot."""
    show_slide_header("42", "Vẽ scatter plot giữa tổng hóa đơn và tiền tip.")

    np.random.seed(42)
    total_bill = np.random.uniform(8, 50, 100)
    tip = total_bill * 0.15 + np.random.normal(0, 1, 100)
    print("Tạo 100 điểm dữ liệu total_bill và tip.")

    plt.figure(figsize=(10, 6))
    plt.scatter(total_bill, tip, alpha=0.6, s=50)
    plt.title("Slide 42: Quan hệ giữa tổng hóa đơn và tiền tip")
    plt.xlabel("Tổng hóa đơn (total_bill)")
    plt.ylabel("Tiền tip (tip)")
    plt.grid(True, alpha=0.3)
    plt.savefig(save("slide42_scatter_plot.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Slide 45
  
def slide_45_facet_grid() -> None:
    """Slide 45: Mô phỏng Facet Grid theo nhóm hút thuốc."""
    show_slide_header("45", "So sánh hóa đơn trung bình theo ngày và nhóm smoker.")

    np.random.seed(45)
    days = ["Thurs", "Fri", "Sat", "Sun"] * 25
    smoker = ["No", "Yes"] * 50
    total_bill = np.random.uniform(10, 50, 100)

    data = pd.DataFrame({"day": days, "smoker": smoker, "total_bill": total_bill})
    print("Tạo dữ liệu Facet Grid: 100 dòng.")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for smoker_status, ax in zip(["No", "Yes"], axes):
        data_filtered = data[data["smoker"] == smoker_status]
        daily_avg = data_filtered.groupby("day")["total_bill"].mean()

        ax.bar(range(len(daily_avg)), daily_avg.values, color="steelblue", edgecolor="black")
        ax.set_xticks(range(len(daily_avg)))
        ax.set_xticklabels(daily_avg.index)
        ax.set_title(f"Smoker = {smoker_status}")
        ax.set_ylabel("Hóa đơn trung bình")
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Slide 45: So sánh theo ngày và tình trạng hút thuốc", fontsize=12)
    plt.tight_layout()
    plt.savefig(save("slide45_facet_grid.png"), dpi=100, bbox_inches="tight")
    plt.close()


  
# Chạy toàn bộ ví dụ
  
if __name__ == "__main__":
    print("=" * 80)
    print("CHƯƠNG 3: TRỰC QUAN HÓA VÀ PHÂN TÍCH DỮ LIỆU")
    print("Tất cả ví dụ code từ Slide 9 trở đi")
    print("=" * 80)
    print_all_requirements()

    slide_9_example()
    slide_13_14_subplots()
    slide_15_customize_appearance()
    slide_17_18_ticks_labels()
    slide_19_legend()
    slide_20_save_figure()
    slide_21_22_rc_parameters()
    slide_28_29_line_plot()
    slide_30_31_customize_line_plot()
    slide_33_34_bar_plot()
    slide_35_horizontal_bar()
    slide_37_39_histogram()
    slide_42_scatter_plot()
    slide_45_facet_grid()

    print("\n" + "=" * 80)
    print("[OK] Tất cả ví dụ đã chạy xong!")
    print(f"[OK] Các file hình ảnh đã được lưu tại: {OUTPUT_DIR}")
    print("=" * 80)
