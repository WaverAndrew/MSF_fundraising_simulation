import json
from typing import Dict, Any, List

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from defaults import DEFAULTS, SOURCES, LANGUAGE
from utils.formatting import euro, pct, badge
from utils.charts import stacked_bar_overview
from models.rail import RailInputs, compute_rail_monthly
from models.retail import RetailInputs, RetailMethod, compute_retail_monthly, simulate_roundup_distribution
from models.montecarlo import run_monte_carlo


st.set_page_config(page_title="MSF Micro-donations Simulator", layout="wide")


def init_state() -> None:
    if "assumptions" not in st.session_state:
        st.session_state.assumptions = json.loads(json.dumps(DEFAULTS))
    if "rail_inputs" not in st.session_state:
        st.session_state.rail_inputs = None
    if "retail_inputs" not in st.session_state:
        st.session_state.retail_inputs = None
    if "months" not in st.session_state:
        st.session_state.months = 12




def sources_tab() -> None:
    st.subheader("Data Sources & References")
    
    st.markdown("""
    This simulator uses data from multiple sources. All assumptions and defaults are based on publicly available information 
    and industry research. Click on the links below to access the original sources.
    """)
    
    st.markdown("### Key Sources")
    
    for label, url in SOURCES.items():
        st.markdown(f"- **[{label}]({url})**")
    
    st.markdown("---")
    
    st.markdown("### Compliance & Ethics")
    st.info("""
    **EU Consumer Rights Directive**: All donations must be opt-in only. Pre-ticked boxes for paid extras are prohibited.
    
    This simulator enforces compliance by ensuring all donation prompts are explicit opt-in choices, aligning with MSF's 
    values of transparency and respect for donor autonomy.
    """)
    
    st.markdown("### Notes on Data")
    st.markdown("""
    - **Rail data**: Based on 2023 figures from FS Group and Italo press releases. Digital share estimates are based on 
      industry trends and FS digital growth reports.
    
    - **Retail data**: ISTAT household spending data (2023/2024) combined with NielsenIQ grocery statistics. 
      Charm pricing prevalence based on academic research.
    
    - **Opt-in rates**: Defaults are conservative estimates based on checkout charity research and industry benchmarks. 
      Actual rates may vary based on implementation, placement, and messaging.
    
    - **Payment processors**: Adyen Giving offers fee-free donations. Other processors may charge standard transaction fees.
    """)


def overview_tab(rail_df: pd.DataFrame, retail_df: pd.DataFrame) -> None:
    rail_annual = rail_df[rail_df["metric"] == "net"].groupby("year")["value"].sum().sum()
    retail_annual = retail_df[retail_df["metric"] == "net"].groupby("year")["value"].sum().sum()
    total_annual = rail_annual + retail_annual
    msf_baseline = st.session_state.assumptions["msf_italy"]["fundraising_2024_eur"]

    retail_only = st.checkbox("Show retail-only scenario", value=False, key="overview_retail_only")
    display_total = retail_annual if retail_only else total_annual
    months = st.session_state.months
    period_label = f"Total net € ({months} month{'s' if months != 1 else ''})"

    c1, c2, c3 = st.columns(3)
    c1.metric(period_label, euro(display_total))
    rail_label = "Rail net €" + (" (excluded)" if retail_only else "")
    retail_label = "Retail net €" + (" (included)" if retail_only else "")
    c2.metric(rail_label, euro(rail_annual))
    c3.metric(retail_label, euro(retail_annual))

    st.markdown(
        "A soft, explicit opt-in at checkout aligns with MSF's ethics and donor experience."
    )

    share = (display_total / msf_baseline) if msf_baseline > 0 else 0
    st.metric("% of MSF Italy fundraising 2024", pct(share))

    fig = stacked_bar_overview(
        rail=0 if retail_only else rail_annual,
        retail=retail_annual,
        baseline=msf_baseline,
    )
    st.plotly_chart(fig, use_container_width=True)

    if retail_only:
        st.info("Retail-only scenario: rail contribution excluded from totals above.")
    else:
        st.info("Compliance: opt-in donations only. No pre-ticked boxes (EU directive).")


def rail_tab() -> pd.DataFrame:
    st.subheader("Rail module (Trenitalia + Italo)")

    a = st.session_state.assumptions
    months = st.slider("Time period (months)", min_value=1, max_value=36, value=st.session_state.months, key="rail_months")
    st.session_state.months = months
    
    with st.expander("Inputs", expanded=True):
        trenitalia_riders = st.number_input(
            "Trenitalia annual riders",
            min_value=0,
            value=int(a["rail"]["trenitalia_riders"]),
            step=1000000,
            key="rail_trenitalia_riders",
        )

        italo_riders = st.number_input(
            "Italo annual riders",
            min_value=0,
            value=int(a["rail"]["italo_riders"]),
            step=100000,
            help="If above 40M, double-check public figures."
            , key="rail_italo_riders"
        )
        if italo_riders > 40000000:
            st.warning("Above current public figures; double-check.")

        digital_share = st.slider(
            "% of purchases via app/web",
            0, 100, int(a["rail"]["digital_share_pct"]), key="rail_digital_share"
        ) / 100.0
        if digital_share < 0.2 or digital_share > 0.95:
            st.warning("Atypical digital share; verify.")

        eligible_share = st.slider(
            "% of tickets where donation UI is shown",
            0, 100, int(a["rail"]["eligible_share_pct"]), key="rail_eligible_share"
        ) / 100.0

        ask_type = st.radio(
            "Ask type",
            options=["€1 fixed", "€2 fixed", "€1 or €2 choice"],
            index=["€1 fixed", "€2 fixed", "€1 or €2 choice"].index(a["rail"]["ask_type"]),
            key="rail_ask_type"
        )
        choice_share_eur1 = 0.7
        if ask_type == "€1 or €2 choice":
            choice_share_eur1 = st.slider("% choosing €1 (else €2)", 0, 100, int(a["rail"]["choice_share_eur1_pct"]), key="rail_choice_share") / 100.0

        optin_web_1 = st.slider("Web/App opt-in for €1", 0, 100, int(a["rail"]["optin_web_1_pct"]), key="rail_optin_web1") / 100.0
        optin_web_2 = st.slider("Web/App opt-in for €2", 0, 100, int(a["rail"]["optin_web_2_pct"]), key="rail_optin_web2") / 100.0
        optin_pos = st.slider("Station POS opt-in", 0, 100, int(a["rail"]["optin_pos_pct"]), key="rail_optin_pos") / 100.0

        if optin_web_1 > 0.15 or optin_web_2 > 0.15 or optin_pos > 0.15:
            st.caption(badge("Aggressive assumption vs literature; run sensitivity.", color="yellow"))

        with st.popover("Seasonality (12 months multipliers)"):
            seasonality = []
            cols = st.columns(4)
            for i in range(12):
                seasonality.append(cols[i % 4].number_input(f"m{i+1}", min_value=0.1, max_value=2.0, value=float(a["rail"]["seasonality"][i]), step=0.05, key=f"rail_season_{i}"))

        processor = st.selectbox("Processor & fees", options=["Adyen Giving", "Stripe", "Nexi"], index=["Adyen Giving", "Stripe", "Nexi"].index(a["fees"]["processor"]), key="rail_processor")
        fee_rate = 0.0
        fee_fixed = 0.0
        if processor == "Adyen Giving":
            st.caption("Adyen covers all fees; donation in full to nonprofit.")
        else:
            fee_rate = st.number_input("% fee", min_value=0.0, max_value=5.0, value=float(a["fees"]["rate_pct"]), key="rail_fee_rate") / 100.0
            fee_fixed = st.number_input("Fixed € per donation", min_value=0.0, max_value=1.0, value=float(a["fees"]["fixed_eur"]), key="rail_fee_fixed")

    inputs = RailInputs(
        trenitalia_riders=trenitalia_riders,
        italo_riders=italo_riders,
        digital_share=digital_share,
        eligible_share=eligible_share,
        ask_type=ask_type,
        choice_share_eur1=choice_share_eur1,
        optin_web_1=optin_web_1,
        optin_web_2=optin_web_2,
        optin_pos=optin_pos,
        seasonality=seasonality,
        fee_rate=fee_rate,
        fee_fixed=fee_fixed,
        processor=processor,
    )
    st.session_state.rail_inputs = inputs

    monthly = compute_rail_monthly(inputs, months=months)

    # Charts
    st.markdown("Funnel: Riders → Exposed → Donors → € net")
    funnel_cols = ["riders", "eligible", "exposed_digital", "donors", "net"]
    annual_funnel = monthly.groupby("metric")["value"].sum().reindex(funnel_cols).reset_index()
    fig_funnel = px.funnel(annual_funnel, y="metric", x="value", title="Rail funnel (annual)")
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.markdown("Monthly net € with seasonality")
    monthly_net = monthly[(monthly["metric"] == "net") & (monthly["operator"] == "all")]
    fig_line = px.line(monthly_net, x="month", y="value", title="Rail monthly net €")
    st.plotly_chart(fig_line, use_container_width=True)

    # Bars: Trenitalia vs Italo
    bars = monthly[(monthly["metric"] == "net") & (monthly["operator"] != "all")]\
        .groupby("operator")["value"].sum().reset_index()
    fig_bars = px.bar(bars, x="operator", y="value", title="Annual net € by operator")
    st.plotly_chart(fig_bars, use_container_width=True)

    return monthly


def retail_tab() -> pd.DataFrame:
    st.subheader("Retail round-up module (Grocery & POS)")
    a = st.session_state.assumptions
    months = st.slider("Time period (months)", min_value=1, max_value=36, value=st.session_state.months, key="retail_months")
    st.session_state.months = months

    with st.expander("Inputs", expanded=True):
        method_label = st.radio("Estimation method", ["Market-top-down", "Retailer-direct"], index=0, key="retail_method")
        method = RetailMethod.TOP_DOWN if method_label == "Market-top-down" else RetailMethod.DIRECT

        monthly_spend = st.number_input("ISTAT monthly household spend (€)", min_value=0.0, value=float(a["retail"]["istat_monthly_spend_2023"]), key="retail_monthly_spend")
        grocery_share = st.slider("% household spend on grocery", 0, 100, int(a["retail"]["grocery_share_pct"]), key="retail_grocery_share") / 100.0
        avg_receipt = st.number_input("Average receipt (€)", min_value=1.0, value=float(a["retail"]["avg_receipt_eur"]), key="retail_avg_receipt")
        population_households = st.number_input("Households (for top-down)", min_value=0, value=int(a["retail"]["households"]), key="retail_households")

        daily_receipts = st.number_input("Daily receipts (per store)", min_value=0, value=int(a["retail"]["daily_receipts"]), key="retail_daily_receipts")
        stores = st.number_input("Stores", min_value=0, value=int(a["retail"]["stores"]), key="retail_stores")
        active_days = st.number_input("Active days/year", min_value=1, max_value=366, value=int(a["retail"]["active_days"]), key="retail_active_days")

        charm_prevalence = st.slider("Charm pricing prevalence", 0, 100, int(a["retail"]["charm_prevalence_pct"]), key="retail_charm_prev") / 100.0
        roundup_min = 0.01
        roundup_mode = 0.50
        roundup_max = 0.99
        st.caption("Round-up modeled as triangular(0.01, 0.50, 0.99)")

        optin = st.slider("Opt-in rate", 1, 12, int(a["retail"]["optin_pct"]), key="retail_optin") / 100.0
        if optin > 0.12:
            st.caption(badge("Aggressive assumption vs literature; run sensitivity.", color="yellow"))

        payment_card_share = st.slider("% card/contactless", 0, 100, int(a["retail"]["payment_card_share_pct"]), key="retail_card_share") / 100.0

        processor = st.selectbox("Processor & fees", options=["Adyen Giving", "Stripe", "Nexi"], index=["Adyen Giving", "Stripe", "Nexi"].index(a["fees"]["processor"]), key="retail_processor")
        fee_rate = 0.0
        fee_fixed = 0.0
        if processor == "Adyen Giving":
            st.caption("Adyen covers all fees; donation in full to nonprofit.")
        else:
            fee_rate = st.number_input("% fee", min_value=0.0, max_value=5.0, value=float(a["fees"]["rate_pct"]), key="retail_fee_rate") / 100.0
            fee_fixed = st.number_input("Fixed € per donation", min_value=0.0, max_value=1.0, value=float(a["fees"]["fixed_eur"]), key="retail_fee_fixed")

    inputs = RetailInputs(
        method=method,
        monthly_spend=monthly_spend,
        grocery_share=grocery_share,
        avg_receipt=avg_receipt,
        households=population_households,
        daily_receipts=daily_receipts,
        stores=stores,
        active_days=active_days,
        charm_prevalence=charm_prevalence,
        optin=optin,
        fee_rate=fee_rate,
        fee_fixed=fee_fixed,
        processor=processor,
        triangular_min=roundup_min,
        triangular_mode=roundup_mode,
        triangular_max=roundup_max,
        payment_card_share=payment_card_share,
    )
    st.session_state.retail_inputs = inputs

    monthly = compute_retail_monthly(inputs, months=months)

    st.markdown("Histogram of simulated round-up per transaction (10k samples)")
    samples = simulate_roundup_distribution(inputs, n=10000, seed=42)
    fig_hist = px.histogram(x=samples, nbins=50, title="Round-up per transaction (€)")
    fig_hist.update_xaxes(title_text="€ per transaction")
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("Funnel: transactions → opted-in → gross € → net of fees")
    funnel_metrics = ["transactions", "donors", "gross", "net"]
    wf = (
        monthly[(monthly["channel"] == "all") & (monthly["metric"].isin(funnel_metrics))]
        .groupby("metric")["value"]
        .sum()
        .reindex(funnel_metrics)
        .reset_index()
    )
    fig_wf = px.funnel(wf, y="metric", x="value", title="Retail funnel (annual)")
    st.plotly_chart(fig_wf, use_container_width=True)

    scenario = monthly[(monthly["metric"] == "net") & (monthly["channel"].isin(["in_store", "online"]))] \
        .groupby("channel")["value"].sum().reset_index()
    fig_scn = px.bar(scenario, x="channel", y="value", title="Annual net € by channel")
    st.plotly_chart(fig_scn, use_container_width=True)

    return monthly


def sensitivity_tab(rail_df: pd.DataFrame, retail_df: pd.DataFrame) -> None:
    st.subheader("Sensitivity")
    mc_toggle = st.checkbox("Run Monte Carlo (fast)", value=False)
    if mc_toggle:
        scenario = st.radio(
            "Scenario focus",
            ["Combined (rail + retail)", "Retail only"],
            key="mc_scenario_focus",
            horizontal=True,
        )
        include_rail = scenario == "Combined (rail + retail)"
        include_retail = True

        if include_rail and st.session_state.rail_inputs is None:
            st.warning("Please configure the Rail tab first to include rail in Monte Carlo.")
            return
        if include_retail and st.session_state.retail_inputs is None:
            st.warning("Please configure the Retail tab first to include retail in Monte Carlo.")
            return
        results = run_monte_carlo(
            st.session_state.rail_inputs,
            st.session_state.retail_inputs,
            st.session_state.months,
            include_rail=include_rail,
            include_retail=include_retail,
            iterations=2000,
            seed=123
        )
        fig = px.histogram(results, x="total_net", nbins=60, title="Monte Carlo distribution of total net €")
        st.plotly_chart(fig, use_container_width=True)
        perc = np.percentile(results["total_net"], [5, 50, 95])
        c1, c2, c3 = st.columns(3)
        c1.metric("5th %", euro(perc[0]))
        c2.metric("Median", euro(perc[1]))
        c3.metric("95th %", euro(perc[2]))
        st.caption("Scenario: {}".format("Retail only" if not include_rail else "Rail + Retail combined"))
    else:
        st.info("Use Monte Carlo toggle to explore uncertainty bands.")


def assumptions_tab() -> None:
    st.subheader("Assumptions (editable)")
    if st.button("Reset to source defaults"):
        st.session_state.assumptions = json.loads(json.dumps(DEFAULTS))
        st.rerun()

    a = st.session_state.assumptions
    st.markdown("### MSF Italy 2024 context")
    a["msf_italy"]["fundraising_2024_eur"] = st.number_input("MSF Italy fundraising 2024 (€)", min_value=0.0, value=float(a["msf_italy"]["fundraising_2024_eur"]), key="assump_msf2024")

    st.markdown("### Rail defaults")
    col1, col2 = st.columns(2)
    with col1:
        a["rail"]["trenitalia_riders"] = st.number_input("Trenitalia riders (default)", min_value=0, value=int(a["rail"]["trenitalia_riders"]), key="assump_trenitalia_riders")
        a["rail"]["italo_riders"] = st.number_input("Italo riders (default)", min_value=0, value=int(a["rail"]["italo_riders"]), key="assump_italo_riders")
        a["rail"]["digital_share_pct"] = st.slider("Digital share % (default)", 0, 100, int(a["rail"]["digital_share_pct"]), key="assump_rail_digital_share")
        a["rail"]["eligible_share_pct"] = st.slider("Eligible shown % (default)", 0, 100, int(a["rail"]["eligible_share_pct"]), key="assump_rail_eligible")
    with col2:
        a["rail"]["ask_type"] = st.selectbox("Ask type default", ["€1 fixed", "€2 fixed", "€1 or €2 choice"], index=["€1 fixed", "€2 fixed", "€1 or €2 choice"].index(a["rail"]["ask_type"]), key="assump_rail_ask_type")
        a["rail"]["choice_share_eur1_pct"] = st.slider("% choosing €1 if choice (default)", 0, 100, int(a["rail"]["choice_share_eur1_pct"]), key="assump_rail_choice_share")
        a["rail"]["optin_web_1_pct"] = st.slider("Web/App €1 opt-in % (default)", 0, 100, int(a["rail"]["optin_web_1_pct"]), key="assump_rail_optin_web1")
        a["rail"]["optin_web_2_pct"] = st.slider("Web/App €2 opt-in % (default)", 0, 100, int(a["rail"]["optin_web_2_pct"]), key="assump_rail_optin_web2")
        a["rail"]["optin_pos_pct"] = st.slider("POS opt-in % (default)", 0, 100, int(a["rail"]["optin_pos_pct"]), key="assump_rail_optin_pos")
    st.caption("Seasonality default multipliers:")
    cols = st.columns(6)
    for i in range(12):
        a["rail"]["seasonality"][i] = cols[i % 6].number_input(f"m{i+1}", min_value=0.1, max_value=2.0, value=float(a["rail"]["seasonality"][i]), step=0.05, key=f"assump_rail_season_{i}")

    st.markdown("### Retail defaults")
    col1, col2 = st.columns(2)
    with col1:
        a["retail"]["istat_monthly_spend_2023"] = st.number_input("ISTAT monthly spend 2023 (€)", min_value=0.0, value=float(a["retail"]["istat_monthly_spend_2023"]), key="assump_retail_spend_2023")
        a["retail"]["istat_monthly_spend_2024"] = st.number_input("ISTAT monthly spend 2024 (€)", min_value=0.0, value=float(a["retail"]["istat_monthly_spend_2024"]), key="assump_retail_spend_2024")
        a["retail"]["grocery_share_pct"] = st.slider("Grocery share %", 0, 100, int(a["retail"]["grocery_share_pct"]), key="assump_retail_grocery_share")
        a["retail"]["avg_receipt_eur"] = st.number_input("Average receipt (€)", min_value=1.0, value=float(a["retail"]["avg_receipt_eur"]), key="assump_retail_avg_receipt")
        a["retail"]["households"] = st.number_input("Households (base)", min_value=0, value=int(a["retail"]["households"]), key="assump_retail_households")
    with col2:
        a["retail"]["optin_pct"] = st.slider("Opt-in %", 0, 100, int(a["retail"]["optin_pct"]), key="assump_retail_optin_pct")
        a["retail"]["charm_prevalence_pct"] = st.slider("Charm pricing prevalence %", 0, 100, int(a["retail"]["charm_prevalence_pct"]), key="assump_retail_charm_prev")
        a["retail"]["payment_card_share_pct"] = st.slider("% card/contactless", 0, 100, int(a["retail"]["payment_card_share_pct"]), key="assump_retail_card_share")
        a["retail"]["daily_receipts"] = st.number_input("Daily receipts (per store)", min_value=0, value=int(a["retail"]["daily_receipts"]), key="assump_retail_daily_receipts")
        a["retail"]["stores"] = st.number_input("Stores", min_value=0, value=int(a["retail"]["stores"]), key="assump_retail_stores")
        a["retail"]["active_days"] = st.number_input("Active days/year", min_value=1, max_value=366, value=int(a["retail"]["active_days"]), key="assump_retail_active_days")

    st.markdown("### Fees defaults")
    a["fees"]["processor"] = st.selectbox("Default processor", ["Adyen Giving", "Stripe", "Nexi"], index=["Adyen Giving", "Stripe", "Nexi"].index(a["fees"]["processor"]), key="assumptions_processor")
    a["fees"]["rate_pct"] = st.number_input("Default fee %", min_value=0.0, max_value=5.0, value=float(a["fees"]["rate_pct"]), key="assump_fee_rate")
    a["fees"]["fixed_eur"] = st.number_input("Default fixed €", min_value=0.0, max_value=1.0, value=float(a["fees"]["fixed_eur"]), key="assump_fee_fixed")

    st.success("Assumptions updated in-session. Use 'Reset' to restore source defaults.")


def download_tab(rail_df: pd.DataFrame, retail_df: pd.DataFrame) -> None:
    st.subheader("Download")

    inputs_json = json.dumps(st.session_state.assumptions, indent=2)
    st.download_button("Download inputs.json", data=inputs_json, file_name="inputs.json", mime="application/json")

    monthly = pd.concat([rail_df.assign(initiative="rail"), retail_df.assign(initiative="retail")], ignore_index=True)
    csv_monthly = monthly.to_csv(index=False).encode("utf-8")
    st.download_button("Download monthly_projections.csv", data=csv_monthly, file_name="monthly_projections.csv", mime="text/csv")

    scenarios = monthly.groupby(["initiative", "metric"])  \
        ["value"].sum().reset_index()
    csv_scen = scenarios.to_csv(index=False).encode("utf-8")
    st.download_button("Download scenarios_summary.csv", data=csv_scen, file_name="scenarios_summary.csv", mime="text/csv")

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm

        if st.button("Generate one-pager PDF"):
            import io
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4)
            width, height = A4
            c.setFont("Helvetica-Bold", 14)
            c.drawString(2*cm, height-2*cm, "MSF Micro-donations Simulator – One-pager")

            rail_annual = rail_df[rail_df["metric"] == "net"]["value"].sum()
            retail_annual = retail_df[retail_df["metric"] == "net"]["value"].sum()
            total = rail_annual + retail_annual
            c.setFont("Helvetica", 11)
            c.drawString(2*cm, height-3*cm, f"Rail net €: {euro(rail_annual)}")
            c.drawString(2*cm, height-3.7*cm, f"Retail net €: {euro(retail_annual)}")
            c.drawString(2*cm, height-4.4*cm, f"Total net €: {euro(total)}")
            c.drawString(2*cm, height-5.4*cm, "Assumptions snapshot: see inputs.json")
            c.showPage()
            c.save()
            st.download_button("Download one-pager.pdf", data=buf.getvalue(), file_name="one_pager.pdf", mime="application/pdf")
    except Exception:
        st.warning("PDF engine not available. Use chart toolbar to download PNGs and combine with CSV exports.")


def main() -> None:
    init_state()

    tabs = st.tabs(["Overview", "Rail", "Retail", "Sensitivity", "Assumptions", "Sources", "Download"])

    # Compute base scenario for Overview
    with tabs[1]:
        rail_df = rail_tab()
    with tabs[2]:
        retail_df = retail_tab()
    with tabs[0]:
        overview_tab(rail_df, retail_df)
    with tabs[3]:
        sensitivity_tab(rail_df, retail_df)
    with tabs[4]:
        assumptions_tab()
    with tabs[5]:
        sources_tab()
    with tabs[6]:
        download_tab(rail_df, retail_df)


if __name__ == "__main__":
    main()


