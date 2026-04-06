# -*- coding: utf-8 -*-  # Khai báo UTF-8 để hiển thị tiếng Việt có dấu.
"""Bài 7 - Phân tích nâng cao theo Class và Total."""  # Mô tả mục tiêu bài 7.

import matplotlib.pyplot as plt  # Import thư viện vẽ biểu đồ.

from c3_common import ensure_total, load_data, output_path, setup_plot_style  # Import hàm dùng chung.


if __name__ == "__main__":  # Chạy khi file được gọi trực tiếp.
    print("=== C3_BT7: PHÂN TÍCH NÂNG CAO ===")  # In tiêu đề bài.
    print("Yêu cầu: Vẽ mean Total theo Class và kết luận lớp cao nhất.")  # In yêu cầu bài.

    df, data_path = load_data()  # Đọc dữ liệu đầu vào.
    print(f"File dữ liệu: {data_path}")  # In ra file nguồn dữ liệu.
    setup_plot_style()  # Thiết lập style và font cho biểu đồ.

    if "Class" not in df.columns:  # Kiểm tra cột Class có tồn tại không.
        raise KeyError("Dữ liệu phải có cột Class.")  # Báo lỗi nếu không có Class.

    df = ensure_total(df)  # Bảo đảm cột Total tồn tại trước khi tính toán.
    if "Total" not in df.columns:  # Kiểm tra lại sau khi gọi ensure_total.
        raise KeyError("Không có cột Total và cũng không tạo được từ Score + Bonus.")  # Báo lỗi rõ nguyên nhân.

    mean_total_class = (  # Tạo Series mean Total theo từng lớp.
        df.dropna(subset=["Class", "Total"])  # Bỏ các dòng thiếu Class hoặc Total.
        .groupby("Class")["Total"]  # Nhóm theo Class và chọn cột Total.
        .mean()  # Tính trung bình Total cho mỗi nhóm.
        .sort_values(ascending=False)  # Sắp xếp giảm dần để lớp cao nhất đứng đầu.
    )
    if mean_total_class.empty:  # Kiểm tra trường hợp dữ liệu rỗng sau lọc.
        raise ValueError("Không đủ dữ liệu để tính mean Total theo Class.")  # Báo lỗi khi không đủ dữ liệu.

    plt.figure(figsize=(9, 5))  # Tạo figure cho biểu đồ.
    bars = plt.bar(mean_total_class.index, mean_total_class.values, color="#16A085")  # Vẽ cột mean Total theo Class.
    plt.title("Mean Total theo Class")  # Đặt tiêu đề biểu đồ.
    plt.xlabel("Class")  # Đặt nhãn trục x.
    plt.ylabel("Mean Total")  # Đặt nhãn trục y.
    plt.grid(axis="y", alpha=0.3)  # Bật lưới cho trục y.
    for bar, value in zip(bars, mean_total_class.values):  # Duyệt qua từng cột để gắn nhãn giá trị.
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.2f}", ha="center")  # In giá trị phía trên cột.
    plt.tight_layout()  # Tối ưu bố cục biểu đồ.
    out_file = output_path("C3_BT7_mean_total_class.png")  # Tạo đường dẫn file output.
    plt.savefig(out_file, dpi=200, bbox_inches="tight")  # Lưu biểu đồ ra PNG.
    plt.close()  # Đóng figure để tránh chồng biểu đồ ở lần vẽ sau.

    best_class = mean_total_class.idxmax()  # Lấy lớp có mean Total cao nhất.
    best_total = mean_total_class.max()  # Lấy giá trị mean Total cao nhất.
    print(f"Đã lưu biểu đồ: {out_file}")  # In đường dẫn ảnh đã lưu.
    print(f"Lớp có tổng điểm cao nhất: {best_class} (mean Total = {best_total:.2f})")  # In kết luận cuối.
