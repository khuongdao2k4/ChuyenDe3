"""
Dự báo Doanh Thu Bán Lẻ – Chương 4
Bài toán: Dự báo doanh thu 12 tháng tới dựa trên dữ liệu 3 năm
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler

# ──────────────────────────────────────────────
# 0. TẠO DỮ LIỆU MẪU (nếu chưa có file CSV)
# ──────────────────────────────────────────────
def generate_sample_data(filepath="retail_sales.csv"):
    """Tạo dữ liệu mẫu 3 năm (36 tháng)."""
    np.random.seed(42)
    dates = pd.date_range(start="2022-01-31", periods=36, freq="ME")
    trend = np.linspace(180, 320, 36)
    seasonality = 30 * np.sin(2 * np.pi * np.arange(36) / 12)
    noise = np.random.normal(0, 10, 36)
    sales = trend + seasonality + noise

    promotion = np.random.randint(40, 120, 36).astype(float)
    # Promotion có ảnh hưởng nhẹ đến sales
    sales += 0.4 * promotion + np.random.normal(0, 5, 36)

    num_customers = (sales / 0.5 + np.random.normal(0, 20, 36)).astype(int)

    df = pd.DataFrame({
        "date": dates,
        "sales": np.round(sales, 2),
        "promotion_budget": np.round(promotion, 2),
        "num_customers": num_customers
    })
    df.to_csv(filepath, index=False)
    print(f"✅ Đã tạo dữ liệu mẫu: {filepath}")
    return filepath

# ──────────────────────────────────────────────
# BƯỚC 1: DATA PREPARATION
# ──────────────────────────────────────────────
def step1_data_preparation(filepath):
    print("\n" + "="*60)
    print("BƯỚC 1: DATA PREPARATION")
    print("="*60)

    df = pd.read_csv(filepath)
    print(f"\n📋 Shape ban đầu: {df.shape}")
    print(df.head())

    # 1.1 Convert date → datetime
    df["date"] = pd.to_datetime(df["date"])
    print(f"\n✅ Convert date → datetime: {df['date'].dtype}")

    # 1.2 Set index theo thời gian
    df = df.set_index("date").sort_index()
    print(f"✅ Set index theo date")

    # 1.3 Kiểm tra Missing Values
    print(f"\n🔍 Missing Values:\n{df.isnull().sum()}")

    # 1.4 Kiểm tra Duplicate
    dup = df.index.duplicated().sum()
    print(f"🔍 Duplicate dates: {dup}")

    # 1.5 Resample về Monthly (đã là monthly, đảm bảo chắc chắn)
    df = df.resample("ME").mean()
    print(f"\n✅ Resample monthly → shape: {df.shape}")

    # 1.6 Tạo features
    df["month"]        = df.index.month
    df["quarter"]      = df.index.quarter
    df["year"]         = df.index.year
    df["lag_1"]        = df["sales"].shift(1)
    df["lag_3"]        = df["sales"].shift(3)
    df["rolling_mean_3"] = df["sales"].shift(1).rolling(window=3).mean()

    # Loại bỏ NaN sau khi tạo lag
    df = df.dropna()
    print(f"✅ Tạo feature lag_1, lag_3, rolling_mean_3 → shape sau dropna: {df.shape}")
    print(f"\n📊 Thống kê mô tả:\n{df.describe().round(2)}")

    return df

# ──────────────────────────────────────────────
# BƯỚC 2: EDA
# ──────────────────────────────────────────────
def step2_eda(df):
    print("\n" + "="*60)
    print("BƯỚC 2: EDA – KHÁM PHÁ DỮ LIỆU")
    print("="*60)

    # Xu hướng
    rolling3 = df["sales"].rolling(3).mean()
    rolling6 = df["sales"].rolling(6).mean()

    trend_slope = np.polyfit(range(len(df)), df["sales"], 1)[0]
    print(f"\n📈 Slope xu hướng: {trend_slope:.2f} (tháng)")
    print(f"   → {'Xu hướng TĂNG' if trend_slope > 0 else 'Xu hướng GIẢM'}")

    # Mùa vụ
    seasonal = df.groupby("month")["sales"].mean()
    peak_month = seasonal.idxmax()
    low_month  = seasonal.idxmin()
    print(f"\n📅 Tháng doanh thu cao nhất: {peak_month}")
    print(f"   Tháng doanh thu thấp nhất: {low_month}")

    # Tương quan
    corr_promo    = df["sales"].corr(df["promotion_budget"])
    corr_customer = df["sales"].corr(df["num_customers"])
    print(f"\n🔗 Tương quan sales vs promotion_budget : {corr_promo:.3f}")
    print(f"   Tương quan sales vs num_customers    : {corr_customer:.3f}")

    return rolling3, rolling6

# ──────────────────────────────────────────────
# BƯỚC 3: VISUALIZATION
# ──────────────────────────────────────────────
def step3_visualization(df, rolling3, rolling6):
    print("\n" + "="*60)
    print("BƯỚC 3: VISUALIZATION")
    print("="*60)

    fig = plt.figure(figsize=(18, 14))
    fig.suptitle("Phân tích Doanh Thu Bán Lẻ", fontsize=16, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

    # -- 3.1 Line chart doanh thu + rolling mean --
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(df.index, df["sales"], label="Doanh thu thực tế", color="#2196F3", linewidth=2, marker="o", markersize=4)
    ax1.plot(df.index, rolling3, label="Rolling Mean 3 tháng", color="#FF9800", linewidth=2, linestyle="--")
    ax1.plot(df.index, rolling6, label="Rolling Mean 6 tháng", color="#F44336", linewidth=2, linestyle=":")
    ax1.set_title("Doanh Thu Theo Thời Gian & Rolling Mean", fontweight="bold")
    ax1.set_ylabel("Doanh thu (triệu đồng)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # -- 3.2 Bar chart theo tháng (trung bình) --
    ax2 = fig.add_subplot(gs[1, 0])
    monthly_avg = df.groupby("month")["sales"].mean()
    colors = ["#EF5350" if v == monthly_avg.max() else "#42A5F5" for v in monthly_avg.values]
    bars = ax2.bar(monthly_avg.index, monthly_avg.values, color=colors, edgecolor="white")
    ax2.set_title("Doanh Thu Trung Bình Theo Tháng", fontweight="bold")
    ax2.set_xlabel("Tháng")
    ax2.set_ylabel("Doanh thu TB")
    ax2.set_xticks(range(1, 13))
    for bar, val in zip(bars, monthly_avg.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f"{val:.0f}", ha="center", va="bottom", fontsize=8)
    ax2.grid(True, alpha=0.3, axis="y")

    # -- 3.3 Scatter: promotion vs sales --
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.scatter(df["promotion_budget"], df["sales"], alpha=0.7, color="#66BB6A", s=60, edgecolors="white")
    m, b = np.polyfit(df["promotion_budget"], df["sales"], 1)
    x_line = np.linspace(df["promotion_budget"].min(), df["promotion_budget"].max(), 100)
    ax3.plot(x_line, m * x_line + b, "r--", linewidth=2, label=f"Trend (slope={m:.2f})")
    ax3.set_title("Promotion Budget vs Doanh Thu", fontweight="bold")
    ax3.set_xlabel("Promotion Budget")
    ax3.set_ylabel("Doanh thu")
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # -- 3.4 Scatter: customers vs sales --
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.scatter(df["num_customers"], df["sales"], alpha=0.7, color="#AB47BC", s=60, edgecolors="white")
    m2, b2 = np.polyfit(df["num_customers"], df["sales"], 1)
    x2 = np.linspace(df["num_customers"].min(), df["num_customers"].max(), 100)
    ax4.plot(x2, m2 * x2 + b2, "r--", linewidth=2, label=f"Trend (slope={m2:.3f})")
    ax4.set_title("Số Khách Hàng vs Doanh Thu", fontweight="bold")
    ax4.set_xlabel("Số khách hàng")
    ax4.set_ylabel("Doanh thu")
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # -- 3.5 Box plot theo quý --
    ax5 = fig.add_subplot(gs[2, 1])
    quarters = [df[df["quarter"] == q]["sales"].values for q in [1, 2, 3, 4]]
    bp = ax5.boxplot(quarters, labels=["Q1", "Q2", "Q3", "Q4"],
                     patch_artist=True,
                     boxprops=dict(facecolor="#29B6F6", alpha=0.7),
                     medianprops=dict(color="red", linewidth=2))
    ax5.set_title("Phân Phối Doanh Thu Theo Quý", fontweight="bold")
    ax5.set_ylabel("Doanh thu")
    ax5.grid(True, alpha=0.3, axis="y")

    plt.savefig("eda_visualization.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✅ Đã lưu: eda_visualization.png")

# ──────────────────────────────────────────────
# BƯỚC 4 & 5: MÔ HÌNH & ĐÁNH GIÁ
# ──────────────────────────────────────────────
def step4_5_models(df):
    print("\n" + "="*60)
    print("BƯỚC 4: XÂY DỰNG MÔ HÌNH DỰ BÁO")
    print("="*60)

    FEATURES = ["month", "quarter", "year", "promotion_budget",
                "num_customers", "lag_1", "lag_3", "rolling_mean_3"]
    TARGET = "sales"

    # Train/test split: 80% train, 20% test
    split = int(len(df) * 0.8)
    train = df.iloc[:split]
    test  = df.iloc[split:]

    X_train, y_train = train[FEATURES], train[TARGET]
    X_test,  y_test  = test[FEATURES],  test[TARGET]

    print(f"\n📊 Train: {len(train)} tháng | Test: {len(test)} tháng")

    results = {}

    # ── Mô hình 1: Linear Regression ──
    print("\n🔵 Mô hình 1: Linear Regression")
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    lr = LinearRegression()
    lr.fit(X_train_sc, y_train)
    y_pred_lr = lr.predict(X_test_sc)

    mae_lr  = mean_absolute_error(y_test, y_pred_lr)
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
    mape_lr = np.mean(np.abs((y_test - y_pred_lr) / y_test)) * 100
    print(f"   MAE : {mae_lr:.2f}")
    print(f"   RMSE: {rmse_lr:.2f}")
    print(f"   MAPE: {mape_lr:.2f}%")

    results["Linear Regression"] = {
        "model": lr, "scaler": scaler,
        "y_pred": y_pred_lr,
        "MAE": mae_lr, "RMSE": rmse_lr, "MAPE": mape_lr
    }

    # ── Mô hình 2: Random Forest ──
    print("\n🟢 Mô hình 2: Random Forest")
    rf = RandomForestRegressor(n_estimators=200, max_depth=6, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)

    mae_rf  = mean_absolute_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    mape_rf = np.mean(np.abs((y_test - y_pred_rf) / y_test)) * 100
    print(f"   MAE : {mae_rf:.2f}")
    print(f"   RMSE: {rmse_rf:.2f}")
    print(f"   MAPE: {mape_rf:.2f}%")

    results["Random Forest"] = {
        "model": rf, "scaler": None,
        "y_pred": y_pred_rf,
        "MAE": mae_rf, "RMSE": rmse_rf, "MAPE": mape_rf
    }

    # ── So sánh mô hình ──
    print("\n" + "="*60)
    print("BƯỚC 5: SO SÁNH MÔ HÌNH")
    print("="*60)
    comparison = pd.DataFrame({
        "Mô hình": list(results.keys()),
        "MAE":  [results[k]["MAE"]  for k in results],
        "RMSE": [results[k]["RMSE"] for k in results],
        "MAPE (%)": [results[k]["MAPE"] for k in results],
    })
    print(f"\n{comparison.to_string(index=False)}")

    best_model_name = comparison.loc[comparison["RMSE"].idxmin(), "Mô hình"]
    print(f"\n🏆 Mô hình tốt nhất (RMSE thấp nhất): {best_model_name}")

    return results, best_model_name, train, test, X_test, y_test, FEATURES

# ──────────────────────────────────────────────
# BƯỚC 6: FORECAST 12 THÁNG
# ──────────────────────────────────────────────
def step6_forecast(df, results, best_model_name, FEATURES):
    print("\n" + "="*60)
    print("BƯỚC 6: FORECAST 12 THÁNG TỚI")
    print("="*60)

    best = results[best_model_name]
    model  = best["model"]
    scaler = best["scaler"]

    last_date  = df.index[-1]
    last_sales = df["sales"].values.tolist()

    # Dùng giá trị trung bình promotion & customers
    avg_promo     = df["promotion_budget"].mean()
    avg_customers = df["num_customers"].mean()

    forecast_dates  = []
    forecast_values = []

    sales_history = list(df["sales"].values)

    for i in range(1, 13):
        next_date = last_date + pd.DateOffset(months=i)
        next_date = next_date + pd.offsets.MonthEnd(0)

        lag_1 = sales_history[-1]
        lag_3 = sales_history[-3] if len(sales_history) >= 3 else sales_history[0]
        roll3 = np.mean(sales_history[-3:]) if len(sales_history) >= 3 else sales_history[-1]

        row = pd.DataFrame([{
            "month":            next_date.month,
            "quarter":          (next_date.month - 1) // 3 + 1,
            "year":             next_date.year,
            "promotion_budget": avg_promo,
            "num_customers":    avg_customers,
            "lag_1":            lag_1,
            "lag_3":            lag_3,
            "rolling_mean_3":   roll3,
        }])

        if scaler:
            X_input = scaler.transform(row[FEATURES])
        else:
            X_input = row[FEATURES].values

        pred = model.predict(X_input)[0]
        forecast_values.append(pred)
        sales_history.append(pred)
        forecast_dates.append(next_date)

    forecast_df = pd.DataFrame({
        "date": forecast_dates,
        "forecast_sales": np.round(forecast_values, 2)
    }).set_index("date")

    print(f"\n📅 Dự báo doanh thu 12 tháng tới ({best_model_name}):")
    print(forecast_df.to_string())

    return forecast_df

# ──────────────────────────────────────────────
# BIỂU ĐỒ KẾT QUẢ MÔ HÌNH
# ──────────────────────────────────────────────
def plot_model_results(df, results, best_model_name, test, y_test, forecast_df):
    fig, axes = plt.subplots(3, 1, figsize=(14, 16))
    fig.suptitle("Kết Quả Mô Hình & Dự Báo Doanh Thu", fontsize=15, fontweight="bold")

    # -- Plot 1: Actual vs Predicted (2 mô hình) --
    ax = axes[0]
    ax.plot(test.index, y_test, label="Actual", color="#2196F3", linewidth=2, marker="o", markersize=5)
    colors_model = {"Linear Regression": "#FF9800", "Random Forest": "#4CAF50"}
    for name, res in results.items():
        ax.plot(test.index, res["y_pred"], label=f"Predicted ({name})",
                color=colors_model.get(name, "gray"), linewidth=2, linestyle="--", marker="s", markersize=5)
    ax.set_title("Actual vs Predicted – Giai đoạn Test", fontweight="bold")
    ax.set_ylabel("Doanh thu")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # -- Plot 2: So sánh MAE / RMSE --
    ax2 = axes[1]
    names = list(results.keys())
    mae_vals  = [results[k]["MAE"]  for k in names]
    rmse_vals = [results[k]["RMSE"] for k in names]
    x = np.arange(len(names))
    w = 0.35
    bars1 = ax2.bar(x - w/2, mae_vals,  w, label="MAE",  color="#42A5F5", edgecolor="white")
    bars2 = ax2.bar(x + w/2, rmse_vals, w, label="RMSE", color="#EF5350", edgecolor="white")
    for bar in list(bars1) + list(bars2):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=9)
    ax2.set_title("So Sánh MAE & RMSE Giữa Các Mô Hình", fontweight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(names)
    ax2.set_ylabel("Error")
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis="y")

    # -- Plot 3: Forecast 12 tháng --
    ax3 = axes[2]
    ax3.plot(df.index, df["sales"], label="Doanh thu lịch sử", color="#2196F3",
             linewidth=2, marker="o", markersize=4)
    ax3.plot(forecast_df.index, forecast_df["forecast_sales"],
             label=f"Dự báo 12 tháng ({best_model_name})",
             color="#FF5722", linewidth=2.5, linestyle="--", marker="D", markersize=6)
    # Vùng uncertainty ±10%
    lower = forecast_df["forecast_sales"] * 0.90
    upper = forecast_df["forecast_sales"] * 1.10
    ax3.fill_between(forecast_df.index, lower, upper, alpha=0.15, color="#FF5722", label="Khoảng tin cậy ±10%")
    # Đường phân cách lịch sử / dự báo
    ax3.axvline(x=df.index[-1], color="gray", linestyle=":", linewidth=1.5, label="Ranh giới dự báo")
    ax3.set_title(f"Dự Báo Doanh Thu 12 Tháng Tới ({best_model_name})", fontweight="bold")
    ax3.set_ylabel("Doanh thu (triệu đồng)")
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("forecast_results.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("✅ Đã lưu: forecast_results.png")

# ──────────────────────────────────────────────
# BƯỚC 7: BUSINESS INSIGHT
# ──────────────────────────────────────────────
def step7_business_insight(df, results, forecast_df):
    print("\n" + "="*60)
    print("BƯỚC 7: BUSINESS INSIGHT")
    print("="*60)

    # Xu hướng
    slope = np.polyfit(range(len(df)), df["sales"], 1)[0]
    avg_monthly_growth = slope
    total_forecast = forecast_df["forecast_sales"].sum()
    peak_forecast_month = forecast_df["forecast_sales"].idxmax()
    low_forecast_month  = forecast_df["forecast_sales"].idxmin()

    # Tương quan
    corr_promo    = df["sales"].corr(df["promotion_budget"])
    corr_customer = df["sales"].corr(df["num_customers"])

    # Tháng mùa vụ
    monthly_avg   = df.groupby("month")["sales"].mean()
    peak_months   = monthly_avg.nlargest(3).index.tolist()
    low_months    = monthly_avg.nsmallest(3).index.tolist()

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    BUSINESS INSIGHT REPORT                   ║
╠══════════════════════════════════════════════════════════════╣

 1. XU HƯỚNG DOANH THU
   ▸ Doanh thu tăng trung bình {avg_monthly_growth:+.1f} triệu đồng/tháng
   ▸ Tổng dự báo 12 tháng tới: {total_forecast:.0f} triệu đồng
   ▸ Tháng đỉnh dự báo   : {peak_forecast_month.strftime('%m/%Y')} 
     ({forecast_df['forecast_sales'].max():.1f} triệu đồng)
   ▸ Tháng đáy dự báo    : {low_forecast_month.strftime('%m/%Y')} 
     ({forecast_df['forecast_sales'].min():.1f} triệu đồng)

 2. HIỆU QUẢ PROMOTION
   ▸ Tương quan promotion vs sales: r = {corr_promo:.3f}
   ▸ {'Promotion có ảnh hưởng TÍCH CỰC đến doanh thu ✅' if corr_promo > 0.3 else 'Ảnh hưởng promotion còn HẠN CHẾ ⚠️'}
   ▸ Tương quan customers vs sales : r = {corr_customer:.3f}

 3. MÙA VỤ & KHI NÀO TĂNG MARKETING
   ▸ Top 3 tháng doanh thu CAO: {peak_months}
     → Đây là mùa đỉnh, nên chạy promotion trước 1–2 tháng
   ▸ Top 3 tháng doanh thu THẤP: {low_months}
     → Cần kích cầu: giảm giá, tặng kèm, voucher

 4. ĐỀ XUẤT KINH DOANH

   A. KHI NÀO NÊN TĂNG MARKETING?
      • Tăng ngân sách marketing vào tháng {low_months[0]} – {low_months[1]}
        để kéo doanh thu trong mùa thấp điểm
      • Giữ ngân sách ổn định tháng đỉnh vì nhu cầu đã tự nhiên cao

   B. CÓ NÊN MỞ RỘNG KINH DOANH?
      • Xu hướng tăng {avg_monthly_growth:+.1f} triệu/tháng → CÓ tiềm năng mở rộng
      • Khuyến nghị: Mở rộng sau khi đạt doanh thu ổn định ≥ 3 quý liên tiếp

   C. CHIẾN LƯỢC TĂNG DOANH THU
      1. Tăng Giá Trị Đơn Hàng: Upsell / Bundle sản phẩm
      2. Chăm Sóc Khách Hàng: Loyalty program → tăng repeat purchase
      3. Mở Kênh Online: Bổ sung kênh bán hàng TMĐT
      4. Tối ưu Promotion: Chạy promotion đúng thời điểm thấp điểm

╚══════════════════════════════════════════════════════════════╝
""")

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print(" BẮT ĐẦU PIPELINE DỰ BÁO DOANH THU BÁN LẺ")
    print("="*60)

    # 0. Tạo / đọc dữ liệu
    filepath = generate_sample_data("retail_sales.csv")

    # 1. Data Preparation
    df = step1_data_preparation(filepath)

    # 2. EDA
    rolling3, rolling6 = step2_eda(df)

    # 3. Visualization
    step3_visualization(df, rolling3, rolling6)

    # 4 & 5. Mô hình & Đánh giá
    results, best_model_name, train, test, X_test, y_test, FEATURES = step4_5_models(df)

    # 6. Forecast
    forecast_df = step6_forecast(df, results, best_model_name, FEATURES)

    # 7. Business Insight
    step7_business_insight(df, results, forecast_df)

    # Plot kết quả
    plot_model_results(df, results, best_model_name, test, y_test, forecast_df)

    # Lưu kết quả dự báo
    forecast_df.to_csv("forecast_12months.csv")
    print("\n Đã lưu: forecast_12months.csv")
    print("\n HOÀN THÀNH! Các file output:")
    print("    eda_visualization.png")
    print("    forecast_results.png")
    print("    forecast_12months.csv")
    print("    retail_sales.csv")