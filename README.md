🛡️ Property Catastrophe Reinsurance Optimizer
📊 Overview
This project is a quantitative decision-support tool designed to evaluate the impact of reinsurance structures on a property insurance portfolio. Using a 10,000-year stochastic simulation, the model analyzes how different "layers" of protection (Attachment and Limit) affect an insurer’s capital volatility and net loss profile.

💡 Why This Is Useful
In the Canadian property market, managing "Tail Risk" is essential for both solvency and regulatory compliance (e.g., OSFI B-9). This tool provides immediate clarity on:

Risk Transfer Efficiency: Visualizing how much catastrophic volatility is moved from the Insurer's balance sheet to the Reinsurer.

PML Validation: Determining if a chosen treaty limit is sufficient to cover a 1-in-250 year event (Probable Maximum Loss).

Pricing Insights: Calculating the "Burn Cost" (Average Annual Loss) to establish a technical baseline for treaty negotiations.

🔬 Methodology
The model utilizes a Frequency-Severity approach to simulate 10,000 potential years of loss activity:

Event Frequency: Modeled via a Poisson Distribution, representing the expected number of catastrophic claims per year.

Event Severity: Modeled via a Pareto Distribution. This "heavy-tailed" distribution is the industry standard for capturing "Black Swan" events where a single storm can cause multi-billion dollar losses.

Treaty Logic: The model applies a standard "Excess of Loss" (XoL) structure:

Retention (Attachment): The amount the insurer pays before the treaty kicks in.

Limit: The maximum capacity provided by the reinsurer.

Net Loss: The actual loss remaining with the insurer after reinsurance recoveries.

🛠️ How to Use the Dashboard
The interactive Streamlit interface allows users to stress-test the portfolio in real-time:

Adjust Parameters: Use the sidebar to change the treaty Attachment and Limit.

Analyze EP Curves: Compare the Gross vs. Net Exceedance Probability (EP) curves to see the "shaving" of tail risk.

Review the 'Burn': Monitor the Average Annual Loss (AAL) to understand the expected payout of the layer.

Trial View: Inspect the "Stochastic Spikes" plot to see exactly which simulated years exhaust the treaty limit.

📂 Technical Structure
cat_app.py: The core simulation engine and Streamlit interface.

requirements.txt: List of necessary Python libraries (NumPy, Matplotlib, Streamlit).

.gitignore: Professional configuration to ensure a clean, production-ready repository.
