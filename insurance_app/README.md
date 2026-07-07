# Etiqa Motor Vehicle Insurance System

A production-quality Streamlit prototype that simulates the complete motor insurance purchase journey:

Customer Registration -> Vehicle Information -> Coverage Selection -> Premium Calculation (OJK) -> Application Submission -> Document Verification -> Underwriting -> Approval/Rejection -> Policy Issued -> Analytics Dashboard

## Features

- End-to-end insurance workflow
- OJK-based premium calculation with CSV rate lookup
- Rule-based underwriting engine
- Automatic policy issuance and PDF generation
- SQLite + SQLAlchemy relational data model
- Auto-generated Indonesian dummy data (500 customers, 500 vehicles, 500 applications, 300 policies)
- Interactive analytics dashboard with Plotly
- Auto-initialization for DB, tables, OJK rates, and CSV datasets

## Project Structure

```text
insurance_app/
  app.py
  requirements.txt
  README.md
  config.py
  database.py
  premium_engine.py
  underwriting.py
  policy_generator.py
  dashboard.py
  utils.py
  database/
    insurance.db
  data/
    ojk_rates.csv
    customers.csv
    vehicles.csv
    applications.csv
    policies.csv
  pages/
    1_Home.py
    2_New_Application.py
    3_Premium_Calculation.py
    4_Underwriting.py
    5_Policy.py
    6_Dashboard.py
  assets/
    logo.png
    banner.png
```

## Installation

1. Ensure Python 3.12 is installed.
2. Open terminal in project folder:

```bash
cd insurance_app
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

The first run automatically:

- Creates `database/insurance.db`
- Creates all SQLite tables
- Creates `data/ojk_rates.csv` (if missing)
- Generates and inserts dummy data
- Exports CSV datasets to `data/`

## Deployment

### Streamlit Community Cloud

1. Push this folder to a Git repository.
2. Set app entry point to `app.py`.
3. Add dependencies from `requirements.txt`.
4. Deploy.

### Other Platforms

You can deploy with Docker, Azure App Service, or any VM that supports Python 3.12 + Streamlit.

## Notes

- This prototype is designed for technical assessment and portfolio demonstration.
- OJK rates are modeled from standard range references and used as midpoint simulation rates.
