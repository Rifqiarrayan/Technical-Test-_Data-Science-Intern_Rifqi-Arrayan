from __future__ import annotations

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"
PAGES_DIR = BASE_DIR / "pages"

DB_PATH = DB_DIR / "insurance.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

OJK_RATES_PATH = DATA_DIR / "ojk_rates.csv"
CUSTOMERS_CSV_PATH = DATA_DIR / "customers.csv"
VEHICLES_CSV_PATH = DATA_DIR / "vehicles.csv"
APPLICATIONS_CSV_PATH = DATA_DIR / "applications.csv"
POLICIES_CSV_PATH = DATA_DIR / "policies.csv"

POLICY_OUTPUT_DIR = DATA_DIR / "policies_pdf"

APP_TITLE = "Etiqa Motor Vehicle Insurance System"
APP_SUBTITLE = "End-to-end prototype for insurance purchase journey"

ADMIN_FEE = 50_000
STAMP_DUTY = 10_000

INDONESIAN_BRANDS = [
    "Toyota",
    "Honda",
    "Suzuki",
    "Mitsubishi",
    "Hyundai",
    "Daihatsu",
    "BMW",
    "Mercedes",
    "Wuling",
]

APPLICATION_STATUSES = [
    "Submitted",
    "Document Verified",
    "Underwriting",
    "Approved",
    "Rejected",
    "Policy Issued",
]

RISK_LEVELS = ["Low", "Medium", "High"]

COVERAGE_TYPES = ["Comprehensive", "TLO"]
AREAS = ["Area 1", "Area 2", "Area 3"]
ADDITIONAL_COVERAGES = [
    "Flood",
    "Earthquake",
    "Riot",
    "Third Party Liability",
    "Personal Accident",
]
