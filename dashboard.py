import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from financial_simulator import FinancialSimulator

# Configure page
st.set_page_config(page_title="Financial Literacy Simulator", layout="wide")

# Title
st.title("💰 Financial Literacy Simulator")
st.markdown("Learn financial management through interactive simulations!")

# Sidebar for initial setup
st.sidebar.header("⚙️ Setup Your Scenario")

# Scenario selection
scenario = st.sidebar.radio(
    "Choose a scenario:",
    ["Student", "Young Professional", "Freelancer", "Custom"]
)

# Define scenarios
scenarios = {
    "Student": {
        "initial_cash": 1000,
        "initial_income": 1500,
        "initial_expenses": 1200,
        "initial_debt": 2000,
        "debt_interest_rate": 0.02,
        "savings_interest_rate": 0.001,
        "initial_investment": 0,
        "investment_return_rate": 0.007,
    },
    "Young Professional": {
        "initial_cash": 5000,
        "initial_income": 4000,
        "initial_expenses": 2500,
        "initial_debt": 5000,
        "debt_interest_rate": 0.015,
        "savings_interest_rate": 0.002,
        "initial_investment": 1000,
        "investment_return_rate": 0.01,
    },
    "Freelancer": {
        "initial_cash": 3000,
        "initial_income": 3500,
        "initial_expenses": 2000,
        "initial_debt": 1000,
        "debt_interest_rate": 0.015,
        "savings_interest_rate": 0.001,
        "initial_investment": 2000,
        "investment_return_rate": 0.008,
    },
}

# Get scenario parameters
if scenario in scenarios:
    params = scenarios[scenario]
else:
    params = {
        "initial_cash": st.sidebar.number_input("Initial Cash (₹)", 1000),
        "initial_income": st.sidebar.number_input("Monthly Income (₹)", 2000),
        "initial_expenses": st.sidebar.number_input("Monthly Expenses (₹)", 1500),
        "initial_debt": st.sidebar.number_input("Initial Debt (₹)", 500),
        "debt_interest_rate": st.sidebar.slider("Debt Interest Rate (%)", 4.0, 10.0, 20.0) / 100,
        "savings_interest_rate": st.sidebar.slider("Savings Interest Rate (%)", 4.0, 6.0, 8.0) / 100,
        "initial_investment": st.sidebar.number_input("Initial Investment (₹)", 0),
        "investment_return_rate": st.sidebar.slider("Investment Return Rate (%)", 1.0, 10.0, 20.0, 30.0) / 100,
    }

# Initialize session state
if "simulator" not in st.session_state:
    st.session_state.simulator = FinancialSimulator(**params)
    st.session_state.month_decisions = []

# Main layout
col1, col2 = st.columns([3, 1])

with col2:
    st.subheader("📊 Current Status")
    sim = st.session_state.simulator
    st.metric("Current Month", sim.month)
    st.metric("Net Worth", f"₹{sim.net_worth:.2f}")
    st.metric("Cash", f"₹{sim.cash:.2f}")
    st.metric("Debt", f"₹{sim.debt:.2f}")
    st.metric("Investments", f"₹{sim.investment:.2f}")

with col1:
    st.subheader("💡 Financial Overview")
    overview_data = {
        "Metric": ["Cash", "Income", "Expenses", "Debt", "Investment", "Net Worth"],
        "Value": [
            f"₹{sim.cash:.2f}",
            f"₹{sim.income:.2f}",
            f"₹{sim.expenses:.2f}",
            f"₹{sim.debt:.2f}",
            f"₹{sim.investment:.2f}",
            f"₹{sim.net_worth:.2f}",
        ],
    }
    st.dataframe(pd.DataFrame(overview_data), hide_index=True, use_container_width=True)

# Monthly decisions
st.divider()
st.subheader("🎯 Make Monthly Decisions")

col1, col2, col3 = st.columns(3)

with col1:
    invest_amount = st.number_input(
        "Amount to Invest (₹)",
        min_value=0.0,
        step=100.0,
        value=0.0,
        help="Money to move from cash to investments"
    )

with col2:
    pay_debt_amount = st.number_input(
        "Amount to Pay Debt (₹)",
        min_value=0.0,
        step=100.0,
        value=0.0,
        help="Money to pay towards your debt"
    )

with col3:
    # Set goal
    goal_name = st.text_input("Goal Name (optional)", key=f"goal_{sim.month}")
    set_goal = st.checkbox("Set Goal for this month?")

if set_goal and goal_name:
    goal_target = st.number_input("Target Amount (₹)", min_value=0.0)
    goal_months = st.number_input("Months to achieve goal", min_value=1, value=12)

# Advance month button
if st.button("⏭️ Advance to Next Month", use_container_width=True, type="primary"):
    # Set goal if specified
    if set_goal and goal_name:
        st.session_state.simulator.set_goal(
            goal_name,
            goal_target,
            sim.month + goal_months,
            "net_worth"
        )
    
    # Advance month
    st.session_state.simulator.advance_month(
        invest_amount=invest_amount,
        pay_debt_amount=pay_debt_amount
    )
    st.rerun()

# Display goals if any
if st.session_state.simulator.goals:
    st.divider()
    st.subheader("🎪 Financial Goals")
    goal_data = []
    for name, details in st.session_state.simulator.goals.items():
        current_value = 0
        if details["type"] == "net_worth":
            current_value = st.session_state.simulator.net_worth
        elif details["type"] == "cash":
            current_value = st.session_state.simulator.cash
        elif details["type"] == "investment":
            current_value = st.session_state.simulator.investment
        
        progress_pct = (current_value / details["target_amount"]) * 100 if details["target_amount"] > 0 else 0
        
        goal_data.append({
            "Goal": name,
            "Target": f"₹{details['target_amount']:.2f}",
            "Current": f"₹{current_value:.2f}",
            "Status": details["status"],
            "Progress": f"{progress_pct:.1f}%"
        })
    
    st.dataframe(pd.DataFrame(goal_data), hide_index=True, use_container_width=True)

# Visualizations
st.divider()
st.subheader("📈 Historical Trends")

history_df = st.session_state.simulator.get_history()

if len(history_df) > 1:
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Net Worth", "Cash Flow", "Debt vs Investment"])
    
    with tab1:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(history_df["Month"], history_df["Net Worth"], marker="o", linewidth=2, color="green")
        ax.set_xlabel("Month")
        ax.set_ylabel("Net Worth (₹)")
        ax.set_title("Net Worth Over Time")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with tab2:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(history_df["Month"], history_df["Cash"], marker="o", label="Cash", linewidth=2)
        ax.plot(history_df["Month"], history_df["Income"], marker="s", label="Income", linewidth=2, linestyle="--")
        ax.plot(history_df["Month"], history_df["Expenses"], marker="^", label="Expenses", linewidth=2, linestyle="--")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Cash Flow Analysis")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with tab3:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(history_df["Month"], history_df["Debt"], marker="o", label="Debt", linewidth=2, color="red")
        ax.plot(history_df["Month"], history_df["Investment"], marker="s", label="Investment", linewidth=2, color="blue")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")
        ax.set_title("Debt vs Investment Strategy")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

# Download history
st.divider()
col1, col2 = st.columns(2)

with col1:
    csv = history_df.to_csv(index=False)
    st.download_button(
        label="📥 Download History as CSV",
        data=csv,
        file_name=f"financial_simulator_history_month_{sim.month}.csv",
        mime="text/csv"
    )

with col2:
    if st.button("🔄 Reset Simulation"):
        st.session_state.simulator = FinancialSimulator(**params)
        st.rerun()

# Footer
st.divider()
st.markdown("""
### 📚 Tips for Financial Success:
1. **Balance Debt & Investment**: Pay off high-interest debt first, then invest
2. **Set Realistic Goals**: Achievable targets keep you motivated
3. **Track Progress**: Monitor your net worth growth over time
4. **Plan Ahead**: Unexpected events happen - keep emergency savings
5. **Diversify**: Don't put all money in one place

*Happy learning! 💡*
""")
