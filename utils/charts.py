import pandas as pd
import plotly.express as px


def stacked_bar_overview(rail: float, retail: float, baseline: float):
    df = pd.DataFrame({
        "category": ["Rail", "Retail", "MSF 2024"],
        "value": [rail, retail, baseline],
    })
    fig = px.bar(df, x="category", y="value", text_auto=True, title="Annual totals (net €)")
    fig.update_yaxes(title_text="€ net")
    return fig




