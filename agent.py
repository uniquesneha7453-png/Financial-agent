import pandas as pd
import yaml
from datetime import datetime, timedelta

class FinancialAgent:
    def __init__(self, config_path="code/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def forecast_balance(self, balance, income, recurring, pending, essentials):
        """Compute net disposable balance."""
        return balance + income - (recurring + pending + essentials)

    def decide_payment(self, request):
        amount = request["requested_amount"]
        allows_partial = request["allows_partial_payment"]
        deadline = request["desired_completion_date"]
        request_date = request["request_date"]

        # Pull defaults from config
        balance = self.config["default_balance"]
        income = self.config["default_income"]
        recurring = self.config["default_recurring"]
        pending = self.config["default_pending"]
        essentials = self.config["default_essentials"]
        min_balance = self.config["min_balance"]

        net_disposable = self.forecast_balance(balance, income, recurring, pending, essentials)

        result = {"request_id": request["request_id"]}

        if net_disposable - amount >= min_balance:
            result.update({
                "amount_safe_to_pay": amount,
                "affordability_status": "Affordable now",
                "recommended_payment_method": "Pay in full",
                "payment_plan": f"{request_date} → {amount}",
                "earliest_date_for_full_payment": request_date,
                "spending_changes_needed": "None",
                "decision_explanation": "Expense fits within disposable balance."
            })
        elif allows_partial and net_disposable > min_balance:
            safe_amount = net_disposable - min_balance
            result.update({
                "amount_safe_to_pay": safe_amount,
                "affordability_status": "Affordable with a plan",
                "recommended_payment_method": "Installments",
                "payment_plan": f"{request_date} → {safe_amount}, {deadline} → remainder",
                "earliest_date_for_full_payment": deadline,
                "spending_changes_needed": "Reduce flexible spending",
                "decision_explanation": "Installments protect minimum balance."
            })
        else:
            result.update({
                "amount_safe_to_pay": 0,
                "affordability_status": "Affordable later",
                "recommended_payment_method": "Wait",
                "payment_plan": "None",
                "earliest_date_for_full_payment": deadline,
                "spending_changes_needed": "Cut discretionary expenses",
                "decision_explanation": "Full payment now risks essential expenses."
            })

        return result

    def run_batch(self, input_csv, output_csv):
        df = pd.read_csv(input_csv)
        outputs = [self.decide_payment(row) for _, row in df.iterrows()]
        out_df = pd.DataFrame(outputs)
        out_df.to_csv(output_csv, index=False)

        # Evaluation workflow
        mismatches = []
        expected_cols = [c for c in df.columns if c in out_df.columns]
        if expected_cols:
            for i, row in df.iterrows():
                for col in expected_cols:
                    if str(row[col]) != str(out_df.iloc[i][col]):
                        mismatches.append(
                            f"Request {row['request_id']}: expected {col}={row[col]}, got {out_df.iloc[i][col]}"
                        )

        with open(self.config["logging"]["log_file"], "w") as f:
            if mismatches:
                f.write("Evaluation mismatches:\n")
                f.write("\n".join(mismatches))
            else:
                f.write("Evaluation complete. No mismatches found.\n")

        return out_df
