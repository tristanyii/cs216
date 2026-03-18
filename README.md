# Evaluating Probability Accuracy of Kalshi Event-Based Prediction Markets

**Course:** CS 216: Everything Data  
**Date:** February 18, 2026  

**Group Members:**  
- Kevin Fan (kdf32)  
- Tristan Yi (tty3)  
- Marcus McFadden (mdm144)  
- Brianna Yang (bcy5)  
- Kambi Kanu (kok6)  

---

## Overview

This project investigates whether prediction markets—specifically Kalshi—produce well-calibrated probabilities for real-world events. Kalshi is a U.S.-based event contract exchange where users trade binary “Yes” or “No” contracts priced between 1 and 99 cents, representing implied probabilities.

Despite being legal nationwide, prediction markets like Kalshi face criticism for resembling gambling platforms. This project approaches the topic empirically, evaluating whether these markets provide reliable forecasts rather than speculation.

---

## Research Question

**Are the market prices of Kalshi predictions well-calibrated relative to their outcomes?**

### Definition of Calibration
A prediction market is *well-calibrated* if:
- Events priced at **x cents** correspond to approximately an **x% probability** of occurring.

**Example:**  
If contracts closing around 70 cents are well-calibrated, then about 70% of those events should resolve to “Yes.”

---

## Justification

### Substantial
This project evaluates whether market-implied probabilities reflect true likelihoods. It goes beyond basic modeling by requiring:
- Data aggregation from APIs  
- Cleaning and preprocessing  
- Statistical validation  

This enables a deeper understanding of prediction markets as forecasting tools.

### Feasible
Kalshi provides a public API with historical market data, including:
- Contract prices  
- Trade activity  
- Final outcomes  

We have already successfully accessed sample data, confirming feasibility.

### Relevant
Prediction markets are increasingly visible in media and public discourse. This project contributes to ongoing debates about:
- Market legitimacy  
- Regulation  
- Real-world applications of probabilistic forecasting  

---

## Data Sources

We use Kalshi’s historical market data API:

- https://docs.kalshi.com/api-reference/historical/get-historical-market  
- https://docs.kalshi.com/getting_started/quick_start_market_data  

### Key Variables
- `last_price_dollars`: Final market price (implied probability)  
- `result`: Outcome of the event (Yes/No)  
- `status`: Filtered to `"finalized"` markets only  

This allows us to directly compare predicted probabilities with actual outcomes.

---

## Methodology

### Data Wrangling (Module 4)
- Clean and structure API data  
- Handle missing values  
- Filter finalized markets  
- Prepare data for probability binning  

### Visualization (Module 3)
- Calibration plots (predicted vs. actual outcomes)  
- Histograms of probability distributions  

### Statistical Inference (Module 7)
- Hypothesis testing (t-tests)  
- Confidence intervals  
- Analysis of calibration error  
- Detection of systemic bias  

---

## Expected Analysis

We will:
- Bin contracts by predicted probability  
- Compare predicted vs. observed frequencies  
- Evaluate whether deviations are statistically significant  

---

## Project Status

**No changes have been made to the research question or overall project scope since the initial proposal.**

---

## AI Disclosure

- **Tool Used:** ChatGPT v5.2 (chatgpt.com)  
- **Usage:**  
  - Reviewed writing  
  - Provided feedback based on rubric  
  - Suggested improvements for clarity and structure  
