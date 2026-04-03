# -*- coding: utf-8 -*-  # Khai báo UTF-8 để hiển thị tiếng Việt đúng.
"""Bài 5 - So sánh điểm trung bình theo City."""  # Mô tả ngắn mục tiêu bài.

import matplotlib.pyplot as plt  # Import matplotlib để vẽ biểu đồ cột.

from c3_common import load_data, output_path, setup_plot_style  # Import các hàm tiện ích dùng chung.


if __name__ == "__main__":  # Chạy khi gọi file trực tiếp.
    print("=== C3_BT5: SO SÁNH GIỮA CÁC NHÓM ===")  # In tiêu đề bài.
    print("Yêu cầu: Vẽ mean Score theo City và kết luận City tốt nhất.")  # In yêu cầu bài.

    df, data_path = load_data()  # Đọc dữ liệu đã làm sạch.
    print(f"File dữ liệu: {data_path}")  # In ra đường dẫn file dữ liệu.
    setup_plot_style()  # Thiết lập font/kiểu cho biểu đồ.

    if "City" not in df.columns or "Score" not in df.columns:  # Kiểm tra cột bắt buộc.
        raise KeyError("Dữ liệu phải có cột City và Score.")  # Báo lỗi khi thiếu cột.

    mean_score_city = (  # Tạo Series mean Score theo từng City.
        df.dropna(subset=["City", "Score"])  # Bỏ dòng thiếu City hoặc Score.
        .groupby("City")["Score"]  # Nhóm theo City và chọn cột Score.
        .mean()  # Tính trung bình Score cho mỗi nhóm.
        .sort_values(ascending=False)  # Sắp xếp giảm dần để City tốt nhất đứng đầu.
    )
    if mean_score_city.empty:  # Kiểm tra trường hợp không có dữ liệu hợp lệ.
        raise ValueError("Không đủ dữ liệu để tính mean Score theo City.")  # Báo lỗi nếu rỗng.

    plt.figure(figsize=(9, 5))  # Tạo figure cho biểu đồ.
    bars = plt.bar(mean_score_city.index, mean_score_city.values, color="#F39C12")  # Vẽ cột mean Score theo City.
    plt.title("Mean Score theo City")  # Đặt tiêu đề biểu đồ.
    plt.xlabel("City")  # Đặt nhãn trục x.
    plt.ylabel("Mean Score")  # Đặt nhãn trục y.
    plt.grid(axis="y", alpha=0.3)  # Bật lưới trục y.
    for bar, value in zip(bars, mean_score_city.values):  # Duyệt từng cột và giá trị trung bình.
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.2f}", ha="center")  # Ghi giá trị lên đầu cột.
    plt.tight_layout()  # Canh bố cục để không bị cắt chữ.
    out_file = output_path("C3_BT5_mean_score_city.png")  # Tạo đường dẫn file output.
    plt.savefig(out_file, dpi=200, bbox_inches="tight")  # Lưu biểu đồ ra file PNG.
    plt.close()  # Đóng figure hiện tại.

    best_city = mean_score_city.idxmax()  # Lấy tên City có mean Score cao nhất.
    best_score = mean_score_city.max()  # Lấy giá trị mean Score cao nhất.
    print(f"Đã lưu biểu đồ: {out_file}")  # In thông báo lưu file thành công.
    print(f"Thành phố học tốt nhất: {best_city} (mean Score = {best_score:.2f})")  # In kết luận.
