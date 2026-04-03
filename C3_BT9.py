# -*- coding: utf-8 -*-  # Khai báo UTF-8 để dùng tiếng Việt có dấu.
"""Bài 9 - Tổng hợp và viết nhận xét dữ liệu."""  # Mô tả mục tiêu của bài 9.

from c3_common import ensure_grade, ensure_total, load_data, output_path  # Import các hàm hỗ trợ dùng chung.


if __name__ == "__main__":  # Khối này chỉ chạy khi gọi trực tiếp file C3_BT9.py.
    print("=== C3_BT9: TỔNG HỢP VÀ NHẬN XÉT ===")  # In tiêu đề bài.
    print("Yêu cầu: Viết 5-7 dòng nhận xét tổng quan.")  # In yêu cầu cần đạt.

    df, data_path = load_data()  # Đọc dữ liệu đầu vào từ file CSV.
    print(f"File dữ liệu: {data_path}")  # In ra file dữ liệu đang dùng.
    df = ensure_total(df)  # Bảo đảm DataFrame có cột Total.
    df = ensure_grade(df)  # Bảo đảm DataFrame có cột Grade.

    total_students = len(df)  # Tính tổng số sinh viên trong dữ liệu.
    mean_score = df["Score"].mean()  # Tính điểm Score trung bình toàn bộ dữ liệu.
    mean_total = df["Total"].mean() if "Total" in df.columns else float("nan")  # Tính Total trung bình nếu có cột Total.

    city_best = df.groupby("City")["Score"].mean().sort_values(ascending=False)  # Tính mean Score theo City và sắp giảm dần.
    class_best = df.groupby("Class")["Total"].mean().sort_values(ascending=False)  # Tính mean Total theo Class và sắp giảm dần.
    outliers = df[(df["Score"] > 9.5) | (df["Score"] < 5)]  # Lọc các điểm được xem là bất thường theo đề bài.
    grade_count = df["Grade"].value_counts()  # Đếm số lượng sinh viên theo từng mức học lực.

    top_city = city_best.index[0] if not city_best.empty else "Không xác định"  # Lấy City đứng đầu hoặc trả về mặc định nếu rỗng.
    top_city_score = city_best.iloc[0] if not city_best.empty else float("nan")  # Lấy mean Score cao nhất theo City.
    top_class = class_best.index[0] if not class_best.empty else "Không xác định"  # Lấy Class đứng đầu hoặc mặc định nếu rỗng.
    top_class_total = class_best.iloc[0] if not class_best.empty else float("nan")  # Lấy mean Total cao nhất theo Class.
    top_grade = grade_count.index[0] if not grade_count.empty else "Không xác định"  # Lấy nhóm học lực có số lượng nhiều nhất.

    summary_lines = [  # Tạo sẵn 6 dòng nhận xét theo đúng yêu cầu đề.
        f"1) Tập dữ liệu có {total_students} sinh viên, điểm Score trung bình là {mean_score:.2f}.",  # Dòng nhận xét 1.
        f"2) Tổng điểm (Total) trung bình là {mean_total:.2f}, cho thấy mặt bằng chung ở mức khá.",  # Dòng nhận xét 2.
        f"3) City nổi bật nhất là {top_city} với mean Score = {top_city_score:.2f}.",  # Dòng nhận xét 3.
        f"4) Class có tổng điểm cao nhất là {top_class} với mean Total = {top_class_total:.2f}.",  # Dòng nhận xét 4.
        f"5) Số điểm bất thường (Score > 9.5 hoặc < 5) là {len(outliers)} trường hợp.",  # Dòng nhận xét 5.
        f"6) Học lực phân bố nhiều nhất ở nhóm '{top_grade}', cần theo dõi các nhóm còn lại.",  # Dòng nhận xét 6.
    ]

    print("\nNhận xét tổng hợp (6 dòng):")  # In tiêu đề phần nhận xét.
    for line in summary_lines:  # Duyệt từng dòng nhận xét đã tạo.
        print(line)  # In từng dòng ra màn hình.

    out_file = output_path("C3_BT9_nhan_xet.txt")  # Tạo đường dẫn file txt đầu ra.
    out_file.write_text("\n".join(summary_lines), encoding="utf-8")  # Ghi toàn bộ nhận xét vào file UTF-8.
    print(f"\nĐã lưu nhận xét vào file: {out_file}")  # Thông báo vị trí file nhận xét.
