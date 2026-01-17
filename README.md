# 🛡️ Property Catastrophe Reinsurance Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://alexanderdecosta-capital-retention-analytics-app-7o0yv5.streamlit.app/)

### 📊 Overview
This project is a quantitative decision-support tool designed to evaluate the impact of reinsurance structures on a property insurance portfolio. Using a 10,000-year stochastic simulation, the model analyzes how different "layers" of protection (Attachment and Limit) affect an insurer’s capital volatility and net loss profile.

**🔗 Live Dashboard:** [Reinsurance Risk Optimizer](https://alexanderdecosta-capital-retention-analytics-app-7o0yv5.streamlit.app/)

### 💡 Why This Is Useful
In the Canadian property market, managing "Tail Risk" is essential for both solvency and regulatory compliance (e.g., **OSFI B-9**). This tool provides immediate clarity on:

* **Risk Transfer Efficiency:** Visualizing exactly how much catastrophic volatility is moved from the Insurer's balance sheet to the Reinsurer.
* **PML Validation:** Determining if a chosen treaty limit is sufficient to cover a 1-in-250 year event (Probable Maximum Loss).
* **Pricing Insights:** Calculating the "Burn Cost" (Average Annual Loss) to establish a technical baseline for treaty negotiations.

---

### 🔬 Methodology
The model utilizes a **Frequency-Severity** approach to simulate 10,000 potential years of loss activity:

1. **Event Frequency ($N$):** Modeled via a **Poisson Distribution**.
   $$N \sim \text{Poisson}(\lambda)$$
   This represents the expected number of catastrophic events occurring within a one-year window.

2. **Event Severity ($X$):** Modeled via a **Pareto Distribution**.
   $$X \sim \text{Pareto}(\alpha, x_m)$$
   The "heavy-tailed" nature of the Pareto distribution is the industry standard for capturing "Black Swan" events, where a single event can result in multi-billion dollar losses.

3. **Treaty Logic:** The model applies a standard **Excess of Loss (XoL)** structure to the aggregate annual losses ($S$):
   * **Retention (Attachment):** The threshold the insurer pays before the treaty triggers.
   * **Limit:** The maximum capacity provided by the reinsurer.
   * **Net Loss:** The loss remaining with the insurer after reinsurance recoveries:
   $$\text{Net Loss} = S - \min(\max(0, S - \text{Retention}), \text{Limit})$$

---

### 🛠️ How to Use the Dashboard
The interactive interface allows users to stress-test the portfolio in real-time:

* **Adjust Parameters:** Use the sidebar to change the treaty **Attachment** and **Limit**.
* **Analyze EP Curves:** Compare the **Gross vs. Net Exceedance Probability (EP)** curves to see the "shaving" of tail risk across different return periods.
* **Review the 'Burn':** Monitor the **Average Annual Loss (AAL)** to understand the expected technical payout of the layer.
* **Trial View:** Inspect the "Stochastic Spikes" plot to see exactly which simulated years exhaust the treaty limit and where residual risk remains.

---

### 📂 Technical Structure
* `app.py`: The core simulation engine and Streamlit interface.
* `requirements.txt`: List of necessary Python libraries (NumPy, Matplotlib, Streamlit).
* `.gitignore`: Professional configuration to ensure a clean, production-ready repository.
