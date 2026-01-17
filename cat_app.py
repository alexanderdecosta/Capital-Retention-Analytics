import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#np.random.seed(42)

st.set_page_config(page_title="Reinsurance Risk Optimizer", layout="wide")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Model Parameters")
avg_events = st.sidebar.slider("Avg Events per Year (Poisson λ)", 0.5, 5.0, 2.0)
tail_risk = st.sidebar.slider("Tail Risk (Pareto Alpha)", 1.01, 2.5, 1.5)
seed_cost = st.sidebar.number_input("Average Storm Cost ($M)", value=50)

st.sidebar.header("Treaty Structure")
retention = st.sidebar.number_input("Retention ($M)", value=400)
limit = st.sidebar.number_input("Limit ($M)", value=2800)

# --- THE ENGINE ---
num_years = 10000
events = np.random.poisson(avg_events, num_years)
annual_losses = []

for n in events:
    if n > 0:
        storm_costs = (np.random.pareto(tail_risk, n) + 1) * seed_cost
        annual_losses.append(np.sum(storm_costs))
    else:
        annual_losses.append(0)

annual_losses = np.array(annual_losses)
payouts = np.clip(annual_losses - retention, 0, limit)

# --- CALCULATIONS ---
aal = np.mean(payouts)
attach_prob = np.mean(payouts > 0)
exhaust_prob = np.mean(payouts == limit)
pml_100 = np.percentile(annual_losses, 99)
pml_250 = np.percentile(annual_losses, 99.6)

# --- DASHBOARD UI ---
st.title("Catastrophe Reinsurance Optimizer")
st.markdown("### Interactive Stochastic Risk Model for Canadian Perils")

# Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Expected Payout (AAL)", f"${aal:.2f}M")
col2.metric("Attach Prob.", f"{attach_prob*100:.1f}%")
col3.metric("Exhaust Prob.", f"{exhaust_prob*100:.1f}%")
col4.metric("1-in-100 PML", f"${pml_100:.1f}M")
col5.metric("1-in-250 PML", f"${pml_250:.1f}M")

# Create a 2x2 grid of plots
fig, ax = plt.subplots(2, 2, figsize=(16, 12)) # Height increased for two rows

# --- PREPARE DATA ---
sorted_losses = np.sort(annual_losses)[::-1]
sorted_payouts = np.sort(payouts)[::-1]
net_losses = annual_losses - payouts
sorted_net = np.sort(net_losses)[::-1]
prob = np.arange(1, num_years + 1) / num_years

# --- ROW 1, COL 1: ANNUAL AGGREGATE LOSS (GROSS) ---
ax[0, 0].plot(sorted_losses, prob, color='blue', linewidth=2)
ax[0, 0].set_yscale('log')
ax[0, 0].set_title("Gross Loss (Insurer View)", fontweight='bold')
ax[0, 0].set_xlabel("Loss Amount ($M)")
ax[0, 0].set_ylabel("Annual Probability (Log Scale)")
ax[0, 0].axvline(pml_250, color='purple', linestyle=':', label=f'1-in-250: ${pml_250:,.0f}M')
ax[0, 0].grid(True, which="both", ls="-", alpha=0.2)
ax[0, 0].legend(fontsize='small')

# --- ROW 1, COL 2: NET LOSS VS GROSS LOSS ---
ax[0, 1].plot(sorted_losses, prob, color='blue', alpha=0.3, label='Gross Loss')
ax[0, 1].plot(sorted_net, prob, color='green', linewidth=2, label='Net Loss (Insurer)')
ax[0, 1].set_yscale('log')
ax[0, 1].set_title("Net Loss vs Gross Loss", fontweight='bold')
ax[0, 1].set_xlabel("Loss Amount ($M)")
ax[0, 1].set_ylabel("Annual Probability (Log Scale)")
ax[0, 1].axvline(retention, color='red', linestyle='--', label=f'Retention: ${retention:,.0f}M')
ax[0, 1].axvline(retention + limit, color='orange', linestyle='--', label='Exhaustion Point')
ax[0, 1].grid(True, which="both", ls="-", alpha=0.2)
ax[0, 1].legend(fontsize='small')

# --- ROW 2, COL 1: REINSURER PAYOUTS (THE BURN) ---
ax[1, 0].plot(sorted_payouts, prob, color='green', linewidth=2)
ax[1, 0].set_yscale('log')
ax[1, 0].set_title("Reinsurer Payout (The Burn)", fontweight='bold')
ax[1, 0].set_xlabel("Payout Amount ($M)")
ax[1, 0].set_ylabel("Annual Probability (Log Scale)")
ax[1, 0].axvline(aal, color='orange', label=f'Burn Cost: ${aal:.1f}M')
ax[1, 0].grid(True, which="both", ls="-", alpha=0.2)
ax[1, 0].legend(fontsize='small')

# --- ROW 2, COL 2: STOCHASTIC EVENTS (THE SPIKES) ---
ax[1, 1].scatter(range(num_years), annual_losses, alpha=0.2, s=5, color='grey', label='Gross Loss')
ax[1, 1].scatter(range(num_years), payouts, alpha=0.7, s=5, color='#2ca02c', label='Reinsurer Payout')
ax[1, 1].axhline(retention, color='red', linestyle='--', linewidth=1, label='Retention')
ax[1, 1].axhline(retention + limit, color='darkgreen', linestyle='--', linewidth=1, label='Limit Exhausted')
ax[1, 1].fill_between(range(num_years), retention, retention + limit, color='green', alpha=0.05)
ax[1, 1].set_title("Trial View: Risk Transfer", fontweight='bold')
ax[1, 1].set_xlabel("Simulated Year")
ax[1, 1].set_ylabel("Loss Amount ($M)")
ax[1, 1].set_ylim(0, (retention + limit) * 1.5) 
ax[1, 1].legend(loc='upper right', fontsize='x-small')
ax[1, 1].grid(True, axis='y', alpha=0.2)

# Global layout fix to prevent overlapping labels
plt.tight_layout(pad=4.0)
st.pyplot(fig)

st.info("**Insight:** The '1-in-250 Year' event is the regulatory capital standard in Canada. If your Retention + Limit is less than the 1-in-250 PML, the insurer may be under-protected.")