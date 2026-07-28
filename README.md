# Financial-Literacy

This repository contains a small interactive Financial Planning Simulator built with Streamlit and a reference Jupyter notebook.

Key files
- dashboard.py — Streamlit dashboard (UI).
- financial_simulator.py — Canonical simulator implementation (preferred import).
- financial_planning.py — Compatibility wrapper that re-exports FinancialSimulator.
- Financial_Literacy.ipynb — Notebook version of the simulator for exploration.

What's new
- Added support for a "Family Monthly Income" input in the dashboard and simulator. This represents household or partner income that contributes to monthly cash flow. The dashboard exposes this as "Family Monthly Income (₹)" in the sidebar; the simulator includes it when calculating monthly cash (income + family_income - expenses) and in history/plots.

How to run
1. Install requirements:

   pip install -r requirements.txt

2. Run the Streamlit app:

   streamlit run dashboard.py

3. Open the notebook for exploration (optional):

   jupyter notebook Financial_Literacy.ipynb

Notes
- The canonical simulator implementation lives in financial_simulator.py. financial_planning.py is a small compatibility wrapper to preserve older imports.
- If you maintain external code that imports `financial_planning.FinancialPlanning`, it will keep working. Consider updating imports to `from financial_simulator import FinancialSimulator` in follow-up cleanup.

If you want I can also update DEPLOYMENT.md with a short note about this change.
