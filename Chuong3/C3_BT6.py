# -*- coding: utf-8 -*-  # Khai báo UTF-8 để hỗ trợ tiếng Việt.
"""Bài 6 - Phân tích mối quan hệ giữa Age và Score."""  # Mô tả ngắn mục tiêu bài.

import matplotlib.pyplot as plt  # Import thư viện để vẽ scatter plot.

from c3_common import load_data, output_path, setup_plot_style  # Import các hàm dùng chung.


if __name__ == "__main__":  # Chỉ chạy khi gọi file trực tiếp.
    print("=== C3_BT6: PHÂN TÍCH MỐI QUAN HỆ ===")  # In tiêu đề bài.
    print("Yêu cầu: Vẽ scatter Age vs Score và nhận xét ảnh hưởng của tuổi.")  # In yêu cầu.

    df, data_path = load_data()  # Đọc dữ liệu từ file CSV.
    print(f"File dữ liệu: {data_path}")  # In đường dẫn file dữ liệu.
    setup_plot_style()  # Cài đặt style/font cho biểu đồ.

    if "Age" not in df.columns or "Score" not in df.columns:  # Kiểm tra 2 cột bắt buộc.
        raise KeyError("Dữ liệu phải có cột Age và Score.")  # Báo lỗi nếu thiếu cột.

    data = df[["Age", "Score"]].dropna()  # Lấy 2 cột cần phân tích và bỏ giá trị thiếu.
    if data.empty:  # Kiểm tra còn dữ liệu hợp lệ hay không.
        raise ValueError("Không đủ dữ liệu hợp lệ cho Age và Score.")  # Báo lỗi nếu rỗng.

    plt.figure(figsize=(9, 5))  # Tạo khung figure cho biểu đồ.
    plt.scatter(data["Age"], data["Score"], alpha=0.75, s=60, color="#8E44AD")  # Vẽ scatter plot.
    plt.title("Scatter plot: Age vs Score")  # Đặt tiêu đề biểu đồ.
    plt.xlabel("Age")  # Đặt nhãn trục hoành.
    plt.ylabel("Score")  # Đặt nhãn trục tung.
    plt.grid(alpha=0.3)  # Thêm lưới nền để dễ quan sát.
    plt.tight_layout()  # Tối ưu bố cục hình.
    out_file = output_path("C3_BT6_age_score_scatter.png")  # Tạo đường dẫn file output.
    plt.savefig(out_file, dpi=200, bbox_inches="tight")  # Lưu biểu đồ ra PNG.
    plt.close()  # Đóng figure để giải phóng bộ nhớ.

    corr = data["Age"].corr(data["Score"])  # Tính hệ số tương quan Pearson giữa Age và Score.
    if corr is None or (corr != corr):  # Kiểm tra trường hợp NaN hoặc không xác định.
        relation = "Không đủ dữ liệu để kết luận mối quan hệ."  # Nhận xét khi không đủ dữ liệu.
    elif abs(corr) < 0.2:  # Nếu độ lớn tương quan rất thấp.
        relation = "Tuổi ảnh hưởng rất yếu đến điểm."  # Kết luận ảnh hưởng yếu.
    elif abs(corr) < 0.5:  # Nếu độ lớn tương quan mức trung bình.
        relation = "Tuổi có ảnh hưởng mức vừa đến điểm."  # Kết luận ảnh hưởng vừa.
    else:  # Trường hợp còn lại: tương quan khá mạnh.
        relation = "Tuổi có ảnh hưởng rõ đến điểm."  # Kết luận ảnh hưởng rõ.

    print(f"Đã lưu biểu đồ: {out_file}")  # In đường dẫn file biểu đồ đã lưu.
    print(f"Hệ số tương quan Age-Score: {corr:.3f}")  # In giá trị hệ số tương quan.
    print(f"Nhận xét: {relation}")  # In câu nhận xét cuối cùng.
