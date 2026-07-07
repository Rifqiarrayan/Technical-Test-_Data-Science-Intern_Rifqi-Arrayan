from __future__ import annotations

import json
import random
import uuid
from datetime import date, datetime, timedelta
from typing import Iterable

import pandas as pd
from faker import Faker
from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

from config import (
    ADDITIONAL_COVERAGES,
    ADMIN_FEE,
    APPLICATIONS_CSV_PATH,
    APPLICATION_STATUSES,
    AREAS,
    COVERAGE_TYPES,
    CUSTOMERS_CSV_PATH,
    DB_DIR,
    DB_PATH,
    DB_URL,
    OJK_RATES_PATH,
    POLICIES_CSV_PATH,
    POLICY_OUTPUT_DIR,
    STAMP_DUTY,
    VEHICLES_CSV_PATH,
)


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    nik: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(16), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(String(24), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    applications: Mapped[list[Application]] = relationship("Application", back_populates="customer")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vehicle_uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    brand: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    plate_number: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String(32), nullable=False)
    vehicle_usage: Mapped[str] = mapped_column(String(32), nullable=False)
    vehicle_price: Mapped[float] = mapped_column(Float, nullable=False)
    area: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped[Customer] = relationship("Customer")
    applications: Mapped[list[Application]] = relationship("Application", back_populates="vehicle")


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    coverage_type: Mapped[str] = mapped_column(String(24), nullable=False)
    area: Mapped[str] = mapped_column(String(16), nullable=False)
    additional_coverages: Mapped[list[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="Submitted")
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped[Customer] = relationship("Customer", back_populates="applications")
    vehicle: Mapped[Vehicle] = relationship("Vehicle", back_populates="applications")
    premium_result: Mapped[PremiumResult | None] = relationship("PremiumResult", back_populates="application", uselist=False)
    underwriting_result: Mapped[UnderwritingResult | None] = relationship("UnderwritingResult", back_populates="application", uselist=False)
    policy: Mapped[Policy | None] = relationship("Policy", back_populates="application", uselist=False)


class PremiumResult(Base):
    __tablename__ = "premium_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), unique=True, nullable=False)
    ojk_rate: Mapped[float] = mapped_column(Float, nullable=False)
    basic_premium: Mapped[float] = mapped_column(Float, nullable=False)
    additional_coverage_fee: Mapped[float] = mapped_column(Float, nullable=False)
    admin_fee: Mapped[float] = mapped_column(Float, nullable=False, default=ADMIN_FEE)
    stamp_duty: Mapped[float] = mapped_column(Float, nullable=False, default=STAMP_DUTY)
    total_premium: Mapped[float] = mapped_column(Float, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    application: Mapped[Application] = relationship("Application", back_populates="premium_result")


class UnderwritingResult(Base):
    __tablename__ = "underwriting_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), unique=True, nullable=False)
    vehicle_age: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    decision: Mapped[str] = mapped_column(String(24), nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    application: Mapped[Application] = relationship("Application", back_populates="underwriting_result")


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), unique=True, nullable=False)
    policy_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    premium_amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="Issued")
    generated_pdf: Mapped[bool] = mapped_column(Boolean, default=False)

    application: Mapped[Application] = relationship("Application", back_populates="policy")


engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def _ensure_directories() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    POLICY_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OJK_RATES_PATH.parent.mkdir(parents=True, exist_ok=True)


def create_ojk_rates_csv() -> None:
    if OJK_RATES_PATH.exists():
        return

    # Mid-point of OJK rate ranges for simulation purposes.
    ranges = {
        "Comprehensive": {
            "Area 1": {"Cat 1": (3.26, 4.53), "Cat 2": (2.47, 2.72), "Cat 3": (2.08, 2.29), "Cat 4": (1.20, 1.32), "Cat 5": (1.05, 1.16)},
            "Area 2": {"Cat 1": (2.67, 3.69), "Cat 2": (2.47, 2.72), "Cat 3": (2.08, 2.29), "Cat 4": (1.20, 1.32), "Cat 5": (1.05, 1.16)},
            "Area 3": {"Cat 1": (2.53, 3.51), "Cat 2": (2.47, 2.72), "Cat 3": (2.08, 2.29), "Cat 4": (1.20, 1.32), "Cat 5": (1.05, 1.16)},
        },
        "TLO": {
            "Area 1": {"Cat 1": (0.47, 0.56), "Cat 2": (0.63, 0.69), "Cat 3": (0.44, 0.48), "Cat 4": (0.38, 0.42), "Cat 5": (0.31, 0.35)},
            "Area 2": {"Cat 1": (0.65, 0.78), "Cat 2": (0.44, 0.53), "Cat 3": (0.38, 0.42), "Cat 4": (0.25, 0.28), "Cat 5": (0.20, 0.22)},
            "Area 3": {"Cat 1": (0.51, 0.56), "Cat 2": (0.44, 0.53), "Cat 3": (0.29, 0.35), "Cat 4": (0.25, 0.28), "Cat 5": (0.20, 0.22)},
        },
    }

    category_limits = {
        "Cat 1": (0, 125_000_000),
        "Cat 2": (125_000_001, 200_000_000),
        "Cat 3": (200_000_001, 400_000_000),
        "Cat 4": (400_000_001, 800_000_000),
        "Cat 5": (800_000_001, 2_000_000_000),
    }

    rows: list[dict[str, object]] = []
    for coverage, coverage_data in ranges.items():
        for area, area_data in coverage_data.items():
            for category, (rmin, rmax) in area_data.items():
                vmin, vmax = category_limits[category]
                rows.append(
                    {
                        "coverage": coverage,
                        "area": area,
                        "vehicle_category": category,
                        "min_vehicle_value": vmin,
                        "max_vehicle_value": vmax,
                        "premium_rate": round((rmin + rmax) / 2, 4),
                    }
                )

    pd.DataFrame(rows).to_csv(OJK_RATES_PATH, index=False)


def create_database() -> None:
    _ensure_directories()
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    return SessionLocal()


def _vehicle_category(price: float) -> str:
    if price <= 125_000_000:
        return "Cat 1"
    if price <= 200_000_000:
        return "Cat 2"
    if price <= 400_000_000:
        return "Cat 3"
    if price <= 800_000_000:
        return "Cat 4"
    return "Cat 5"


def _lookup_rate(coverage: str, area: str, price: float) -> float:
    rate_df = pd.read_csv(OJK_RATES_PATH)
    category = _vehicle_category(price)
    row = rate_df[
        (rate_df["coverage"] == coverage)
        & (rate_df["area"] == area)
        & (rate_df["vehicle_category"] == category)
    ]
    if row.empty:
        return 2.0
    return float(row.iloc[0]["premium_rate"])


def _additional_fee(price: float, selected: Iterable[str]) -> float:
    fee_map = {
        "Flood": 0.001,
        "Earthquake": 0.0008,
        "Riot": 0.0005,
        "Third Party Liability": 0.0012,
        "Personal Accident": 0.0006,
    }
    return round(sum(price * fee_map.get(item, 0.0) for item in selected), 2)


def _random_plate(rnd: random.Random) -> str:
    prefix = rnd.choice(["B", "D", "F", "L", "N", "DK"]) 
    return f"{prefix} {rnd.randint(1000, 9999)} {rnd.choice(['AA', 'AB', 'CD', 'EF', 'GH'])}"


def _seed_customers(session: Session, faker: Faker, rnd: random.Random, total: int = 500) -> list[Customer]:
    customers: list[Customer] = []
    for _ in range(total):
        gender = rnd.choice(["Male", "Female"])
        birth = faker.date_of_birth(minimum_age=20, maximum_age=65)
        customer = Customer(
            customer_uuid=str(uuid.uuid4()),
            full_name=faker.name_male() if gender == "Male" else faker.name_female(),
            nik="".join(rnd.choices("0123456789", k=16)),
            gender=gender,
            birth_date=birth,
            phone=f"+62{rnd.randint(8110000000, 8999999999)}",
            email=faker.email(),
            address=faker.address().replace("\n", ", "),
        )
        session.add(customer)
        customers.append(customer)
    session.flush()
    return customers


def _seed_vehicles(session: Session, rnd: random.Random, customers: list[Customer], total: int = 500) -> list[Vehicle]:
    brand_models = {
        "Toyota": ["Avanza", "Fortuner", "Innova", "Rush"],
        "Honda": ["Brio", "HR-V", "CR-V", "Mobilio"],
        "Suzuki": ["Ertiga", "XL7", "Baleno"],
        "Mitsubishi": ["Xpander", "Pajero Sport"],
        "Hyundai": ["Creta", "Stargazer", "Ioniq 5"],
        "Daihatsu": ["Xenia", "Terios", "Sigra"],
        "BMW": ["320i", "X1", "X3"],
        "Mercedes": ["C200", "GLA", "E200"],
        "Wuling": ["Almaz", "Air EV", "Confero"],
    }

    base_prices = {
        "Toyota": (180_000_000, 650_000_000),
        "Honda": (170_000_000, 700_000_000),
        "Suzuki": (160_000_000, 400_000_000),
        "Mitsubishi": (220_000_000, 750_000_000),
        "Hyundai": (250_000_000, 900_000_000),
        "Daihatsu": (140_000_000, 350_000_000),
        "BMW": (850_000_000, 1_900_000_000),
        "Mercedes": (900_000_000, 2_000_000_000),
        "Wuling": (190_000_000, 500_000_000),
    }

    vehicles: list[Vehicle] = []
    for idx in range(total):
        customer = customers[idx % len(customers)]
        brand = rnd.choice(list(brand_models.keys()))
        min_price, max_price = base_prices[brand]
        vehicle = Vehicle(
            vehicle_uuid=str(uuid.uuid4()),
            customer_id=customer.id,
            brand=brand,
            model=rnd.choice(brand_models[brand]),
            year=rnd.randint(2012, datetime.now().year),
            plate_number=_random_plate(rnd),
            vehicle_type=rnd.choice(["SUV", "Sedan", "Hatchback", "MPV", "EV"]),
            vehicle_usage=rnd.choice(["Private", "Commercial"]),
            vehicle_price=float(rnd.randint(min_price, max_price)),
            area=rnd.choice(AREAS),
        )
        session.add(vehicle)
        vehicles.append(vehicle)
    session.flush()
    return vehicles


def _seed_applications(session: Session, rnd: random.Random, customers: list[Customer], vehicles: list[Vehicle], total: int = 500) -> list[Application]:
    applications: list[Application] = []
    for idx in range(total):
        customer = customers[idx % len(customers)]
        vehicle = vehicles[idx % len(vehicles)]
        status = rnd.choices(
            APPLICATION_STATUSES,
            weights=[10, 15, 15, 20, 10, 30],
            k=1,
        )[0]
        selected_addons = [item for item in ADDITIONAL_COVERAGES if rnd.random() > 0.65]
        application = Application(
            application_id=str(uuid.uuid4()),
            customer_id=customer.id,
            vehicle_id=vehicle.id,
            coverage_type=rnd.choice(COVERAGE_TYPES),
            area=vehicle.area,
            additional_coverages=selected_addons,
            status=status,
            submitted_at=datetime.utcnow() - timedelta(days=rnd.randint(0, 365)),
        )
        session.add(application)
        applications.append(application)
    session.flush()
    return applications


def _seed_premium_results(session: Session, applications: list[Application]) -> None:
    for app in applications:
        vehicle_price = float(app.vehicle.vehicle_price)
        rate = _lookup_rate(app.coverage_type, app.area, vehicle_price)
        basic = round(vehicle_price * rate / 100, 2)
        addon_fee = _additional_fee(vehicle_price, app.additional_coverages or [])
        total = round(basic + addon_fee + ADMIN_FEE + STAMP_DUTY, 2)
        session.add(
            PremiumResult(
                application_id=app.id,
                ojk_rate=rate,
                basic_premium=basic,
                additional_coverage_fee=addon_fee,
                admin_fee=ADMIN_FEE,
                stamp_duty=STAMP_DUTY,
                total_premium=total,
            )
        )


def _seed_underwriting_results(session: Session, applications: list[Application]) -> None:
    current_year = datetime.now().year
    for app in applications:
        vehicle_age = max(current_year - app.vehicle.year, 0)
        price = app.vehicle.vehicle_price
        usage = app.vehicle.vehicle_usage

        score = 0
        score += 2 if vehicle_age > 10 else 1 if vehicle_age > 5 else 0
        score += 2 if price > 1_000_000_000 else 1 if price > 500_000_000 else 0
        score += 2 if usage == "Commercial" else 0
        score += 1 if app.coverage_type == "Comprehensive" else 0

        if score <= 2:
            risk = "Low"
            decision = "Approved"
            notes = "Low risk profile, eligible for direct approval."
        elif score <= 4:
            risk = "Medium"
            decision = "Need Survey"
            notes = "Medium risk profile, physical survey required."
        else:
            risk = "High"
            decision = "Rejected"
            notes = "High risk profile outside underwriting appetite."

        session.add(
            UnderwritingResult(
                application_id=app.id,
                vehicle_age=vehicle_age,
                risk_level=risk,
                decision=decision,
                notes=notes,
            )
        )


def _seed_policies(session: Session, applications: list[Application], target: int = 300) -> None:
    issued_candidates = [
        app for app in applications if app.status in {"Approved", "Policy Issued"}
    ]
    selected = issued_candidates[:target] if len(issued_candidates) >= target else issued_candidates

    for app in selected:
        premium = app.premium_result.total_premium if app.premium_result else 0.0
        issue = date.today() - timedelta(days=random.randint(0, 60))
        policy = Policy(
            application_id=app.id,
            policy_number=f"ETQ-MTR-{issue.strftime('%Y%m')}-{str(uuid.uuid4())[:8].upper()}",
            issue_date=issue,
            effective_date=issue,
            expiry_date=issue + timedelta(days=365),
            premium_amount=premium,
            status="Issued",
            generated_pdf=False,
        )
        app.status = "Policy Issued"
        session.add(policy)


def export_data_to_csv(session: Session) -> None:
    pd.read_sql(session.query(Customer).statement, session.bind).to_csv(CUSTOMERS_CSV_PATH, index=False)
    pd.read_sql(session.query(Vehicle).statement, session.bind).to_csv(VEHICLES_CSV_PATH, index=False)
    pd.read_sql(session.query(Application).statement, session.bind).to_csv(APPLICATIONS_CSV_PATH, index=False)
    pd.read_sql(session.query(Policy).statement, session.bind).to_csv(POLICIES_CSV_PATH, index=False)


def seed_database_if_empty() -> None:
    create_ojk_rates_csv()
    with SessionLocal() as session:
        count = session.query(func.count(Customer.id)).scalar() or 0
        if count > 0:
            export_data_to_csv(session)
            return

        faker = Faker("id_ID")
        rnd = random.Random(42)

        customers = _seed_customers(session, faker, rnd, total=500)
        vehicles = _seed_vehicles(session, rnd, customers, total=500)
        applications = _seed_applications(session, rnd, customers, vehicles, total=500)
        _seed_premium_results(session, applications)
        session.flush()

        app_refs = session.query(Application).all()
        _seed_underwriting_results(session, app_refs)
        session.flush()

        app_refs = session.query(Application).all()
        _seed_policies(session, app_refs, target=300)

        session.commit()
        export_data_to_csv(session)


def initialize_database() -> None:
    create_database()
    seed_database_if_empty()


def create_application_with_related_records(payload: dict[str, object]) -> str:
    from premium_engine import calculate_premium
    from underwriting import evaluate_underwriting

    with SessionLocal() as session:
        customer = Customer(
            customer_uuid=str(uuid.uuid4()),
            full_name=str(payload["full_name"]),
            nik=str(payload["nik"]),
            gender=str(payload["gender"]),
            birth_date=payload["birth_date"],
            phone=str(payload["phone"]),
            email=str(payload["email"]),
            address=str(payload["address"]),
        )
        session.add(customer)
        session.flush()

        vehicle = Vehicle(
            vehicle_uuid=str(uuid.uuid4()),
            customer_id=customer.id,
            brand=str(payload["brand"]),
            model=str(payload["model"]),
            year=int(payload["year"]),
            plate_number=str(payload["plate_number"]),
            vehicle_type=str(payload["vehicle_type"]),
            vehicle_usage=str(payload["vehicle_usage"]),
            vehicle_price=float(payload["vehicle_price"]),
            area=str(payload["area"]),
        )
        session.add(vehicle)
        session.flush()

        application = Application(
            application_id=str(uuid.uuid4()),
            customer_id=customer.id,
            vehicle_id=vehicle.id,
            coverage_type=str(payload["coverage_type"]),
            area=str(payload["area"]),
            additional_coverages=list(payload.get("additional_coverages", [])),
            status="Submitted",
        )
        session.add(application)
        session.flush()

        premium = calculate_premium(
            vehicle_price=vehicle.vehicle_price,
            coverage_type=application.coverage_type,
            area=application.area,
            additional_coverages=application.additional_coverages,
        )
        session.add(
            PremiumResult(
                application_id=application.id,
                ojk_rate=premium["ojk_rate"],
                basic_premium=premium["basic_premium"],
                additional_coverage_fee=premium["additional_coverage_fee"],
                admin_fee=premium["admin_fee"],
                stamp_duty=premium["stamp_duty"],
                total_premium=premium["total_premium"],
            )
        )

        uw = evaluate_underwriting(
            vehicle_year=vehicle.year,
            vehicle_price=vehicle.vehicle_price,
            coverage_type=application.coverage_type,
            vehicle_usage=vehicle.vehicle_usage,
        )
        session.add(
            UnderwritingResult(
                application_id=application.id,
                vehicle_age=uw["vehicle_age"],
                risk_level=uw["risk_level"],
                decision=uw["decision"],
                notes=uw["notes"],
            )
        )

        if uw["decision"] == "Approved":
            application.status = "Approved"
        elif uw["decision"] == "Need Survey":
            application.status = "Underwriting"
        else:
            application.status = "Rejected"

        session.commit()
        export_data_to_csv(session)

        return application.application_id


def get_application_bundle(application_id: str) -> dict[str, object] | None:
    with SessionLocal() as session:
        app = session.query(Application).filter(Application.application_id == application_id).first()
        if not app:
            return None

        return {
            "application": app,
            "customer": app.customer,
            "vehicle": app.vehicle,
            "premium": app.premium_result,
            "underwriting": app.underwriting_result,
            "policy": app.policy,
        }
