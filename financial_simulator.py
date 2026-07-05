import pandas as pd
import random


class FinancialSimulator:
    def __init__(self, initial_cash=1000, initial_income=2000, initial_expenses=1500, initial_debt=500,
                 debt_interest_rate=0.01, savings_interest_rate=0.001,
                 initial_investment=0, investment_return_rate=0.007):
        self.cash = initial_cash
        self.income = initial_income
        self.expenses = initial_expenses
        self.debt = initial_debt
        self.debt_interest_rate = debt_interest_rate  # Monthly debt interest rate
        self.savings_interest_rate = savings_interest_rate  # Monthly savings interest rate
        self.investment = initial_investment
        self.investment_return_rate = investment_return_rate  # Monthly investment return rate
        self.net_worth = self.cash + self.investment - self.debt  # Net worth includes investments
        self.month = 0

        # New: Goals tracking
        self.goals = {}  # Stores {'goal_name': {'target_amount': X, 'target_month': Y, 'type': 'net_worth'}}
        self.goal_history = pd.DataFrame(columns=['Month'])  # To store goal progress over time

        # History to track progress
        self.history = pd.DataFrame(columns=['Month', 'Cash', 'Income', 'Expenses', 'Debt', 'Investment', 'Net Worth'])
        self._record_state()

    def _record_state(self):
        new_row = {
            'Month': self.month,
            'Cash': self.cash,
            'Income': self.income,
            'Expenses': self.expenses,
            'Debt': self.debt,
            'Investment': self.investment,
            'Net Worth': self.net_worth
        }
        self.history = pd.concat([self.history, pd.DataFrame([new_row])], ignore_index=True)

        # Record goal progress as well
        goal_row = {'Month': self.month}
        for goal_name, goal_details in self.goals.items():
            if goal_details['type'] == 'net_worth':
                goal_row[f'{goal_name}_progress'] = self.net_worth
                goal_row[f'{goal_name}_target'] = goal_details['target_amount']
            elif goal_details['type'] == 'cash':
                goal_row[f'{goal_name}_progress'] = self.cash
                goal_row[f'{goal_name}_target'] = goal_details['target_amount']
            elif goal_details['type'] == 'investment':
                goal_row[f'{goal_name}_progress'] = self.investment
                goal_row[f'{goal_name}_target'] = goal_details['target_amount']

        if len(self.goals) > 0:
            self.goal_history = pd.concat([self.goal_history, pd.DataFrame([goal_row])], ignore_index=True)

    def set_goal(self, name, target_amount, target_month, goal_type='net_worth'):
        """Sets a financial goal."""
        if name in self.goals:
            print(f"Goal '{name}' already exists and will be updated.")
        self.goals[name] = {
            'target_amount': target_amount,
            'target_month': target_month,
            'type': goal_type,  # e.g., 'net_worth', 'cash', 'investment'
            'status': 'In Progress'  # Initial status
        }
        print(f"Goal '{name}' set: Target {goal_type} of ${target_amount:.2f} by Month {target_month}.")

    def update_goals(self):
        """Updates the status of all active goals."""
        for goal_name, goal_details in self.goals.items():
            if goal_details['status'] == 'In Progress' or goal_details['status'] == 'Achieved (Late)':
                current_value = 0
                if goal_details['type'] == 'net_worth':
                    current_value = self.net_worth
                elif goal_details['type'] == 'cash':
                    current_value = self.cash
                elif goal_details['type'] == 'investment':
                    current_value = self.investment

                if current_value >= goal_details['target_amount']:
                    if self.month <= goal_details['target_month']:
                        self.goals[goal_name]['status'] = 'Achieved'
                        print(f"  Goal '{goal_name}' ACHIEVED in Month {self.month} (Target Month: {goal_details['target_month']})!")
                    else:
                        self.goals[goal_name]['status'] = 'Achieved (Late)'
                        print(f"  Goal '{goal_name}' ACHIEVED LATE in Month {self.month} (Target Month: {goal_details['target_month']})!")
                elif self.month > goal_details['target_month'] and self.goals[goal_name]['status'] == 'In Progress':  # Only mark as missed if still 'In Progress'
                    self.goals[goal_name]['status'] = 'Missed'
                    print(f"  Goal '{goal_name}' MISSED in Month {self.month} (Target Month: {goal_details['target_month']})!")

    def invest(self, amount):
        if self.cash >= amount:
            self.cash -= amount
            self.investment += amount
            print(f"  Invested {amount:.2f}. Current investment: {self.investment:.2f}")
        else:
            print(f"  Not enough cash to invest {amount:.2f}. Current cash: {self.cash:.2f}")

    def pay_debt(self, amount):
        if self.cash >= amount:
            self.cash -= amount
            self.debt -= amount
            if self.debt < 0:  # Ensure debt doesn't go negative
                self.debt = 0
            print(f"  Paid {amount:.2f} towards debt. Current debt: {self.debt:.2f}")
        else:
            print(f"  Not enough cash to pay {amount:.2f} towards debt. Current cash: {self.cash:.2f}")

    def generate_random_event(self):
        event_type = random.choice(['expense', 'income', 'none'])
        if event_type == 'expense':
            amount = random.randint(50, 500)
            self.cash -= amount
            print(f"  Random Event: Unexpected expense of ${amount:.2f}")
        elif event_type == 'income':
            amount = random.randint(100, 700)
            self.cash += amount
            print(f"  Random Event: Bonus income of ${amount:.2f}")
        else:
            print("  Random Event: No special event this month.")

    def advance_month(self, invest_amount=0, pay_debt_amount=0):
        self.month += 1

        # Basic monthly operations (income - expenses)
        self.cash += self.income - self.expenses

        # Apply debt interest
        if self.debt > 0:
            debt_interest = self.debt * self.debt_interest_rate
            self.debt += debt_interest
            # print(f"  Debt interest applied: {debt_interest:.2f}") # For debugging

        # Apply savings interest (only if cash is positive)
        if self.cash > 0:
            savings_interest = self.cash * self.savings_interest_rate
            self.cash += savings_interest
            # print(f"  Savings interest applied: {savings_interest:.2f}") # For debugging

        # Apply investment returns
        if self.investment > 0:
            investment_gains = self.investment * self.investment_return_rate
            self.investment += investment_gains
            # print(f"  Investment gains: {investment_gains:.2f}") # For debugging

        # Generate a random event
        self.generate_random_event()

        # Apply decisions for the month
        if invest_amount > 0:
            self.invest(invest_amount)
        if pay_debt_amount > 0:
            self.pay_debt(pay_debt_amount)

        # Update net worth
        self.net_worth = self.cash + self.investment - self.debt

        # Update and check goals AFTER net worth is calculated
        self.update_goals()

        self._record_state()
        print(f"--- End of Month {self.month} ---")
        self.display_status()
        self.display_goals()  # Display goals status after each month

    def display_status(self):
        status_df = pd.DataFrame({
            'Metric': ['Cash', 'Income', 'Expenses', 'Debt', 'Investment', 'Net Worth', 'Debt Interest Rate', 'Savings Interest Rate', 'Investment Return Rate'],
            'Value': [f"{self.cash:.2f}", f"{self.income:.2f}", f"{self.expenses:.2f}", f"{self.debt:.2f}", f"{self.investment:.2f}", f"{self.net_worth:.2f}", f"{self.debt_interest_rate*100:.2f}%", f"{self.savings_interest_rate*100:.2f}%", f"{self.investment_return_rate*100:.2f}%"]
        })
        return status_df

    def display_goals(self):
        """Returns the current status of all financial goals as a DataFrame."""
        if not self.goals:
            return pd.DataFrame()
        
        goal_data = []
        for name, details in self.goals.items():
            current_value = 0
            if details['type'] == 'net_worth':
                current_value = self.net_worth
            elif details['type'] == 'cash':
                current_value = self.cash
            elif details['type'] == 'investment':
                current_value = self.investment

            goal_data.append({
                'Goal Name': name,
                'Type': details['type'],
                'Target Amount': f"${details['target_amount']:.2f}",
                'Current Value': f"${current_value:.2f}",
                'Target Month': details['target_month'],
                'Current Month': self.month,
                'Status': details['status']
            })
        goals_df = pd.DataFrame(goal_data)
        return goals_df

    def get_history(self):
        return self.history

    def get_goal_history(self):
        """Returns the history of goal progress."""
        return self.goal_history
