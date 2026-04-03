# -*- coding: utf-8 -*-  # Khai báo UTF-8 để hiển thị tiếng Việt.
"""Bài 3 - Trực quan hóa cơ bản bằng bar chart."""  # Mô tả mục tiêu bài 3.

import matplotlib.pyplot as plt  # Import thư viện vẽ biểu đồ.

from c3_common import load_data, output_path, setup_plot_style  # Import hàm dùng chung.


if __name__ == "__main__":  # Chạy khi file được gọi trực tiếp.
    print("=== C3_BT3: TRỰC QUAN HÓA CƠ BẢN ===")  # In tiêu đề bài.
    print("Yêu cầu: Vẽ 2 bar chart (City, Class) có title và label.")  # In yêu cầu bài.

    df, data_path = load_data()  # Đọc dữ liệu đầu vào từ file CSV.
    print(f"File dữ liệu: {data_path}")  # In file nguồn dữ liệu.
    setup_plot_style()  # Áp dụng font/style để hiển thị tiếng Việt.

    if "City" not in df.columns or "Class" not in df.columns:  # Kiểm tra cột cần thiết.
        raise KeyError("Dữ liệu phải có cột City và Class.")  # Báo lỗi nếu thiếu cột.

    city_count = df["City"].fillna("UNKNOWN").value_counts()  # Đếm số lượng sinh viên theo City.
    class_count = df["Class"].fillna("UNKNOWN").value_counts()  # Đếm số lượng sinh viên theo Class.

    plt.figure(figsize=(9, 5))  # Tạo khung hình cho biểu đồ City.
    bars = plt.bar(city_count.index, city_count.values, color="#2E86C1")  # Vẽ cột theo City.
    plt.title("Số lượng sinh viên theo City")  # Đặt tiêu đề biểu đồ.
    plt.xlabel("City")  # Đặt nhãn trục hoành.
    plt.ylabel("Số lượng sinh viên")  # Đặt nhãn trục tung.
    plt.grid(axis="y", alpha=0.3)  # Hiển thị lưới theo trục y để dễ đọc.
    for bar, value in zip(bars, city_count.values):  # Duyệt từng cột và giá trị tương ứng.
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.05, str(int(value)), ha="center")  # Ghi giá trị lên đầu cột.
    plt.tight_layout()  # Canh bố cục tránh bị cắt chữ.
    out_city = output_path("C3_BT3_city_count.png")  # Tạo đường dẫn file ảnh output cho City.
    plt.savefig(out_city, dpi=200, bbox_inches="tight")  # Lưu biểu đồ City ra file PNG.
    plt.close()  # Đóng figure hiện tại để giải phóng bộ nhớ.

    plt.figure(figsize=(9, 5))  # Tạo khung hình cho biểu đồ Class.
    bars = plt.bar(class_count.index, class_count.values, color="#28B463")  # Vẽ cột theo Class.
    plt.title("Số lượng sinh viên theo Class")  # Đặt tiêu đề biểu đồ.
    plt.xlabel("Class")  # Đặt nhãn trục hoành.
    plt.ylabel("Số lượng sinh viên")  # Đặt nhãn trục tung.
    plt.grid(axis="y", alpha=0.3)  # Hiển thị lưới theo trục y.
    for bar, value in zip(bars, class_count.values):  # Duyệt từng cột và giá trị tương ứng.
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.05, str(int(value)), ha="center")  # Ghi giá trị lên đầu cột.
    plt.tight_layout()  # Canh bố cục cho đẹp.
    out_class = output_path("C3_BT3_class_count.png")  # Tạo đường dẫn file ảnh output cho Class.
    plt.savefig(out_class, dpi=200, bbox_inches="tight")  # Lưu biểu đồ Class ra file PNG.
    plt.close()  # Đóng figure hiện tại để tránh chồng biểu đồ.

    print(f"Đã lưu: {out_city}")  # Thông báo đường dẫn ảnh City đã lưu.
    print(f"Đã lưu: {out_class}")  # Thông báo đường dẫn ảnh Class đã lưu.
