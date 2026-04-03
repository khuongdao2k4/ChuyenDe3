# -*- coding: utf-8 -*-  # Khai báo mã hóa UTF-8 để dùng tiếng Việt.
"""Bài 2 - Phân tích tổng quan dữ liệu."""  # Mô tả nội dung chính của bài 2.

import pandas as pd  # Import pandas để tạo bảng tổng hợp kiểm tra.

from c3_common import load_data  # Import hàm đọc dữ liệu dùng chung.


if __name__ == "__main__":  # Chạy khối lệnh khi gọi file trực tiếp.
    print("=== C3_BT2: PHÂN TÍCH TỔNG QUAN ===")  # In tiêu đề bài.
    print("Yêu cầu: Thống kê số lượng theo City và Class.")  # In yêu cầu bài.

    df, data_path = load_data()  # Đọc dữ liệu đầu vào và đường dẫn file.
    print(f"File dữ liệu: {data_path}")  # In đường dẫn file đang được dùng.

    if "City" not in df.columns or "Class" not in df.columns:  # Kiểm tra cột bắt buộc.
        raise KeyError("Dữ liệu phải có cột City và Class.")  # Báo lỗi nếu thiếu cột.

    city_count = (  # Tạo bảng đếm số lượng sinh viên theo City.
        df["City"]  # Chọn cột City.
        .fillna("UNKNOWN")  # Thay giá trị thiếu bằng nhãn UNKNOWN.
        .value_counts()  # Đếm số lần xuất hiện từng City.
        .rename_axis("City")  # Đặt tên cột chỉ mục là City.
        .reset_index(name="Số_lượng_sinh_viên")  # Chuyển về DataFrame có tên cột số lượng.
    )

    class_count = (  # Tạo bảng đếm số lượng sinh viên theo Class.
        df["Class"]  # Chọn cột Class.
        .fillna("UNKNOWN")  # Thay giá trị thiếu bằng nhãn UNKNOWN.
        .value_counts()  # Đếm số lần xuất hiện từng Class.
        .rename_axis("Class")  # Đặt tên cột chỉ mục là Class.
        .reset_index(name="Số_lượng_sinh_viên")  # Chuyển về DataFrame có tên cột số lượng.
    )

    print("\nBảng số lượng sinh viên theo City:")  # In tiêu đề bảng City.
    print(city_count.to_string(index=False))  # In bảng City không kèm cột index.

    print("\nBảng số lượng sinh viên theo Class:")  # In tiêu đề bảng Class.
    print(class_count.to_string(index=False))  # In bảng Class không kèm cột index.

    pivot = pd.DataFrame(  # Tạo bảng nhỏ để kiểm tra tổng số lượng có khớp hay không.
        {
            "Tổng_theo_City": [city_count["Số_lượng_sinh_viên"].sum()],  # Tổng số theo City.
            "Tổng_theo_Class": [class_count["Số_lượng_sinh_viên"].sum()],  # Tổng số theo Class.
        }
    )
    print("\nKiểm tra tổng số lượng (City vs Class):")  # In tiêu đề phần kiểm tra.
    print(pivot.to_string(index=False))  # In bảng kiểm tra tổng số.
