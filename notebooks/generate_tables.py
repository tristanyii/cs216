"""
generate_tables.py
Generates formatted table figures for the CS216 prototype report.
Outputs PNG images to ../figures/
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────────
_HERE       = os.path.dirname(os.path.abspath(__file__))
_ROOT       = os.path.dirname(_HERE)
CLEAN_DATA  = os.path.join(_ROOT, "data", "processed", "kalshi_data_clean.csv")
CALIB_DATA  = os.path.join(_ROOT, "data", "processed", "calibration_results.csv")
FIGURES_DIR = os.path.join(_ROOT, "figures") + os.sep

# ── Load data ──────────────────────────────────────────────────────────────────
df    = pd.read_csv(CLEAN_DATA)
calib = pd.read_csv(CALIB_DATA)

df["result_binary"] = (df["result"] == "yes").astype(int)


# ── Helper: render a DataFrame as a PNG table ──────────────────────────────────
def save_table(table_df, filename, title, col_widths=None, figsize=None):
    n_rows, n_cols = table_df.shape
    if figsize is None:
        figsize = (max(8, n_cols * 1.6), 0.55 * n_rows + 1.0)

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")

    tbl = ax.table(
        cellText=table_df.values,
        colLabels=table_df.columns,
        loc="center",
        cellLoc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    if col_widths:
        for (row, col), cell in tbl.get_celld().items():
            cell.set_width(col_widths[col] if col < len(col_widths) else 0.15)

    # Style header row
    for col in range(n_cols):
        tbl[(0, col)].set_facecolor("#2c5f8a")
        tbl[(0, col)].set_text_props(color="white", fontweight="bold")

    # Alternating row shading
    for row in range(1, n_rows + 1):
        color = "#f0f4f8" if row % 2 == 0 else "white"
        for col in range(n_cols):
            tbl[(row, col)].set_facecolor(color)

    ax.set_title(title, fontsize=12, fontweight="bold", pad=14)
    plt.tight_layout()
    path = FIGURES_DIR + filename
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


# ── Table 1: Dataset Descriptive Statistics ────────────────────────────────────
df["date"] = pd.to_datetime(df["date"])

desc = pd.DataFrame({
    "Metric": [
        "Total contracts (cleaned)",
        "Date range",
        "Unique market titles",
        "Mean final price",
        "Median final price",
        "Std dev of final price",
        "Proportion resolving 'Yes'",
        "Proportion resolving 'No'",
    ],
    "Value": [
        f"{len(df):,}",
        f"{df['date'].min().date()} – {df['date'].max().date()}",
        f"{df['title'].nunique():,}",
        f"{df['last_price_dollars'].mean():.3f}",
        f"{df['last_price_dollars'].median():.3f}",
        f"{df['last_price_dollars'].std():.3f}",
        f"{(df['result'] == 'yes').mean():.1%}",
        f"{(df['result'] == 'no').mean():.1%}",
    ],
})

save_table(
    desc,
    "table1_descriptive_stats.png",
    "Table 1: Descriptive Statistics of Cleaned Kalshi Dataset",
    figsize=(8, 4),
)


# ── Table 2: Calibration Results ───────────────────────────────────────────────
calib_display = pd.DataFrame({
    "Probability Bin":    calib["bin"],
    "Contract Count":     calib["count"].apply(lambda x: f"{x:,}"),
    "Predicted Prob.":    calib["pred_mean"].apply(lambda x: f"{x:.3f}"),
    "Observed Freq.":     calib["obs_mean"].apply(lambda x: f"{x:.3f}"),
    "95% CI":             calib.apply(
        lambda r: f"[{r['ci_low']:.3f}, {r['ci_high']:.3f}]", axis=1
    ),
    "Absolute Error":     (calib["pred_mean"] - calib["obs_mean"]).abs().apply(
        lambda x: f"{x:.3f}"
    ),
})

save_table(
    calib_display,
    "table2_calibration_results.png",
    "Table 2: Kalshi Calibration Results by Probability Bin",
    figsize=(12, 5),
)


# ── Table 3: Contracts per Year ────────────────────────────────────────────────
df["year"] = df["date"].dt.year
yearly = df.groupby("year").agg(
    Contracts=("result", "count"),
    Yes_Rate=("result_binary", "mean"),
    Mean_Price=("last_price_dollars", "mean"),
).reset_index()
yearly.columns = ["Year", "Contracts", "Yes Rate", "Mean Final Price"]
yearly["Contracts"]        = yearly["Contracts"].apply(lambda x: f"{x:,}")
yearly["Yes Rate"]         = yearly["Yes Rate"].apply(lambda x: f"{x:.1%}")
yearly["Mean Final Price"] = yearly["Mean Final Price"].apply(lambda x: f"{x:.3f}")

save_table(
    yearly,
    "table3_contracts_per_year.png",
    "Table 3: Contract Volume and Outcome Rates by Year",
    figsize=(8, 3.5),
)

print("\nAll tables saved to", FIGURES_DIR)
