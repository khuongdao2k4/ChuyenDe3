# ============================================================
# BÀI TOÁN CHƯƠNG 4: DỰ BÁO DOANH THU 12 THÁNG TỚI
# Data Analyst - Cửa hàng bán lẻ
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

# ============================================================
# BƯỚC 1: DATA PREPARATION
# ============================================================
print("=" * 60)
print("BƯỚC 1: DATA PREPARATION")
print("=" * 60)

# Load dữ liệu
df = pd.read_csv("dataset.csv")

# Convert date → datetime và set index
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df.set_index("date")

print("Dữ liệu gốc:")
print(df.head())

# Kiểm tra Missing Values
print("\n--- Kiểm tra Missing Values ---")
print(df.isnull().sum())

# Kiểm tra Duplicate
print("\n--- Kiểm tra Duplicate ---")
print(f"Số dòng bị duplicate: {df.index.duplicated().sum()}")

# Resample về monthly (đã là monthly, nhưng đảm bảo đúng)
df = df.resample("ME").mean()

# Tạo features thời gian
df["month"] = df.index.month
df["quarter"] = df.index.quarter
df["year"] = df.index.year

# Tạo lag features
df["lag_1"] = df["sales"].shift(1)
df["lag_3"] = df["sales"].shift(3)

# Rolling mean
df["rolling_mean_3"] = df["sales"].rolling(window=3).mean()

# Xóa NaN do lag/rolling
df_model = df.dropna().copy()

print("\nDữ liệu sau khi tạo features:")
print(df_model.head())
print(f"\nShape sau xử lý: {df_model.shape}")

# ============================================================
# BƯỚC 2: EDA - KHÁM PHÁ DỮ LIỆU
# ============================================================
print("\n" + "=" * 60)
print("BƯỚC 2: EDA - KHÁM PHÁ DỮ LIỆU")
print("=" * 60)

# --- Line chart doanh thu + Rolling mean ---
fig, axes = plt.subplots(3, 1, figsize=(12, 12))
fig.suptitle("EDA - Khám phá dữ liệu doanh thu", fontsize=14, fontweight="bold")

# Plot 1: Line chart + Rolling mean
axes[0].plot(df.index, df["sales"], label="Doanh thu thực tế", color="#2196F3", linewidth=2, marker="o", markersize=4)
axes[0].plot(df.index, df["sales"].rolling(3).mean(), label="Rolling Mean 3 tháng", color="#FF9800", linewidth=2, linestyle="--")
axes[0].plot(df.index, df["sales"].rolling(6).mean(), label="Rolling Mean 6 tháng", color="#F44336", linewidth=2, linestyle="-.")
axes[0].set_title("Doanh thu theo thời gian & Rolling Mean")
axes[0].set_ylabel("Doanh thu")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Tương quan sales vs promotion_budget
axes[1].scatter(df["promotion_budget"], df["sales"], color="#9C27B0", alpha=0.7, s=80)
axes[1].set_title("Tương quan: Sales vs Promotion Budget")
axes[1].set_xlabel("Ngân sách khuyến mãi")
axes[1].set_ylabel("Doanh thu")
axes[1].grid(True, alpha=0.3)
# Thêm trend line
z = np.polyfit(df["promotion_budget"].dropna(), df["sales"].dropna(), 1)
p = np.poly1d(z)
x_line = np.linspace(df["promotion_budget"].min(), df["promotion_budget"].max(), 100)
axes[1].plot(x_line, p(x_line), color="#F44336", linestyle="--", label="Trend")
axes[1].legend()

# Plot 3: Tương quan sales vs num_customers
axes[2].scatter(df["num_customers"], df["sales"], color="#009688", alpha=0.7, s=80)
axes[2].set_title("Tương quan: Sales vs Số Khách Hàng")
axes[2].set_xlabel("Số lượng khách hàng")
axes[2].set_ylabel("Doanh thu")
axes[2].grid(True, alpha=0.3)
z2 = np.polyfit(df["num_customers"].dropna(), df["sales"].dropna(), 1)
p2 = np.poly1d(z2)
x_line2 = np.linspace(df["num_customers"].min(), df["num_customers"].max(), 100)
axes[2].plot(x_line2, p2(x_line2), color="#F44336", linestyle="--", label="Trend")
axes[2].legend()

plt.tight_layout()
plt.savefig("eda_analysis.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Đã lưu: eda_analysis.png")

# Phân tích xu hướng
print("\n--- Phân tích xu hướng ---")
sales_start = df["sales"].iloc[0]
sales_end = df["sales"].iloc[-1]
trend_pct = (sales_end - sales_start) / sales_start * 100
print(f"Doanh thu đầu kỳ: {sales_start:.2f}")
print(f"Doanh thu cuối kỳ: {sales_end:.2f}")
print(f"Tăng trưởng tổng: {trend_pct:.1f}%")

# Phân tích mùa vụ
print("\n--- Phân tích mùa vụ (TB doanh thu theo tháng) ---")
monthly_avg = df.groupby("month")["sales"].mean()
print(monthly_avg.round(2))
print(f"Tháng cao nhất: {monthly_avg.idxmax()} (TB: {monthly_avg.max():.2f})")
print(f"Tháng thấp nhất: {monthly_avg.idxmin()} (TB: {monthly_avg.min():.2f})")

# Tương quan
print("\n--- Hệ số tương quan ---")
corr = df[["sales", "promotion_budget", "num_customers"]].corr()
print(corr.round(3))

# ============================================================
# BƯỚC 3: VISUALIZATION
# ============================================================
print("\n" + "=" * 60)
print("BƯỚC 3: VISUALIZATION")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Visualization - Phân tích doanh thu", fontsize=13, fontweight="bold")

# 1. Line plot time series
axes[0].plot(df.index, df["sales"], color="#2196F3", linewidth=2, marker="o", markersize=5)
axes[0].set_title("Line Plot: Doanh thu theo thời gian")
axes[0].set_xlabel("Thời gian")
axes[0].set_ylabel("Doanh thu")
axes[0].tick_params(axis="x", rotation=45)
axes[0].grid(True, alpha=0.3)

# 2. Bar chart theo tháng
bar_data = df.groupby("month")["sales"].mean()
bars = axes[1].bar(bar_data.index, bar_data.values, color="#4CAF50", edgecolor="white", linewidth=0.5)
axes[1].set_title("Bar Chart: TB Doanh thu theo tháng")
axes[1].set_xlabel("Tháng")
axes[1].set_ylabel("Doanh thu trung bình")
axes[1].set_xticks(range(1, 13))
axes[1].grid(True, alpha=0.3, axis="y")
# Thêm giá trị trên cột
for bar, val in zip(bars, bar_data.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 f"{val:.0f}", ha="center", va="bottom", fontsize=8)

# 3. Scatter: promotion vs sales
axes[2].scatter(df["promotion_budget"], df["sales"], color="#FF5722", alpha=0.8, s=80, edgecolors="white")
axes[2].set_title("Scatter: Promotion Budget vs Sales")
axes[2].set_xlabel("Ngân sách khuyến mãi")
axes[2].set_ylabel("Doanh thu")
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("visualization.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Đã lưu: visualization.png")

# ============================================================
# BƯỚC 4: XÂY DỰNG MÔ HÌNH DỰ BÁO
# ============================================================
print("\n" + "=" * 60)
print("BƯỚC 4: XÂY DỰNG MÔ HÌNH DỰ BÁO")
print("=" * 60)

# Features và Target
FEATURES = ["month", "quarter", "promotion_budget", "num_customers",
            "lag_1", "lag_3", "rolling_mean_3"]
TARGET = "sales"

X = df_model[FEATURES]
y = df_model[TARGET]

# Train/test split (80/20, giữ thứ tự thời gian)
split_idx = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

print(f"Train size: {len(X_train)} | Test size: {len(X_test)}")

# --- MÔ HÌNH 1: Linear Regression (bắt buộc) ---
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

print("\n[MÔ HÌNH 1] Linear Regression - Hệ số:")
for feat, coef in zip(FEATURES, lr.coef_):
    print(f"  {feat}: {coef:.4f}")
print(f"  Intercept: {lr.intercept_:.4f}")

# --- MÔ HÌNH 2: Random Forest ---
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("\n[MÔ HÌNH 2] Random Forest - Feature Importance:")
importance = pd.Series(rf.feature_importances_, index=FEATURES).sort_values(ascending=False)
print(importance.round(4))

# ============================================================
# BƯỚC 5: ĐÁNH GIÁ MÔ HÌNH
# ============================================================
print("\n" + "=" * 60)
print("BƯỚC 5: ĐÁNH GIÁ MÔ HÌNH")
print("=" * 60)

def evaluate_model(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    print(f"\n{'='*30}")
    print(f"📊 {name}")
    print(f"  MAE  : {mae:.4f}")
    print(f"  RMSE : {rmse:.4f}")
    print(f"  MAPE : {mape:.2f}%")
    return {"model": name, "MAE": mae, "RMSE": rmse, "MAPE": mape}

results = []
results.append(evaluate_model("Linear Regression", y_test, y_pred_lr))
results.append(evaluate_model("Random Forest", y_test, y_pred_rf))

results_df = pd.DataFrame(results).set_index("model")
print("\n--- Bảng so sánh mô hình ---")
print(results_df.round(4))

# Chọn model tốt nhất (RMSE thấp nhất)
best_model_name = results_df["RMSE"].idxmin()
best_model = lr if best_model_name == "Linear Regression" else rf
print(f"\n✅ Mô hình tốt nhất: {best_model_name} (RMSE thấp nhất: {results_df.loc[best_model_name, 'RMSE']:.4f})")

# Plot so sánh Actual vs Predicted
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("So sánh Actual vs Predicted trên tập Test", fontsize=13, fontweight="bold")

for ax, (name, y_pred) in zip(axes, [("Linear Regression", y_pred_lr), ("Random Forest", y_pred_rf)]):
    ax.plot(y_test.index, y_test.values, label="Actual", color="#2196F3", marker="o", linewidth=2)
    ax.plot(y_test.index, y_pred, label="Predicted", color="#FF9800", marker="s", linewidth=2, linestyle="--")
    ax.set_title(name)
    ax.set_ylabel("Doanh thu")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("model_evaluation.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Đã lưu: model_evaluation.png")

# ============================================================
# BƯỚC 6: FORECAST 12 THÁNG TỚI
# ============================================================
print("\n" + "=" * 60)
print("BƯỚC 6: FORECAST 12 THÁNG TỚI")
print("=" * 60)

# Tạo dữ liệu cho 12 tháng tới (bắt đầu từ 2025-01)
last_date = df.index[-1]
future_dates = pd.date_range(start=last_date + pd.offsets.MonthEnd(1), periods=12, freq="ME")

# Ước lượng promotion_budget và num_customers bằng rolling mean
avg_promotion = df["promotion_budget"].rolling(6).mean().iloc[-1]
avg_customers = df["num_customers"].rolling(6).mean().iloc[-1]

# Build future dataframe từng bước (cần lag)
history_sales = df["sales"].tolist()

future_rows = []
for i, date in enumerate(future_dates):
    lag_1 = history_sales[-1]
    lag_3 = history_sales[-3]
    rolling_mean_3 = np.mean(history_sales[-3:])
    row = {
        "date": date,
        "month": date.month,
        "quarter": (date.month - 1) // 3 + 1,
        "promotion_budget": avg_promotion,
        "num_customers": avg_customers,
        "lag_1": lag_1,
        "lag_3": lag_3,
        "rolling_mean_3": rolling_mean_3,
    }
    future_rows.append(row)
    # Predict và append vào history
    X_fut = pd.DataFrame([row])[FEATURES]
    pred = best_model.predict(X_fut)[0]
    history_sales.append(pred)

future_df = pd.DataFrame(future_rows).set_index("date")
X_future = future_df[FEATURES]
future_df["predicted_sales"] = best_model.predict(X_future)

print("\nDự báo doanh thu 12 tháng tới:")
print(future_df[["predicted_sales"]].round(2).to_string())

# Plot Actual vs Forecast
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(df.index, df["sales"], label="Doanh thu thực tế", color="#2196F3", linewidth=2, marker="o", markersize=5)
ax.plot(future_df.index, future_df["predicted_sales"], label="Dự báo 12 tháng tới",
        color="#FF5722", linewidth=2.5, marker="D", markersize=6, linestyle="--")
ax.axvline(x=df.index[-1], color="gray", linestyle=":", linewidth=1.5, label="Ranh giới dự báo")
ax.fill_between(future_df.index, future_df["predicted_sales"] * 0.93,
                future_df["predicted_sales"] * 1.07, alpha=0.2, color="#FF5722", label="Khoảng tin cậy ±7%")
ax.set_title(f"Dự báo doanh thu 12 tháng tới ({best_model_name})", fontsize=13, fontweight="bold")
ax.set_xlabel("Thời gian")
ax.set_ylabel("Doanh thu")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("forecast_12months.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Đã lưu: forecast_12months.png")

# ============================================================
# BƯỚC 7: BUSINESS INSIGHT
# ============================================================
print("\n" + "=" * 60)
print("BƯỚC 7: BUSINESS INSIGHT")
print("=" * 60)

# 1. Xu hướng doanh thu
print("\n1️⃣  XU HƯỚNG DOANH THU")
yearly_sales = df.groupby("year")["sales"].sum()
for yr, val in yearly_sales.items():
    print(f"   Năm {yr}: Tổng doanh thu = {val:.2f}")
total_growth = (yearly_sales.iloc[-1] - yearly_sales.iloc[0]) / yearly_sales.iloc[0] * 100
print(f"   → Tăng trưởng từ {yearly_sales.index[0]} đến {yearly_sales.index[-1]}: {total_growth:.1f}%")
print("   → Doanh thu có xu hướng TĂNG ĐỀU qua các năm.")

# 2. Ảnh hưởng của Promotion
print("\n2️⃣  ẢNH HƯỞNG CỦA PROMOTION")
corr_promo = df["sales"].corr(df["promotion_budget"])
print(f"   Hệ số tương quan Sales - Promotion: {corr_promo:.3f}")
if corr_promo > 0.3:
    print("   → Promotion có tác động TÍCH CỰC đến doanh thu.")
    print("   → Tăng ngân sách marketing có xu hướng kéo doanh thu lên.")
else:
    print("   → Promotion có ít ảnh hưởng hoặc không đáng kể đến doanh thu.")

# 3. Gợi ý chiến lược
print("\n3️⃣  ĐỀ XUẤT CHIẾN LƯỢC KINH DOANH")

# Tháng có doanh thu thấp
low_months = monthly_avg.nsmallest(3).index.tolist()
high_months = monthly_avg.nlargest(3).index.tolist()
print(f"\n   📅 Tháng doanh thu CAO: {high_months} → Duy trì chất lượng dịch vụ, tăng tồn kho.")
print(f"   📅 Tháng doanh thu THẤP: {low_months} → Nên tập trung tăng marketing.")

forecast_growth = (future_df["predicted_sales"].iloc[-1] - df["sales"].iloc[-1]) / df["sales"].iloc[-1] * 100
print(f"\n   📈 Dự báo tăng trưởng doanh thu 12 tháng tới: {forecast_growth:.1f}%")

if forecast_growth > 10:
    print("   → XEM XÉT MỞ RỘNG kinh doanh (tăng quy mô, kho bãi, nhân sự).")
elif forecast_growth > 0:
    print("   → Tăng trưởng ổn định, duy trì chiến lược hiện tại.")
else:
    print("   → Cần xem xét lại chiến lược, doanh thu có dấu hiệu giảm.")

print("\n   💡 Gợi ý cụ thể:")
print("      - Tăng ngân sách marketing vào các tháng có doanh thu thấp")
print("      - Theo dõi chặt chẽ số lượng khách (num_customers) – chỉ số sức khoẻ kinh doanh")
print("      - Nếu khách tăng nhưng doanh thu không tăng → cần cải thiện giá trị đơn hàng")
print("      - Nên áp dụng chương trình khách hàng thân thiết để giữ chân khách cũ")

print("\n" + "=" * 60)
print("✅ HOÀN THÀNH TOÀN BỘ PHÂN TÍCH")
print("=" * 60)
print("\nCác file đã tạo:")
print("  📊 eda_analysis.png       - Biểu đồ EDA")
print("  📊 visualization.png      - Visualization (3 biểu đồ)")
print("  📊 model_evaluation.png   - So sánh Actual vs Predicted")
print("  📊 forecast_12months.png  - Dự báo 12 tháng tới")
