"""Compatibility wrapper

Keep a single canonical simulator implementation in financial_simulator.py
and re-export it here as FinancialPlanning for any code that still imports
financial_planning.FinancialPlanning.
"""

from financial_simulator import FinancialSimulator as FinancialPlanning

# Also expose the original name for convenience
from financial_simulator import FinancialSimulator

__all__ = ["FinancialPlanning", "FinancialSimulator"]
