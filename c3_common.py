# -*- coding: utf-8 -*-  # Khai báo mã hóa UTF-8 để dùng tiếng Việt có dấu.
"""Tiện ích dùng chung cho các bài tập Chương 3."""  # Mô tả ngắn nội dung file.

from pathlib import Path  # Dùng Path để thao tác đường dẫn an toàn, đa nền tảng.
import sys  # Dùng sys để cấu hình encoding cho đầu ra terminal.

import matplotlib.pyplot as plt  # Dùng matplotlib để cấu hình style biểu đồ.
import pandas as pd  # Dùng pandas để đọc và xử lý dữ liệu bảng.


# Kiểm tra stdout có hỗ trợ đổi encoding hay không.
if hasattr(sys.stdout, "reconfigure"):  # Nếu có thì đổi sang UTF-8.
    sys.stdout.reconfigure(encoding="utf-8")  # Bảo đảm in tiếng Việt không lỗi.


BASE_DIR = Path(__file__).resolve().parent  # Lấy thư mục hiện tại (thư mục Chuong3).
DATA_CANDIDATES = [  # Danh sách vị trí ưu tiên để tìm file dữ liệu.
    BASE_DIR / "students_cleaned_final.csv",  # Ưu tiên dữ liệu nằm ngay trong Chuong3.
    BASE_DIR.parent / "Chuong2.2" / "students_cleaned_final.csv",  # Nếu không có thì lấy ở Chuong2.2.
]


def get_data_path() -> Path:
    """Tìm đường dẫn file dữ liệu trong các vị trí ưu tiên."""  # Hàm trả về đường dẫn file hợp lệ.
    for path in DATA_CANDIDATES:  # Duyệt lần lượt từng vị trí ứng viên.
        if path.exists():  # Nếu file tồn tại ở vị trí hiện tại.
            return path  # Trả về ngay đường dẫn đang tìm thấy.
    raise FileNotFoundError(  # Nếu duyệt hết mà không thấy file thì báo lỗi rõ ràng.
        "Không tìm thấy students_cleaned_final.csv. "  # Phần 1 thông báo lỗi.
        "Hãy đặt file trong Chuong3 hoặc Chuong2.2."  # Phần 2 thông báo lỗi.
    )


def load_data() -> tuple[pd.DataFrame, Path]:
    """Đọc dữ liệu và ép kiểu các cột số quan trọng."""  # Hàm đọc dữ liệu chuẩn cho mọi bài.
    path = get_data_path()  # Lấy đường dẫn hợp lệ của file dữ liệu.
    df = pd.read_csv(path)  # Đọc file CSV vào DataFrame.

    for col in ["Age", "Score", "Bonus", "Total", "Score_norm"]:  # Danh sách các cột kỳ vọng là số.
        if col in df.columns:  # Chỉ xử lý khi cột đó thực sự tồn tại trong dữ liệu.
            df[col] = pd.to_numeric(df[col], errors="coerce")  # Ép kiểu sang số, lỗi thì thành NaN.
    return df, path  # Trả về DataFrame và đường dẫn để file bài tập có thể in ra.


def setup_plot_style() -> None:
    """Thiết lập font hỗ trợ tiếng Việt cho biểu đồ."""  # Hàm chuẩn hóa font biểu đồ.
    plt.rcParams["font.family"] = "sans-serif"  # Đặt nhóm font chính là sans-serif.
    plt.rcParams["font.sans-serif"] = [  # Khai báo danh sách font fallback có hỗ trợ tiếng Việt.
        "DejaVu Sans",  # Font thường có sẵn trong matplotlib.
        "Arial",  # Font phổ biến trên Windows.
        "Tahoma",  # Font hỗ trợ tiếng Việt tốt trên Windows.
        "Noto Sans",  # Font đa ngôn ngữ.
        "Liberation Sans",  # Font thay thế phổ biến.
    ]
    plt.rcParams["axes.unicode_minus"] = False  # Hiển thị dấu trừ đúng khi dùng font Unicode.


def ensure_total(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo cột Total nếu chưa có (Total = Score + Bonus)."""  # Hàm đảm bảo có cột Total.
    if "Total" not in df.columns and {"Score", "Bonus"}.issubset(df.columns):  # Kiểm tra điều kiện đủ.
        df["Total"] = df["Score"] + df["Bonus"]  # Tạo cột Total bằng tổng Score và Bonus.
    return df  # Trả lại DataFrame sau khi đã bảo đảm cột Total.


def score_to_grade(score: float) -> str:
    """Quy đổi điểm số sang mức học lực."""  # Hàm ánh xạ điểm số sang nhãn học lực.
    if pd.isna(score):  # Nếu điểm bị thiếu hoặc không hợp lệ.
        return "Chưa xếp loại"  # Trả về nhãn chưa xếp loại.
    if score >= 8.5:  # Nếu điểm từ 8.5 trở lên.
        return "Giỏi"  # Xếp loại Giỏi.
    if score >= 7.0:  # Nếu điểm từ 7.0 đến dưới 8.5.
        return "Khá"  # Xếp loại Khá.
    if score >= 5.5:  # Nếu điểm từ 5.5 đến dưới 7.0.
        return "Trung bình"  # Xếp loại Trung bình.
    return "Yếu"  # Còn lại xếp loại Yếu.


def ensure_grade(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo cột Grade từ cột Score nếu dữ liệu chưa có sẵn."""  # Hàm đảm bảo tồn tại cột Grade.
    if "Grade" not in df.columns:  # Chỉ tạo mới khi dữ liệu hiện tại chưa có Grade.
        if "Score" not in df.columns:  # Nếu không có Score thì không thể sinh Grade.
            raise KeyError("Không có cột Score để tạo Grade.")  # Báo lỗi rõ nguyên nhân.
        df["Grade"] = df["Score"].apply(score_to_grade)  # Tạo Grade bằng cách áp dụng hàm quy đổi điểm.
    return df  # Trả lại DataFrame sau khi đã bảo đảm cột Grade.


def output_path(filename: str) -> Path:
    """Trả về đường dẫn output nằm trong thư mục Chuong3."""  # Hàm ghép đường dẫn file đầu ra.
    return BASE_DIR / filename  # Trả về đường dẫn tuyệt đối dạng Path.
