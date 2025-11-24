# MSF Micro-donations Simulator

URL: https://msf-project-bocconi.streamlit.app

A production-ready Streamlit application for modeling potential revenue from micro-donation initiatives for Medici Senza Frontiere (MSF) Italia. The simulator evaluates two key initiatives:

1. **Rail micro-donations**: Opt-in €1/€2 donations during Trenitalia/Italo ticket checkout
2. **Retail round-up**: Round-up to the next euro at grocery and retail checkout points

## Features

- **Interactive modeling** with real-time calculations and visualizations
- **Monte Carlo simulation** for uncertainty analysis
- **A/B testing lab** for sample size calculations
- **Sensitivity analysis** to identify key drivers
- **Editable assumptions** with source links and reset functionality
- **Export capabilities**: CSV, JSON, and PDF reports
- **Compliance guardrails** ensuring opt-in only (no pre-ticked boxes)
- **Data provenance** sidebar with all source links

## Installation

### Requirements

- Python 3.10 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Project Structure

```
msf project/
├── app.py                 # Main Streamlit application and UI
├── defaults.py            # All assumptions, defaults, and source links
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── models/
│   ├── rail.py           # Rail donation calculations and validation
│   ├── retail.py         # Retail round-up calculations and simulation
│   ├── montecarlo.py     # Monte Carlo simulation engine
│   └── ab.py             # A/B testing sample size utilities
└── utils/
    ├── charts.py         # Chart generation helpers
    └── formatting.py     # Number and currency formatting utilities
```

## Application Tabs

### Overview

- **KPI tiles**: Total annual net €, Rail net €, Retail net €
- **Context metric**: % of MSF Italy 2024 fundraising
- **Stacked bar chart**: Visual comparison of Rail, Retail, and MSF baseline
- **Compliance reminder**: Opt-in only, no pre-ticked boxes

### Rail Module

Models micro-donations during train ticket purchases (Trenitalia + Italo).

**Inputs:**

- Annual riders (Trenitalia: 470M default, Italo: 22M default)
- Digital channel exposure (% app/web purchases)
- Eligible transactions (% where donation UI is shown)
- Ask type: €1 fixed, €2 fixed, or €1/€2 choice
- Opt-in rates by channel (Web/App €1, Web/App €2, Station POS)
- Seasonality multipliers (12 months)
- Payment processor and fees (Adyen Giving, Stripe, or Nexi)

**Outputs:**

- Funnel visualization: Riders → Exposed → Donors → € net
- Monthly net € line chart with seasonality
- Heatmap: Opt-in vs Avg donation → Annual € net
- Operator comparison: Trenitalia vs Italo annual net

**Formulas:**

```
monthly_riders = annual_riders × seasonality[month] / sum(seasonality)
eligible = monthly_riders × eligible_share
exposed_digital = eligible × digital_share
donors = exposed_digital × optin
gross = donors × avg_donation
net = gross × (1 - fee_rate) - fee_fixed × donors
```

### Retail Module

Models round-up donations at grocery and retail checkout.

**Two estimation methods:**

1. **Market-top-down (default)**

   - Based on ISTAT household spending data
   - Monthly spend × grocery share → annual grocery spend
   - Transactions inferred from average receipt size

2. **Retailer-direct**
   - Direct inputs: daily receipts, stores, active days
   - Transactions = daily_receipts × stores × active_days

**Inputs:**

- Estimation method (top-down or direct)
- Household spending data (ISTAT 2023/2024)
- Grocery share of household spend
- Average receipt size (€25.12 default from NielsenIQ)
- Charm pricing prevalence (80% default)
- Round-up distribution: Triangular(0.01, 0.50, 0.99)
- Opt-in rate (5% default)
- Payment mix (% card/contactless vs cash)
- Processor and fees

**Outputs:**

- Histogram of simulated round-up per transaction (10k samples)
- Waterfall chart: Transactions → Opted-in → Gross € → Net of fees
- Channel breakdown: In-store vs Online net €

**Formulas:**

```
transactions = (chosen method)
avg_roundup_effective = expected_roundup × charm_prevalence
donors = transactions × optin
gross = donors × avg_roundup_effective
net = gross × (1 - fee_rate) - fee_fixed × donors
```

### Sensitivity

- **Tornado chart**: One-way sensitivity on top drivers
- **Monte Carlo simulation** (optional toggle):
  - Randomizes: opt-in rates (Beta), seasonality, digital share, round-up distribution
  - Outputs: Distribution histogram with 5th, 50th, 95th percentiles

### A/B Testing Lab

Calculate required sample sizes for A/B tests of donation prompts.

**Inputs:**

- Baseline conversion rate
- Minimum detectable effect (MDE)
- Statistical power (default 0.8)
- Alpha level (default 0.05)
- Number of variants (2-4)
- Post-payment vs pre-payment prompt toggle

**Output:**

- Required sample size per variant (two-proportion Z-test power analysis)
- Bar chart visualization

### Assumptions

Editable defaults with source links and rationale.

**Sections:**

- MSF Italy 2024 fundraising context (€79.9M baseline)
- Rail defaults (riders, digital share, opt-in rates, seasonality)
- Retail defaults (ISTAT spending, grocery share, charm pricing, opt-in)
- Fee defaults (processor, rate, fixed amount)

**Features:**

- "Reset to source defaults" button
- All values editable in-app
- Source links provided for each assumption

### Download

Export functionality for analysis and reporting.

**Exports:**

- `inputs.json`: All current parameters and assumptions
- `monthly_projections.csv`: Monthly breakdown by initiative, operator, channel, metric
- `scenarios_summary.csv`: Aggregated totals by initiative and metric
- `one_pager.pdf`: Overview KPIs, top charts, and assumptions snapshot (requires reportlab)

## Default Assumptions & Sources

### MSF Italy Context

- **2024 fundraising**: €79.9M (100% private, ~95% individuals / ~5% companies/foundations)
- Source: MSF Italy Bilancio 2024

### Rail Data

- **Polo Passeggeri 2023**: 648M total riders
- **Trenitalia 2023**: ~470M riders
- **Italo + Itabus 2023**: 25M riders
- **Digital share**: 65% (editable, based on FS digital growth)
- **Opt-in defaults**: Web/App €1: 4%, Web/App €2: 2%, POS: 2%
- Sources: FS Group press releases, Italo CEO statements

### Retail Data

- **ISTAT monthly household spend 2023**: €2,738
- **ISTAT monthly household spend 2024**: €2,755
- **Grocery share**: 18% of household spend
- **Average receipt**: €25.12 (NielsenIQ 2024)
- **Shopping acts/year**: ~196 (NielsenIQ 2024)
- **Charm pricing prevalence**: 80% (70-90% range in literature)
- **Opt-in default**: 5% (1-12% range, based on checkout charity research)
- Sources: ISTAT, NielsenIQ grocery barometer, academic research

### Payment Processors

- **Adyen Giving**: 0% fees (donation in full to nonprofit)
- **Stripe/Nexi**: Custom fee structure (default 1.4% + €0.10)
- **Nexi "Dona Italia"**: QR code option for kiosks/stations

### Compliance

- **EU Consumer Rights Directive**: Prohibits pre-ticked boxes for paid extras
- All donations must be opt-in only
- App enforces this with validation and tooltips

## Validation & Warnings

The app includes guardrails to ensure realistic assumptions:

- **Italo riders > 40M**: Warning to double-check public figures
- **Digital share < 20% or > 95%**: Flagged as atypical
- **Opt-in > 15%**: Yellow badge warning "Aggressive assumption vs literature; run sensitivity"
- **Average round-up > €0.70**: Yellow badge warning for optimistic assumption
- **Pre-ticked boxes**: Hard error with EU directive link (if attempted)

## Technical Details

### Dependencies

- `streamlit`: Web application framework
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `scipy`: Statistical functions (Monte Carlo)
- `plotly.express`: Interactive charts
- `statsmodels`: A/B testing power analysis
- `pydantic`: Input validation
- `reportlab`: PDF generation (optional)

### Code Organization

- **Modular design**: Separate models for rail, retail, Monte Carlo, A/B testing
- **Pydantic validation**: Type-safe inputs with range checks
- **Session state**: Assumptions persist across tab navigation
- **Unique element keys**: All Streamlit widgets have unique keys to prevent ID conflicts

### Calculations

- **Deterministic base scenario**: Uses exact formulas with user inputs
- **Monte Carlo**: Optional stochastic simulation with configurable iterations
- **Monthly aggregation**: All calculations done monthly, then aggregated to annual
- **Fee handling**: Supports both percentage and fixed per-transaction fees

## Usage Tips

1. **Start with Overview**: Get a quick sense of total potential revenue
2. **Adjust assumptions**: Use the Assumptions tab to modify defaults, then return to Rail/Retail
3. **Run sensitivity**: Use Monte Carlo in Sensitivity tab to see uncertainty bands
4. **Export results**: Download CSVs for further analysis in Excel/Python
5. **A/B planning**: Use A/B Lab to plan experiments before implementation

## Ethics & Experience

The simulator emphasizes:

- **Opt-in only**: No pre-ticked boxes, respecting donor autonomy
- **Soft asks**: Aligns with MSF values of transparency and respect
- **Transparency**: All fees and net amounts clearly displayed
- **Evidence-based**: Defaults grounded in research and industry data

## Future Enhancements

Potential additions:

- Italian language toggle (structure already in place)
- Tax receipt aggregation notes (Italian ETS art. 83)
- Additional retailers/operators
- Time-series forecasting
- Donor retention modeling

## License

This project is developed for MSF Italia internal use.

## Contact

For questions or issues, please contact the MSF Italia fundraising team.

---

**Note**: This simulator is a modeling tool. Actual results will depend on implementation details, user experience design, and market conditions. Always validate assumptions with pilot tests before scaling.
