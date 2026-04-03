# -*- coding: utf-8 -*-  # Khai báo UTF-8 để hiển thị tiếng Việt.
"""Bài 4 - Phân tích điểm số bằng histogram."""  # Mô tả mục tiêu bài 4.

import numpy as np  # Import numpy để tìm bin có tần suất lớn nhất.
import matplotlib.pyplot as plt  # Import matplotlib để vẽ biểu đồ.

from c3_common import load_data, output_path, setup_plot_style  # Import tiện ích dùng chung.


if __name__ == "__main__":  # Chạy khối lệnh khi gọi file trực tiếp.
    print("=== C3_BT4: PHÂN TÍCH ĐIỂM SỐ ===")  # In tiêu đề bài.
    print("Yêu cầu: Vẽ histogram Score và nhận xét khoảng điểm tập trung.")  # In yêu cầu bài.

    df, data_path = load_data()  # Đọc dữ liệu từ file CSV đã làm sạch.
    print(f"File dữ liệu: {data_path}")  # In ra file dữ liệu đang phân tích.
    setup_plot_style()  # Thiết lập font tiếng Việt cho biểu đồ.

    if "Score" not in df.columns:  # Kiểm tra cột Score có tồn tại không.
        raise KeyError("Dữ liệu phải có cột Score.")  # Báo lỗi nếu thiếu cột.

    scores = df["Score"].dropna()  # Loại bỏ giá trị thiếu ở cột Score.
    if scores.empty:  # Kiểm tra trường hợp không còn dữ liệu hợp lệ để vẽ.
        raise ValueError("Cột Score không có dữ liệu hợp lệ.")  # Báo lỗi nếu không thể phân tích.

    plt.figure(figsize=(9, 5))  # Tạo khung hình biểu đồ.
    counts, bins, _ = plt.hist(scores, bins=8, color="#5DADE2", edgecolor="black")  # Vẽ histogram và lấy tần suất từng bin.
    plt.title("Histogram điểm Score")  # Đặt tiêu đề biểu đồ.
    plt.xlabel("Điểm Score")  # Đặt nhãn trục hoành.
    plt.ylabel("Số lượng sinh viên")  # Đặt nhãn trục tung.
    plt.grid(axis="y", alpha=0.3)  # Thêm lưới theo trục y.
    plt.tight_layout()  # Tối ưu bố cục tránh tràn chữ.
    out_file = output_path("C3_BT4_score_hist.png")  # Tạo đường dẫn file ảnh output.
    plt.savefig(out_file, dpi=200, bbox_inches="tight")  # Lưu biểu đồ ra file PNG.
    plt.close()  # Đóng biểu đồ để giải phóng tài nguyên.

    max_bin_idx = int(np.argmax(counts))  # Tìm chỉ số bin có tần suất cao nhất.
    low, high = bins[max_bin_idx], bins[max_bin_idx + 1]  # Lấy cận dưới và cận trên của bin đó.
    print(f"Đã lưu biểu đồ: {out_file}")  # Thông báo vị trí ảnh đã lưu.
    print("Nhận xét: Điểm tập trung nhiều nhất trong khoảng " f"{low:.2f} đến {high:.2f} (tần suất cao nhất).")  # In nhận xét tự động.
