# -*- coding: utf-8 -*-  # Khai báo UTF-8 để hiển thị tiếng Việt.
"""Bài 8 - Trực quan hóa phân bố học lực theo Grade."""  # Mô tả mục tiêu bài 8.

import matplotlib.pyplot as plt  # Import matplotlib để vẽ biểu đồ cột.

from c3_common import ensure_grade, load_data, output_path, setup_plot_style  # Import tiện ích dùng chung.


if __name__ == "__main__":  # Chỉ chạy khi file được thực thi trực tiếp.
    print("=== C3_BT8: TRỰC QUAN HÓA NÂNG CAO ===")  # In tiêu đề bài.
    print("Yêu cầu: Vẽ số lượng sinh viên theo Grade và nhận xét phân bố học lực.")  # In yêu cầu.

    df, data_path = load_data()  # Đọc dữ liệu đầu vào.
    print(f"File dữ liệu: {data_path}")  # In file đang được dùng.
    setup_plot_style()  # Thiết lập font/style cho biểu đồ tiếng Việt.

    df = ensure_grade(df)  # Tạo cột Grade nếu dữ liệu chưa có.

    grade_order = ["Giỏi", "Khá", "Trung bình", "Yếu", "Chưa xếp loại"]  # Khai báo thứ tự hiển thị học lực.
    grade_count = df["Grade"].value_counts().reindex(grade_order, fill_value=0)  # Đếm số lượng từng mức học lực theo đúng thứ tự.
    grade_count = grade_count[grade_count > 0]  # Loại các mức có số lượng bằng 0 để biểu đồ gọn hơn.

    if grade_count.empty:  # Kiểm tra dữ liệu Grade còn hợp lệ để vẽ hay không.
        raise ValueError("Không có dữ liệu Grade để vẽ biểu đồ.")  # Báo lỗi nếu không có dữ liệu.

    plt.figure(figsize=(9, 5))  # Tạo figure cho biểu đồ.
    bars = plt.bar(grade_count.index, grade_count.values, color="#C0392B")  # Vẽ bar chart theo Grade.
    plt.title("Số lượng sinh viên theo Grade")  # Đặt tiêu đề biểu đồ.
    plt.xlabel("Grade")  # Đặt nhãn trục x.
    plt.ylabel("Số lượng sinh viên")  # Đặt nhãn trục y.
    plt.grid(axis="y", alpha=0.3)  # Hiển thị lưới nền theo trục y.
    for bar, value in zip(bars, grade_count.values):  # Duyệt qua từng cột và giá trị.
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.05, str(int(value)), ha="center")  # Ghi số lượng lên đầu cột.
    plt.tight_layout()  # Canh bố cục biểu đồ.
    out_file = output_path("C3_BT8_grade_count.png")  # Tạo đường dẫn file output.
    plt.savefig(out_file, dpi=200, bbox_inches="tight")  # Lưu biểu đồ ra ảnh PNG.
    plt.close()  # Đóng figure để giải phóng bộ nhớ.

    percent = (grade_count / grade_count.sum() * 100).round(1)  # Tính tỉ lệ phần trăm từng mức học lực.
    print(f"Đã lưu biểu đồ: {out_file}")  # In thông báo file đã lưu.
    print("Phân bố học lực (%):")  # In tiêu đề phần tỉ lệ.
    for grade, p in percent.items():  # Duyệt qua từng mức học lực và phần trăm tương ứng.
        print(f"- {grade}: {p}%")  # In chi tiết tỉ lệ từng mức.
