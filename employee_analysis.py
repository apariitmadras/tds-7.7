"""
employee_analysis.py
Author contact: 24ds1000011@ds.study.iitm.ac.in

What this script does
- Loads employee data from 'employees.csv' if present; otherwise generates a synthetic dataset of 100 employees and saves it.
- Calculates and prints the frequency count for the "Finance" department.
- Creates a histogram-style bar chart showing the distribution of departments using matplotlib.
- Saves an HTML file ('employee_report.html') that embeds:
    - the exact Python code
    - the generated plot (as a base64-embedded PNG)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from pathlib import Path

def load_or_generate_data(csv_path: Path) -> pd.DataFrame:
    if csv_path.exists():
        df = pd.read_csv(csv_path)
    else:
        rng = np.random.default_rng(7)
        departments = ["Finance", "HR", "IT", "Operations", "Sales", "Marketing"]
        regions = ["North", "South", "East", "West"]
        # Generate 100 employees with realistic distributions
        data = {
            "Employee_ID": range(1, 101),
            "Department": rng.choice(departments, size=100, p=[0.18, 0.12, 0.22, 0.20, 0.18, 0.10]),
            "Region": rng.choice(regions, size=100, p=[0.3, 0.25, 0.25, 0.2]),
            "Performance_Score": rng.integers(1, 6, size=100),  # 1 to 5
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)
    return df

def plot_department_distribution(df: pd.DataFrame) -> BytesIO:
    counts = df["Department"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))  # single chart as required
    ax.bar(counts.index, counts.values)     # no explicit colors to follow tool rules
    ax.set_title("Department Distribution (Employee Count)")
    ax.set_xlabel("Department")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()

    # Save to buffer
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

def build_html_report(code_text: str, img_png_bytes: bytes, finance_count: int, out_html: Path):
    img_b64 = base64.b64encode(img_png_bytes).decode("ascii")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Employee Analysis Report</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; }}
    h1, h2 {{ margin: 0.2em 0; }}
    .code {{ white-space: pre; background: #f5f5f5; border: 1px solid #e0e0e0; padding: 12px; overflow-x: auto; }}
    .meta {{ color: #444; margin-bottom: 16px; }}
    .imgwrap {{ display: flex; justify-content: center; margin: 16px 0; }}
  </style>
</head>
<body>
  <h1>Employee Performance Analysis</h1>
  <div class="meta">Author contact: <strong>24ds1000011@ds.study.iitm.ac.in</strong></div>

  <h2>Finance Department Frequency</h2>
  <p>Number of employees in <strong>Finance</strong>: <strong>{finance_count}</strong></p>

  <h2>Department Distribution (Histogram-style)</h2>
  <div class="imgwrap">
    <img alt="Department Distribution" src="data:image/png;base64,{img_b64}" />
  </div>

  <h2>Python Code</h2>
  <div class="code">{code_text}</div>
</body>
</html>"""
    out_html.write_text(html, encoding="utf-8")

def main():
    # Paths
    base = Path(".")
    csv_path = base / "employees.csv"
    out_html = base / "employee_report.html"

    # Load or generate data
    df = load_or_generate_data(csv_path)

    # Frequency count for Finance
    finance_count = int((df["Department"] == "Finance").sum())
    print(f"Finance department frequency: {finance_count}")

    # Plot distribution
    buf = plot_department_distribution(df)
    img_bytes = buf.getvalue()

    # Read our own code to embed into HTML
    code_text = Path(__file__).read_text(encoding="utf-8")
    # Escape HTML special characters for safe display
    code_text = (code_text
                 .replace("&", "&amp;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;"))

    # Build the HTML report
    build_html_report(code_text, img_bytes, finance_count, out_html)

if __name__ == "__main__":
    main()
