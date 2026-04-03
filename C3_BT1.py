# -*- coding: utf-8 -*-  # Khai báo mã hóa UTF-8 để hiển thị tiếng Việt.
"""Bài 1 - Kiểm tra dữ liệu đầu vào."""  # Mô tả ngắn nội dung bài 1.

from c3_common import load_data  # Import hàm đọc dữ liệu dùng chung.


if __name__ == "__main__":  # Chỉ chạy khi gọi trực tiếp file này.
    print("=== C3_BT1: KIỂM TRA DỮ LIỆU ĐẦU VÀO ===")  # In tiêu đề bài.
    print("Yêu cầu: Đọc file, in shape và info().")  # In yêu cầu cần thực hiện.

    df, data_path = load_data()  # Đọc DataFrame và lấy đường dẫn file dữ liệu.
    print(f"File dữ liệu: {data_path}")  # In ra nguồn dữ liệu đang sử dụng.

    print(f"Shape: {df.shape}")  # In số dòng và số cột của DataFrame.

    print("\nThông tin DataFrame:")  # In nhãn trước khi gọi info().
    df.info()  # In kiểu dữ liệu, số lượng non-null, dung lượng bộ nhớ.
