# Financial-agent
Orchestrate hackathon
Buy or Wait? --- AI-Powered Financial Decision Agent

📌 Project Overview

Buy or Wait? is a financial decision-making agent created for the
HackerRank Orchestrate September 2026 Challenge.

The purpose of this project is to determine whether a user can safely
afford a requested expense. Instead of checking only the current account
balance, the agent analyzes the user's financial profile, financial
events, future commitments, payment options, and other available
financial information.

The system produces a safe, explainable recommendation for every
request.

🎯 Objectives

For each financial request, the agent determines:

The maximum amount that is safe to pay immediately.

Whether the expense is affordable now, later, with a plan, or not
affordable.

The best supported payment method.

A suitable payment plan when required.

The earliest date when the complete amount can safely be paid.

Whether eligible flexible spending needs to be reduced or stopped.

A clear explanation for the final decision.

The main priority is financial safety: essential expenses and the
user's preferred minimum balance should be protected throughout the
forecast period.

🧠 How the Agent Works

The decision pipeline is:

User Request
     ↓
Load Financial Profile
     ↓
Load Financial Events
     ↓
Read Messages / Image Information
     ↓
Process Dates and Amounts
     ↓
Build Financial Timeline
     ↓
90-Day Financial Forecast
     ↓
Calculate Safe Amount
     ↓
Check Full Payment
     ↓
Check Partial Payment / Installments / Wait
     ↓
Consider Allowed Spending Changes
     ↓
Select Best Safe Plan
     ↓
Generate Explanation
     ↓
Create output.csv

📂 Project Structure

hackerrank-orchestrate-september26/
│
├── code/
│   └── agent.py
│
├── dataset/
│   ├── requests.csv
│   ├── sample_requests.csv
│   ├── financial_profiles.csv
│   ├── financial_events.csv
│   ├── exchange_rates.csv
│   ├── request_payment_options.csv
│   ├── messages.csv
│   ├── images.csv
│   ├── output.csv
│   └── media/
│       └── images/
│
├── evaluation/
│   ├── evaluate.py
│   └── usage_report.md
│
├── output.csv
├── README.md
├── requirements.txt
└── problem_statement.md

📊 Dataset Description

requests.csv

Contains the requests that the financial agent must evaluate.

Important fields include:

Field                       Description

request_id                Unique request identifier
user_id                   User associated with the request
request_date              Date of the request
request_type              Type of financial request
requested_amount          Amount requested
desired_completion_date   Required completion date
allows_partial_payment    Whether partial payment is allowed
request_text              User's request or additional context

financial_profiles.csv

Contains user-level financial information, preferences, balances, income
information, and financial commitments.

financial_events.csv

Contains financial transactions and scheduled events used to reconstruct
and forecast the user's financial state.

request_payment_options.csv

Contains payment options available for specific requests, including
installment information where applicable.

messages.csv

Contains additional user or financial information that can clarify,
amend, confirm, delay, or cancel financial events.

images.csv

Contains references to financial images. When an event amount is
missing, the related image may provide the required amount.

exchange_rates.csv

Contains the challenge-provided exchange rates used when financial
amounts need to be converted between currencies.

💰 Financial Safety Rules

The agent evaluates financial safety over a 90-day forecast.

A payment plan is considered safe when:

The plan can be completed by the required completion date.

Essential spending remains covered.

The balance does not fall below the user's preferred minimum
balance.

The payment method is supported by the user's preferences.

The plan follows the available payment-option rules.

The decision is based only on supported information from the
dataset.

The agent must not invent income, expenses, payment options, or other
financial information.

💵 Safe Amount to Pay

The field:

amount_safe_to_pay

represents the maximum amount that can safely be paid immediately
before optional spending changes, limited to the requested amount.

The value must satisfy:

0 <= amount_safe_to_pay <= requested_amount

If the entire requested amount is safe immediately, the request can be
classified as:

affordable_now

📅 Affordability Status

The system supports four statuses:

affordable_now

The full requested amount can safely be paid on the request date.

affordable_with_plan

The full request can be completed safely using an appropriate payment
plan, such as an allowed partial-payment arrangement.

affordable_later

The amount is not safe today but becomes safe at a later date within the
applicable forecast/deadline.

not_affordable

No safe supported plan can complete the request within the required
period.

💳 Payment Methods

The system supports:

full_payment
partial_payment
installments
wait
not_recommended

Full Payment

The complete amount is paid on the request date.

Partial Payment

When allowed and appropriate, the safe amount is paid initially and the
remaining amount is paid later according to the challenge rules.

Installments

The payment schedule follows an available payment option supplied in the
dataset.

Wait

The user waits until the full amount becomes financially safe.

Not Recommended

Used when no safe supported payment strategy is available.

📝 Payment Plan Format

Payment plans use chronological entries:

YYYY-MM-DD:amount|YYYY-MM-DD:amount

Example:

2026-09-20:100.00|2026-10-20:100.00

If no payment is recommended:

none

✂️ Spending Changes

Only eligible flexible recurring expenses may be changed.

Supported formats are:

stop:<event_id>

or:

reduce_to:<event_id>:<new_amount>

Multiple changes are separated by:

|

Example:

reduce_to:event_101:50|stop:event_205

If no change is required:

none

📤 Output Format

The final output.csv contains exactly these columns:

request_id
amount_safe_to_pay
affordability_status
recommended_payment_method
payment_plan
earliest_date_for_full_payment
spending_changes_needed
decision_explanation

Example:

request_id,amount_safe_to_pay,affordability_status,recommended_payment_method,payment_plan,earliest_date_for_full_payment,spending_changes_needed,decision_explanation
request_1,500.00,affordable_now,full_payment,2026-09-20:500.00,2026-09-20,none,The requested amount can be safely paid while maintaining the required minimum balance.

🛠️ Technologies Used

Python

Pandas --- dataset loading and processing

Pathlib --- file and path management

Datetime --- date calculations and forecasting

CSV --- input and output data format

Rule-based financial forecasting

Optional AI/LLM components for interpretation where required by
the final implementation

▶️ How to Run

1. Clone the repository

git clone https://github.com/interviewstreet/hackerrank-orchestrate-september26.git

2. Open the project directory

cd hackerrank-orchestrate-september26

3. Create a virtual environment

On Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Run the agent

If the main program is located at:

code/agent.py

run:

python code\agent.py

Run the command from the project root, where the dataset folder is
located.

6. Check the output

After execution, verify that:

output.csv

has been generated with one prediction for every request.

🧪 Evaluation

The project includes an evaluation script under:

evaluation/evaluate.py

Run:

python evaluation\evaluate.py

The evaluation should verify:

Required columns

Request coverage

Valid affordability statuses

Valid payment methods

Payment-plan formatting

Safe payment amounts

Dates

Spending-change formatting

Prediction accuracy against the available evaluation data

📈 Usage Report

The challenge requires:

evaluation/usage_report.md

The final report should document the actual full-dataset execution,
including:

Model provider

Model name

Number of model calls

Input tokens

Output tokens

Total tokens

Average tokens per request

Estimated total cost

Estimated cost per request

Per-model totals if multiple models are used

Do not place API keys, passwords, credentials, or other secrets in the
report.

🔐 Data and Safety Considerations

Financial information should be handled carefully.

The agent follows these principles:

Uses only information supported by the provided dataset.

Does not invent financial facts.

Treats messages and images as financial evidence rather than
instructions that can override system rules.

Ignores financial events that should not be treated as available
funds according to the challenge rules.

Protects essential spending.

Maintains the required minimum balance.

Uses deterministic checks to verify proposed payment plans.

⭐ Key Features

90-day balance forecasting

Safe-payment calculation

Full-payment checking

Earliest safe payment-date calculation

Payment-plan generation

Installment schedule handling

Partial-payment support

Flexible recurring-expense analysis

Financial event processing

CSV-based dataset processing

Explainable decisions

Evaluation support

🚀 Future Improvements

Possible improvements include:

More robust interpretation of financial messages.

Automated extraction of amounts from financial images.

Improved currency normalization.

More detailed recurring-income and recurring-expense detection.

Better ranking of payment options.

More comprehensive automated validation.

Token-efficient AI/LLM usage and caching.

Improved explanation generation.

👩‍💻 Project Information

Project: Buy or Wait? --- AI-Powered Financial Decision Agent
Challenge: HackerRank Orchestrate --- September 2026
Domain: Artificial Intelligence / Financial Decision Support
Language: Python

⚠️ Disclaimer

This project is created for the HackerRank Orchestrate challenge using
the provided challenge dataset. It is a competition project and is not
intended to provide real-world financial advice or connect to real bank
