def euro(x: float) -> str:
    return f"€{x:,.0f}".replace(",", " ")


def pct(x: float) -> str:
    return f"{x*100:.1f}%"


def badge(text: str, color: str = "yellow") -> str:
    return f"[{text}]"




