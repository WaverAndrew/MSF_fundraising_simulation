# MSF Micro-donations Simulator - Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Understanding the Tabs](#understanding-the-tabs)
4. [Tab-by-Tab Guide](#tab-by-tab-guide)
5. [Common Workflows](#common-workflows)
6. [Understanding the Results](#understanding-the-results)
7. [Tips and Best Practices](#tips-and-best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is This Tool?

The MSF Micro-donations Simulator is a web-based calculator that helps you estimate how much money MSF Italia could raise from two types of micro-donation programs:

1. **Rail Donations**: Small €1 or €2 donations when people buy train tickets online or at stations
2. **Retail Round-ups**: When shoppers round up their grocery bill to the next euro (e.g., if a bill is €24.37, they donate €0.63 to make it €25.00)

### Why Use This Tool?

- **Plan fundraising initiatives**: See potential revenue before launching programs
- **Test different scenarios**: What if we change the donation amount? What if more people opt in?
- **Compare options**: Which initiative (rail or retail) might raise more money?
- **Understand uncertainty**: See a range of possible outcomes, not just one number

### Key Concepts You Need to Know

**Opt-in**: People must actively choose to donate. The donation box cannot be pre-checked (this is required by EU law).

**Net vs Gross**: 
- **Gross** = Total money donated
- **Net** = Money after payment processing fees are deducted
- Example: If €100 is donated and fees are 1.4%, gross = €100, net = €98.60

**Time Period**: You can simulate anywhere from 1 month to 36 months (3 years). The default is 12 months (1 year).

---

## Getting Started

### First Steps

1. **Open the application** in your web browser
2. **Start with the Overview tab** to see the big picture
3. **Configure the Rail tab** with your assumptions
4. **Configure the Retail tab** with your assumptions
5. **Check the Overview tab again** to see combined results
6. **Use Sensitivity tab** to see uncertainty ranges
7. **Download your results** when ready

### Important Notes

- **The app remembers your settings** as you move between tabs
- **Changes update automatically** - you don't need to click "Calculate"
- **All amounts are in Euros (€)**
- **All percentages are shown as whole numbers** (e.g., 4% not 0.04)

---

## Understanding the Tabs

The application has 7 tabs at the top:

1. **Overview** - See total results from both initiatives
2. **Rail** - Configure and analyze train ticket donations
3. **Retail** - Configure and analyze grocery round-up donations
4. **Sensitivity** - See uncertainty and risk analysis
5. **Assumptions** - Edit default values used throughout the app
6. **Sources** - View data sources and references
7. **Download** - Export your results as files

---

## Tab-by-Tab Guide

### Tab 1: Overview

**Purpose**: See the combined results from both Rail and Retail initiatives at a glance.

**What You'll See**:

1. **Three Key Numbers (at the top)**:
   - **Total net €**: Combined revenue from both initiatives for your time period
   - **Rail net €**: Revenue from train ticket donations only
   - **Retail net €**: Revenue from grocery round-ups only

2. **Percentage of MSF Italy 2024 Fundraising**:
   - Shows what percentage your projected revenue represents compared to MSF Italy's total 2024 fundraising (€79.9M)
   - Example: If you see "2.5%", that means your projections equal 2.5% of MSF Italy's 2024 total

3. **Stacked Bar Chart**:
   - Visual comparison showing:
     - Rail donations (blue)
     - Retail donations (green)
     - MSF Italy 2024 baseline (gray) for context
   - Helps you see the scale of potential revenue

**How to Use This Tab**:

- This tab automatically updates when you change settings in Rail or Retail tabs
- Use it to quickly see if your initiatives are worth pursuing
- The chart helps you present results to others visually

**Important**: This tab shows results based on your current settings in Rail and Retail tabs. Make sure you've configured those tabs first!

---

### Tab 2: Rail Module

**Purpose**: Estimate revenue from micro-donations during train ticket purchases (Trenitalia and Italo).

#### Time Period Setting

At the top, you'll see a slider: **"Time period (months)"**

- **What it does**: Sets how many months to simulate (1 to 36 months)
- **Default**: 12 months (1 year)
- **How to use**: Drag the slider or type a number
- **Note**: This setting is shared with the Retail tab - changing it here changes it everywhere

#### Inputs Section (Click to expand/collapse)

All the settings you can adjust are in the "Inputs" section. Here's what each one means:
s
##### 1. Trenitalia Annual Riders
- **What it is**: Total number of people who ride Trenitalia trains in one year
- **Default**: 470,000,000 (470 million)
- **Source**: Based on 2023 FS Group data
- **How to change**: Type a new number or use the up/down arrows
- **Tip**: If you have more recent data, update this number

##### 2. Italo Annual Riders
- **What it is**: Total number of people who ride Italo trains in one year
- **Default**: 22,000,000 (22 million)
- **Source**: Based on 2023 Italo data
- **How to change**: Type a new number or use the up/down arrows
- **Warning**: If you enter more than 40 million, you'll see a warning to double-check your numbers

##### 3. % of Purchases via App/Web
- **What it is**: What percentage of tickets are bought online or through mobile apps (vs. at station counters)
- **Default**: 65%
- **Why it matters**: Donations are typically only shown for online/app purchases, not at physical counters
- **How to change**: Drag the slider left (lower %) or right (higher %)
- **Warning**: If you set it below 20% or above 95%, you'll see a warning that this is unusual

##### 4. % of Tickets Where Donation UI is Shown
- **What it is**: Even for online purchases, the donation prompt might not appear on every screen (e.g., some ticket types might skip it)
- **Default**: 90%
- **How to change**: Drag the slider
- **Tip**: 90% is a reasonable assumption - you might show it on most but not all ticket types

##### 5. Ask Type
- **What it is**: How much you ask people to donate
- **Options**:
  - **€1 fixed**: Always ask for exactly €1
  - **€2 fixed**: Always ask for exactly €2
  - **€1 or €2 choice**: Let people choose between €1 and €2
- **Default**: €1 fixed
- **How to change**: Click the radio button for your choice
- **If you choose "€1 or €2 choice"**: You'll see an additional slider asking what percentage choose €1 (default: 70%)

##### 6. Opt-in Rates (Three Separate Settings)

These are the most important numbers - they determine how many people actually donate:

- **Web/App opt-in for €1**: What % of people who see a €1 ask actually donate
  - **Default**: 4%
  - **Range**: 0% to 100%
  - **Reality check**: Research shows 2-6% is typical for checkout charity

- **Web/App opt-in for €2**: What % of people who see a €2 ask actually donate
  - **Default**: 2%
  - **Why lower?**: People are less likely to donate larger amounts
  - **Reality check**: Usually about half the rate of €1 donations

- **Station POS opt-in**: What % of people donate at physical ticket counters
  - **Default**: 2%
  - **Why lower?**: In-person donations typically have lower rates than online
  - **Note**: This is only used if you implement donations at physical stations

**Warning**: If you set any opt-in rate above 15%, you'll see a yellow warning that this is "aggressive" compared to research. Consider running sensitivity analysis.

##### 7. Seasonality (12 Months Multipliers)

- **What it is**: Train ridership varies by month (e.g., more in summer, less in January)
- **How it works**: Each month has a multiplier (default: 1.0 for all months = no variation)
- **How to access**: Click the "Seasonality (12 months multipliers)" popover button
- **How to use**:
  - **1.0** = Normal month
  - **1.15** = 15% more riders than average (e.g., summer months)
  - **0.9** = 10% fewer riders than average (e.g., January)
- **Example**: If you set June to 1.2 and January to 0.8, June will have 50% more riders than January
- **Tip**: The app automatically adjusts so the total still equals your annual rider count

##### 8. Processor & Fees

- **What it is**: Which payment company processes the donations and what fees they charge
- **Options**:
  - **Adyen Giving**: 0% fees (donation goes 100% to MSF)
  - **Stripe**: Custom fees (you set the % and fixed amount)
  - **Nexi**: Custom fees (you set the % and fixed amount)
- **Default**: Adyen Giving
- **If you choose Stripe or Nexi**: You'll see two additional fields:
  - **% fee**: Percentage of each donation (default: 1.4%)
  - **Fixed € per donation**: Fixed amount per transaction (default: €0.10)
  - **Example**: With 1.4% + €0.10, a €1 donation = €0.014 + €0.10 = €0.114 in fees, so MSF gets €0.886

#### Charts Section

After you configure inputs, you'll see three charts:

##### 1. Funnel Chart: "Riders → Exposed → Donors → € net"

- **What it shows**: How many people move through each stage
- **Stages**:
  - **Riders**: Total annual riders
  - **Eligible**: Riders who could see the donation prompt
  - **Exposed digital**: Riders who see it online/app
  - **Donors**: People who actually donate
  - **€ net**: Final revenue after fees
- **How to read**: Each bar gets smaller as people drop out at each stage
- **Use**: Shows where you're losing potential donors (e.g., if "Exposed" is much smaller than "Eligible", you might want to show the prompt more often)

##### 2. Monthly Net € Line Chart

- **What it shows**: How much revenue you get each month
- **X-axis**: Month (1-12 or however many months you set)
- **Y-axis**: Net revenue in Euros
- **How to read**: The line shows monthly variation due to seasonality
- **Use**: See which months generate the most revenue, plan cash flow

##### 3. Annual Net € by Operator (Bar Chart)

- **What it shows**: How much comes from Trenitalia vs. Italo
- **How to read**: Two bars side-by-side showing each operator's contribution
- **Use**: Understand which partnership is more valuable

#### How the Calculation Works

The app calculates:

1. **Monthly riders** = Annual riders × (seasonality for that month / sum of all seasonality)
2. **Eligible** = Monthly riders × % eligible
3. **Exposed digital** = Eligible × % digital purchases
4. **Donors** = Exposed digital × opt-in rate (based on ask type)
5. **Gross revenue** = Donors × average donation amount
6. **Net revenue** = Gross × (1 - fee %) - (fixed fee × number of donors)

This happens for each month, then all months are added together.

---

### Tab 3: Retail Module

**Purpose**: Estimate revenue from round-up donations at grocery stores and retail checkout.

#### Time Period Setting

Same as Rail tab - sets how many months to simulate (1-36).

#### Inputs Section

##### 1. Estimation Method

Choose how to calculate the number of transactions:

- **Market-top-down (default)**: Start with total household spending, then calculate transactions
  - **Use this if**: You want to estimate based on overall market data
  - **Requires**: Household spending data and number of households

- **Retailer-direct**: Start with specific store data
  - **Use this if**: You have actual data from specific stores
  - **Requires**: Daily receipts per store, number of stores, active days

##### 2. Market-Top-Down Method Inputs

If you chose "Market-top-down":

- **ISTAT Monthly Household Spend (€)**:
  - **What it is**: Average amount an Italian household spends per month
  - **Default**: €2,738 (2023 data)
  - **Source**: ISTAT (Italian national statistics)
  - **Alternative**: You can use €2,755 for 2024 data

- **% Household Spend on Grocery**:
  - **What it is**: What portion of household spending goes to groceries
  - **Default**: 18%
  - **How to change**: Drag the slider

- **Average Receipt (€)**:
  - **What it is**: Average amount per grocery shopping trip
  - **Default**: €25.12
  - **Source**: NielsenIQ 2024 grocery statistics
  - **How it's used**: Total grocery spending ÷ average receipt = number of transactions

- **Households (for top-down)**:
  - **What it is**: Number of households in your target market
  - **Default**: 1,000,000
  - **How to use**: Enter the actual number of households you're targeting
  - **Example**: If targeting all of Italy, use ~26 million households

##### 3. Retailer-Direct Method Inputs

If you chose "Retailer-direct":

- **Daily Receipts (per store)**:
  - **What it is**: Average number of transactions per store per day
  - **Default**: 500
  - **How to get**: Ask the retailer for their average daily transaction count

- **Stores**:
  - **What it is**: Number of stores participating
  - **Default**: 100
  - **How to use**: Enter the actual number of stores

- **Active Days/Year**:
  - **What it is**: How many days per year the stores are open and accepting donations
  - **Default**: 360 (stores closed ~5 days per year)
  - **How to use**: Adjust based on store hours (e.g., 365 for 24/7 stores, 300 for stores closed Sundays)

**Calculation**: Transactions = Daily receipts × Stores × Active days

##### 4. Charm Pricing Prevalence

- **What it is**: What percentage of prices end in .99, .95, etc. (e.g., €4.99 instead of €5.00)
- **Default**: 80%
- **Why it matters**: If prices end in .99, people can round up. If prices are already round numbers, there's nothing to round up.
- **Source**: Research shows 70-90% of retail prices use "charm pricing"
- **How to change**: Drag the slider (0-100%)

##### 5. Round-up Distribution

- **What it is**: How much people round up (ranges from €0.01 to €0.99)
- **Default model**: Triangular distribution with:
  - Minimum: €0.01
  - Most common (mode): €0.50
  - Maximum: €0.99
- **What this means**: Most people round up about €0.50, but it can be anywhere from 1 cent to 99 cents
- **Note**: This is automatically calculated - you don't need to change it

##### 6. Opt-in Rate

- **What it is**: What percentage of shoppers choose to round up
- **Default**: 5%
- **Range**: 1% to 12%
- **Reality check**: Research shows 3-8% is typical for checkout round-ups
- **Warning**: If you set above 12%, you'll see a warning that this is optimistic
- **How to change**: Drag the slider

##### 7. % Card/Contactless

- **What it is**: What percentage of payments are made with cards or contactless (vs. cash)
- **Default**: 70%
- **Why it matters**: Round-ups are easier to implement for card payments
- **Source**: Based on ECB/Bank of Italy payment studies
- **How to change**: Drag the slider

##### 8. Processor & Fees

Same as Rail tab - choose Adyen Giving (0% fees) or Stripe/Nexi (custom fees).

#### Charts Section

##### 1. Histogram: Round-up per Transaction

- **What it shows**: Distribution of how much people round up
- **X-axis**: Amount rounded up (€0.01 to €0.99)
- **Y-axis**: Number of transactions
- **How to read**: The chart shows a bell curve, with most round-ups around €0.50
- **Use**: Understand the average round-up amount

##### 2. Waterfall Chart: Transactions → Opted-in → Gross € → Net of Fees

- **What it shows**: How money flows through the system
- **Stages**:
  - **Transactions**: Total number of shopping trips
  - **Donors**: Transactions × opt-in rate
  - **Gross €**: Donors × average round-up
  - **Net**: Gross minus fees
- **How to read**: Each bar shows the value at that stage, with arrows showing the flow
- **Use**: See where money is lost (fees) and how many people actually donate

##### 3. Annual Net € by Channel (Bar Chart)

- **What it shows**: Revenue split between in-store and online
- **How to read**: Two bars showing each channel's contribution
- **Use**: Understand which channel generates more revenue

#### How the Calculation Works

1. **Calculate transactions**:
   - **Top-down**: (Households × Monthly spend × 12 × Grocery %) ÷ Average receipt
   - **Direct**: Daily receipts × Stores × Active days

2. **Calculate average round-up**:
   - Expected round-up = (0.01 + 0.50 + 0.99) ÷ 3 × Charm prevalence
   - Default: ~€0.50 × 80% = €0.40 average

3. **Calculate donors**: Transactions × Opt-in rate

4. **Calculate gross**: Donors × Average round-up

5. **Calculate net**: Gross × (1 - fee %) - (fixed fee × donors)

---

### Tab 4: Sensitivity

**Purpose**: Understand uncertainty and see a range of possible outcomes, not just one number.

#### What is Sensitivity Analysis?

Real-world results won't match your exact assumptions. Sensitivity analysis shows you:
- **Best case**: If things go better than expected
- **Worst case**: If things go worse than expected
- **Most likely**: The middle ground

#### Monte Carlo Simulation

**What it is**: The app runs 2,000 simulations with slightly different assumptions each time, then shows you the distribution of results.

**How to use**:

1. **First**: Make sure you've configured the Rail and Retail tabs (otherwise you'll see a warning)
2. **Check the box**: "Run Monte Carlo (fast)"
3. **Wait a few seconds**: The app will calculate 2,000 scenarios
4. **View results**: You'll see:
   - **Histogram**: A bell curve showing all possible outcomes
   - **Three key numbers**:
     - **5th percentile**: Only 5% of scenarios are worse than this (conservative estimate)
     - **Median (50th percentile)**: Half of scenarios are better, half are worse (most likely)
     - **95th percentile**: Only 5% of scenarios are better than this (optimistic estimate)

#### How to Interpret Results

**Example**: If you see:
- 5th %: €500,000
- Median: €750,000
- 95th %: €1,200,000

This means:
- **Worst case (5%)**: You'll likely raise at least €500,000
- **Most likely (median)**: You'll probably raise around €750,000
- **Best case (95%)**: You might raise up to €1,200,000, but don't count on it

**What gets randomized**:
- Opt-in rates (slightly higher or lower)
- Seasonality (some months busier than expected)
- Digital share (more or fewer online purchases)
- Charm pricing prevalence (more or fewer .99 prices)
- Round-up amounts (people round up more or less)

**Use this tab to**:
- Present realistic ranges to stakeholders (not just one number)
- Understand risk and uncertainty
- Plan for different scenarios
- Build confidence intervals for your projections

---

### Tab 5: Assumptions

**Purpose**: Edit the default values that appear throughout the app.

#### How This Tab Works

- **All values here become the new defaults** for the Rail and Retail tabs
- **Changes apply immediately** - when you go back to Rail/Retail tabs, you'll see your new defaults
- **"Reset to source defaults" button**: Restores all original values

#### Sections

##### 1. MSF Italy 2024 Context

- **MSF Italy fundraising 2024 (€)**: Used in Overview tab to show percentage comparison
- **Default**: €79,900,000
- **When to change**: If you have updated fundraising data

##### 2. Rail Defaults

All the default values for the Rail tab:
- Trenitalia riders
- Italo riders
- Digital share %
- Eligible shown %
- Ask type (€1, €2, or choice)
- Choice share (if using choice)
- Opt-in rates (€1, €2, POS)
- Seasonality multipliers (12 months)

##### 3. Retail Defaults

All the default values for the Retail tab:
- ISTAT monthly spend (2023 and 2024)
- Grocery share %
- Average receipt
- Households
- Opt-in %
- Charm pricing prevalence %
- Payment card share %
- Daily receipts, stores, active days

##### 4. Fees Defaults

- Default processor (Adyen, Stripe, or Nexi)
- Default fee % (if using Stripe/Nexi)
- Default fixed € (if using Stripe/Nexi)

#### When to Use This Tab

- **Setting up for your organization**: Change defaults to match your specific situation
- **Creating standard scenarios**: Set defaults that your team will use repeatedly
- **Updating with new data**: When you get updated statistics, change defaults here
- **Experimenting**: Try different default values to see impact

**Tip**: After changing defaults, click "Reset to source defaults" if you want to go back to original values.

---

### Tab 6: Sources

**Purpose**: View all data sources, references, and compliance information.

#### What You'll Find

1. **Key Sources**: Clickable links to all data sources used in the simulator:
   - MSF Italy financial reports
   - Train ridership statistics
   - ISTAT household spending data
   - NielsenIQ grocery statistics
   - Academic research on charm pricing
   - Payment processor documentation
   - EU Consumer Rights Directive

2. **Compliance & Ethics Section**:
   - Explanation of EU Consumer Rights Directive
   - Why opt-in is required (no pre-ticked boxes)
   - How this aligns with MSF values

3. **Notes on Data**:
   - Explanations of where each data point comes from
   - Notes on data quality and limitations
   - Guidance on interpreting the data

#### When to Use This Tab

- **Preparing presentations**: Reference sources for credibility
- **Understanding data quality**: See where numbers come from
- **Compliance questions**: Show stakeholders that the model follows EU regulations
- **Research**: Deep dive into the underlying data

---

### Tab 7: Download

**Purpose**: Export your results and assumptions as files for sharing, analysis, or reporting.

#### Available Downloads

##### 1. inputs.json

- **What it is**: A text file containing all your current assumptions and settings
- **Format**: JSON (JavaScript Object Notation) - readable text format
- **Contains**: Every number, percentage, and setting you've configured
- **Use cases**:
  - Save a scenario for later
  - Share exact assumptions with colleagues
  - Document your analysis
  - Reproduce results later

**How to use**: Click "Download inputs.json" - the file will download to your computer.

##### 2. monthly_projections.csv

- **What it is**: A spreadsheet file with month-by-month breakdown
- **Format**: CSV (Comma-Separated Values) - opens in Excel, Google Sheets, etc.
- **Contains**:
  - Each month (1-12 or your time period)
  - Each initiative (Rail, Retail)
  - Each metric (transactions, donors, gross, net)
  - Each operator/channel breakdown
- **Use cases**:
  - Create custom charts in Excel
  - Analyze monthly trends
  - Build cash flow projections
  - Share detailed data with finance team

**How to use**: Click "Download monthly_projections.csv" - open in Excel or Google Sheets.

##### 3. scenarios_summary.csv

- **What it is**: A simplified summary of total results
- **Format**: CSV spreadsheet
- **Contains**:
  - Total for each initiative (Rail, Retail)
  - Total for each metric (transactions, donors, gross, net)
  - Aggregated across all months
- **Use cases**:
  - Quick reference for key numbers
  - Include in presentations
  - Compare different scenarios side-by-side

**How to use**: Click "Download scenarios_summary.csv" - open in Excel or Google Sheets.

##### 4. one_pager.pdf

- **What it is**: A one-page PDF summary report
- **Format**: PDF document
- **Contains**:
  - Total net revenue (Rail, Retail, Combined)
  - Key assumptions reference
- **Use cases**:
  - Print for meetings
  - Email to stakeholders
  - Include in reports
  - Quick reference document

**How to use**: 
1. Click "Generate one-pager PDF"
2. Wait a moment for generation
3. Click "Download one-pager.pdf"

**Note**: If PDF generation fails, you'll see a message. In that case, use the chart download buttons (camera icon on charts) to save images, and combine with CSV files.

#### Tips for Using Downloads

- **Save multiple scenarios**: Download inputs.json for each scenario you test, name them clearly (e.g., "scenario1_conservative.json", "scenario2_optimistic.json")
- **Combine data**: Import CSV files into Excel to create custom analyses
- **Document your work**: Always download inputs.json to remember what assumptions you used
- **Share with team**: CSV files are easy to share and work with in common tools

---

## Common Workflows

### Workflow 1: Quick Estimate

**Goal**: Get a fast estimate of potential revenue

**Steps**:
1. Open the app
2. Go to **Rail tab** - accept all defaults, just note the "Rail net €" number
3. Go to **Retail tab** - accept all defaults, just note the "Retail net €" number
4. Go to **Overview tab** - see total and percentage of MSF fundraising
5. Done! You have a baseline estimate

**Time**: 2-3 minutes

---

### Workflow 2: Detailed Analysis

**Goal**: Create a comprehensive projection with your specific assumptions

**Steps**:
1. **Set time period**: In Rail tab, set months (e.g., 12 for one year)
2. **Configure Rail**:
   - Update rider numbers if you have current data
   - Set opt-in rates based on your expectations
   - Adjust seasonality if you know peak months
   - Choose payment processor and fees
3. **Configure Retail**:
   - Choose estimation method (top-down or direct)
   - Enter household data or store data
   - Set opt-in rate
   - Adjust charm pricing if needed
4. **Review Overview**: Check combined results
5. **Run Sensitivity**: Check Monte Carlo to see uncertainty
6. **Adjust if needed**: Go back and tweak assumptions
7. **Download results**: Save all files for your report

**Time**: 15-30 minutes

---

### Workflow 3: Compare Scenarios

**Goal**: Test "conservative" vs. "optimistic" assumptions

**Steps**:
1. **Create conservative scenario**:
   - Set lower opt-in rates (e.g., 3% instead of 5%)
   - Use lower rider numbers
   - Download inputs.json as "conservative.json"
2. **Create optimistic scenario**:
   - Set higher opt-in rates (e.g., 7% instead of 5%)
   - Use higher rider numbers
   - Download inputs.json as "optimistic.json"
3. **Compare results**: Look at Overview tab for each scenario
4. **Use Sensitivity**: Run Monte Carlo to see realistic ranges
5. **Present both**: Show stakeholders the range of possibilities

**Time**: 20-40 minutes

---

### Workflow 4: Update with New Data

**Goal**: Refresh projections with latest statistics

**Steps**:
1. Go to **Assumptions tab**
2. Update relevant defaults:
   - New rider numbers? Update Rail defaults
   - New household spending? Update Retail defaults
   - New opt-in research? Update opt-in defaults
3. Click "Reset to source defaults" if you want to start fresh
4. Go to **Rail** and **Retail** tabs - new defaults are already loaded
5. Review **Overview** with updated numbers
6. Download updated results

**Time**: 10-15 minutes

---

## Understanding the Results

### Key Metrics Explained

#### Net Revenue (Most Important)

**What it is**: Money that actually goes to MSF after all fees

**Why it matters**: This is what you can actually spend

**Example**: 
- Gross donations: €1,000,000
- Fees (1.4%): €14,000
- Net revenue: €986,000

#### Percentage of MSF Fundraising

**What it is**: How your projections compare to MSF Italy's total 2024 fundraising

**Why it matters**: Shows the scale and impact of the initiative

**Example**: 
- Your projection: €2,000,000
- MSF Italy 2024: €79,900,000
- Percentage: 2.5%

**Interpretation**: This initiative could add 2.5% to MSF Italy's fundraising, which is significant!

#### Opt-in Rate Impact

**What it is**: The single most important number for determining revenue

**Why it matters**: Small changes in opt-in rate create large changes in revenue

**Example** (Rail, 470M riders, €1 ask):
- 2% opt-in: €9.4M gross
- 4% opt-in: €18.8M gross (double!)
- 6% opt-in: €28.2M gross (triple!)

**Takeaway**: Focus on maximizing opt-in rate through good UX and messaging

#### Time Period Impact

**What it is**: Revenue scales linearly with time (mostly)

**Why it matters**: 6 months = roughly half of 12 months revenue

**Example**:
- 12 months: €1,000,000
- 6 months: ~€500,000
- 24 months: ~€2,000,000

**Note**: Seasonality can make this not perfectly linear, but it's close

---

## Tips and Best Practices

### 1. Start Conservative

- Use lower opt-in rates initially (3-4% for rail, 4-5% for retail)
- You can always increase later if you get better results
- Better to under-promise and over-deliver

### 2. Use Sensitivity Analysis

- Always run Monte Carlo before finalizing projections
- Present ranges, not single numbers
- Shows you've thought about uncertainty

### 3. Document Your Assumptions

- Download inputs.json for each scenario
- Note why you chose specific values
- Makes it easier to update later

### 4. Compare to Benchmarks

- Check the "Percentage of MSF Fundraising" metric
- If it's very high (>10%), double-check your assumptions
- If it's very low (<0.5%), consider if it's worth the effort

### 5. Test Multiple Scenarios

- Create at least 3 scenarios: conservative, realistic, optimistic
- Helps stakeholders understand the range of possibilities
- Builds confidence in your analysis

### 6. Focus on What You Can Control

- You can't control rider numbers or household spending
- You CAN control: opt-in rate (through UX), ask type, processor choice
- Optimize the things you can influence

### 7. Update Regularly

- Rider numbers change year-to-year
- Opt-in rates may improve as people get used to the feature
- Re-run projections quarterly or annually

### 8. Use the Charts

- Charts are easier to understand than numbers
- Use them in presentations
- They tell a story

---

## Troubleshooting

### Problem: "Numbers don't make sense"

**Possible causes**:
- Time period mismatch (check months setting)
- Forgot to configure Rail or Retail tabs
- Using wrong estimation method in Retail

**Solution**:
1. Check time period slider in Rail/Retail tabs
2. Make sure you've entered inputs in both tabs
3. Verify you're using the right method (top-down vs. direct)

---

### Problem: "Monte Carlo shows very different numbers"

**This is normal!** Monte Carlo randomizes assumptions, so results will vary.

**What to check**:
- Median should be close to your deterministic calculation
- If median is very different, check that you've configured Rail and Retail tabs first
- The range (5th to 95th percentile) shows uncertainty - wider range = more uncertainty

---

### Problem: "Can't download PDF"

**Possible causes**:
- PDF library not installed
- Browser blocking download

**Solution**:
- Use chart download buttons (camera icon) to save images
- Combine with CSV files manually
- Or use the CSV files directly in Excel/Google Sheets

---

### Problem: "Opt-in rates seem too high/low"

**Check**:
- Research shows 2-6% is typical for checkout charity
- 4% for €1 and 2% for €2 are reasonable defaults
- If you see warnings about "aggressive assumptions," consider lowering

**Solution**:
- Use sensitivity analysis to see impact of different rates
- Research similar programs for benchmarks
- Start conservative, adjust based on pilot results

---

### Problem: "Seasonality doesn't seem to work"

**Check**:
- Make sure you've set multipliers for all 12 months
- Values should be around 1.0 (0.8 to 1.2 is typical)
- The app automatically normalizes, so total still equals annual riders

**Solution**:
- Set summer months (June-August) to 1.1-1.2
- Set winter months (January) to 0.8-0.9
- Keep other months around 1.0

---

### Problem: "Retail calculations seem wrong"

**Check**:
- Are you using top-down or direct method?
- If top-down: Do you have the right number of households?
- If direct: Are daily receipts realistic? (500/day = ~20/hour for 24-hour store)

**Solution**:
- Verify your input numbers make sense
- Check that transactions = (annual grocery spend) ÷ (avg receipt)
- Or transactions = (daily receipts) × (stores) × (active days)

---

## Glossary

**Charm Pricing**: Prices ending in .99, .95, etc. (e.g., €4.99 instead of €5.00)

**Digital Share**: Percentage of purchases made online or through apps (vs. in-person)

**Eligible**: Transactions where the donation prompt could be shown

**Gross Revenue**: Total donations before fees are deducted

**Net Revenue**: Total donations after fees are deducted (what MSF actually receives)

**Opt-in Rate**: Percentage of people who see the donation prompt and choose to donate

**Processor**: Payment company that handles the transaction (Adyen, Stripe, Nexi)

**Round-up**: Donating the difference to make a total a round number (e.g., €24.37 → €25.00, donate €0.63)

**Seasonality**: How ridership or sales vary by month throughout the year

**Sensitivity Analysis**: Testing how results change when assumptions change

**Triangular Distribution**: A statistical model where values cluster around a most-likely number but can vary

---

## Final Notes

This simulator is a **planning tool**, not a guarantee. Actual results will depend on:
- Implementation quality (how well the donation prompt is designed)
- User experience (how easy it is to donate)
- Messaging (how compelling the ask is)
- Market conditions (economic factors, consumer behavior)
- Partnership execution (how well the integration works)

**Best practice**: Use this tool to:
- Set realistic expectations
- Compare different options
- Plan for different scenarios
- Communicate potential to stakeholders

But always remember: **Start with a pilot, measure real results, and adjust based on data.**

---

## Getting Help

If you have questions or issues:
1. Check this guide first
2. Review the Sources tab for data references
3. Check the Assumptions tab to understand defaults
4. Try the Sensitivity tab to see if uncertainty explains unexpected results

**Remember**: The app is designed to be intuitive. If something seems wrong, it's usually a misunderstanding of an input or assumption. Take your time, read the labels carefully, and don't hesitate to experiment with different values to see how they affect results.

---

*Last updated: Based on app version with 7 tabs (Overview, Rail, Retail, Sensitivity, Assumptions, Sources, Download)*

