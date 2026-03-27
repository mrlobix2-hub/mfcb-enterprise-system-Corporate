
import os
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, send_from_directory, abort
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "mfcb-enterprise-secret-key")
db_url = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx", "txt", "xlsx"}

def now_utc():
    return datetime.utcnow()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def to_decimal(value, default="0"):
    value = str(value).strip()
    if not value:
        value = default
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal(default)

def decimal_to_str(v):
    if v is None:
        return "0.00"
    return f"{Decimal(v):.2f}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    client_profile_id = db.Column(db.Integer, db.ForeignKey("client_profile.id"), nullable=True)

    client_profile = db.relationship("ClientProfile", foreign_keys=[client_profile_id], backref="account_user", uselist=False)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

class PortfolioProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    project_type = db.Column(db.String(80), nullable=False)
    year_label = db.Column(db.String(20), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False, default="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85")

class UKAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), nullable=False)

class BaseRecordMixin:
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(80), nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)
    is_locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=now_utc)

class PeopleMatter(db.Model, BaseRecordMixin):
    person_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), default="")
    total_amount = db.Column(db.Numeric(12,2), default=0)
    paid_amount = db.Column(db.Numeric(12,2), default=0)
    remaining_amount = db.Column(db.Numeric(12,2), default=0)
    currency = db.Column(db.String(20), default="PKR")
    payment_method = db.Column(db.String(50), default="")
    transaction_id = db.Column(db.String(100), default="")
    contact_mode = db.Column(db.String(50), default="")
    case_flag = db.Column(db.String(80), default="")
    case_details = db.Column(db.Text, default="")
    notes = db.Column(db.Text, default="")
    status = db.Column(db.String(30), default="pending")

class LegalCase(db.Model, BaseRecordMixin):
    person_name = db.Column(db.String(120), nullable=False)
    role_type = db.Column(db.String(80), default="")
    phone = db.Column(db.String(50), default="")
    case_purpose = db.Column(db.String(150), default="")
    department_name = db.Column(db.String(120), default="")
    amount_paid = db.Column(db.Numeric(12,2), default=0)
    amount_pending = db.Column(db.Numeric(12,2), default=0)
    payment_method = db.Column(db.String(50), default="")
    transaction_id = db.Column(db.String(100), default="")
    case_status = db.Column(db.String(50), default="in_progress")
    agreement_status = db.Column(db.String(50), default="")
    notes = db.Column(db.Text, default="")

class RiskRecord(db.Model, BaseRecordMixin):
    person_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), default="")
    risk_level = db.Column(db.String(50), default="medium")
    background = db.Column(db.Text, default="")
    notes = db.Column(db.Text, default="")

class LendingRecord(db.Model, BaseRecordMixin):
    person_name = db.Column(db.String(120), nullable=False)
    entry_type = db.Column(db.String(50), default="recoverable")
    reason = db.Column(db.String(150), default="")
    amount_given = db.Column(db.Numeric(12,2), default=0)
    amount_received_back = db.Column(db.Numeric(12,2), default=0)
    remaining_amount = db.Column(db.Numeric(12,2), default=0)
    currency = db.Column(db.String(20), default="PKR")
    payment_method = db.Column(db.String(50), default="")
    entry_date = db.Column(db.String(30), default="")
    notes = db.Column(db.Text, default="")
    status = db.Column(db.String(30), default="pending")

class PersonalFinance(db.Model, BaseRecordMixin):
    entry_type = db.Column(db.String(30), default="received")
    relation_name = db.Column(db.String(120), default="")
    relation_type = db.Column(db.String(80), default="")
    category = db.Column(db.String(80), default="")
    amount = db.Column(db.Numeric(12,2), default=0)
    currency = db.Column(db.String(20), default="PKR")
    payment_method = db.Column(db.String(50), default="")
    source_detail = db.Column(db.String(150), default="")
    entry_date = db.Column(db.String(30), default="")
    purpose = db.Column(db.String(150), default="")
    notes = db.Column(db.Text, default="")

class HouseholdExpense(db.Model, BaseRecordMixin):
    expense_group = db.Column(db.String(80), default="")
    item_name = db.Column(db.String(120), default="")
    beneficiary = db.Column(db.String(120), default="")
    amount = db.Column(db.Numeric(12,2), default=0)
    currency = db.Column(db.String(20), default="PKR")
    payment_method = db.Column(db.String(50), default="")
    expense_date = db.Column(db.String(30), default="")
    paid_status = db.Column(db.String(30), default="paid")
    source_of_funds = db.Column(db.String(120), default="")
    purpose = db.Column(db.String(150), default="")
    notes = db.Column(db.Text, default="")

class ConstructionRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate_type = db.Column(db.String(80), default="")
    unit_type = db.Column(db.String(30), default="marla")
    rate_value = db.Column(db.Numeric(12,2), default=0)
    effective_date = db.Column(db.String(30), default="")
    notes = db.Column(db.Text, default="")

class MaterialRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steel_rate = db.Column(db.Numeric(12,2), default=0)
    cement_rate = db.Column(db.Numeric(12,2), default=0)
    sand_rate = db.Column(db.Numeric(12,2), default=0)
    bajri_rate = db.Column(db.Numeric(12,2), default=0)
    effective_date = db.Column(db.String(30), default="")
    notes = db.Column(db.Text, default="")

class ConstructionProject(db.Model, BaseRecordMixin):
    project_name = db.Column(db.String(150), nullable=False)
    project_received_status = db.Column(db.String(50), default="")
    square_feet = db.Column(db.Numeric(12,2), default=0)
    marla = db.Column(db.Numeric(12,2), default=0)
    owner_name = db.Column(db.String(120), default="")
    owner_phone = db.Column(db.String(50), default="")
    contractor_name = db.Column(db.String(120), default="")
    mason_name = db.Column(db.String(120), default="")
    labour_details = db.Column(db.Text, default="")
    project_type = db.Column(db.String(80), default="")
    rate_used = db.Column(db.Numeric(12,2), default=0)
    auto_total = db.Column(db.Numeric(12,2), default=0)
    contract_amount = db.Column(db.Numeric(12,2), default=0)
    project_status = db.Column(db.String(50), default="in_progress")
    notes = db.Column(db.Text, default="")

class ClientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(50), unique=True, nullable=False)
    client_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), default="")
    email = db.Column(db.String(120), default="")
    destination_country = db.Column(db.String(80), default="")
    case_type = db.Column(db.String(80), default="")
    current_stage = db.Column(db.String(80), default="")
    case_status = db.Column(db.String(30), default="in_progress")
    total_fee = db.Column(db.Numeric(12,2), default=0)
    received_amount = db.Column(db.Numeric(12,2), default=0)
    remaining_amount = db.Column(db.Numeric(12,2), default=0)
    payment_status = db.Column(db.String(30), default="pending")
    payment_due_date = db.Column(db.String(30), default="")
    payment_warning_note = db.Column(db.String(200), default="")
    documents_status = db.Column(db.String(50), default="pending")
    form_submitted = db.Column(db.String(50), default="pending")
    embassy_status = db.Column(db.String(50), default="pending")
    work_permit_status = db.Column(db.String(50), default="pending")
    mofa_status = db.Column(db.String(50), default="pending")
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=now_utc)

class CaseStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client_profile.id"), nullable=False)
    step_name = db.Column(db.String(120), nullable=False)
    step_status = db.Column(db.String(50), default="pending")
    step_note = db.Column(db.Text, default="")
    step_date = db.Column(db.String(30), default="")
    client = db.relationship("ClientProfile", backref="case_steps")

class ClientDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client_profile.id"), nullable=False)
    document_name = db.Column(db.String(150), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    uploaded_by_role = db.Column(db.String(30), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=now_utc)
    notes = db.Column(db.Text, default="")
    client = db.relationship("ClientProfile", backref="documents")

class VaultEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_category = db.Column(db.String(80), default="")
    label = db.Column(db.String(150), default="")
    url = db.Column(db.String(255), default="")
    username = db.Column(db.String(120), default="")
    password_value = db.Column(db.String(120), default="")
    bank_name = db.Column(db.String(120), default="")
    account_title = db.Column(db.String(120), default="")
    account_number = db.Column(db.String(80), default="")
    iban = db.Column(db.String(80), default="")
    private_note = db.Column(db.Text, default="")
    hidden_flag = db.Column(db.Boolean, default=False)

MODULES = {
    "people": {
        "model": PeopleMatter,
        "title": "People Matters",
        "nav_group": "People Matters",
        "fields": [
            ("person_name", "Person Name", "text"),
            ("phone", "Phone", "text"),
            ("total_amount", "Total Amount", "number"),
            ("paid_amount", "Paid Amount", "number"),
            ("currency", "Currency", "text"),
            ("payment_method", "Payment Method", "text"),
            ("transaction_id", "Transaction ID", "text"),
            ("contact_mode", "Contact Mode", "text"),
            ("case_flag", "Case Flag", "text"),
            ("case_details", "Case Details", "textarea"),
            ("notes", "Notes", "textarea"),
        ],
        "columns": ["person_name", "phone", "total_amount", "paid_amount", "remaining_amount", "currency", "status", "created_by", "is_locked"],
    },
    "legal": {
        "model": LegalCase,
        "title": "Legal / Lawyer / Police / FIA / Special Cases",
        "nav_group": "Legal / Special",
        "fields": [
            ("person_name", "Person Name", "text"),
            ("role_type", "Role Type", "text"),
            ("phone", "Phone", "text"),
            ("case_purpose", "Case Purpose", "text"),
            ("department_name", "Department Name", "text"),
            ("amount_paid", "Amount Paid", "number"),
            ("amount_pending", "Amount Pending", "number"),
            ("payment_method", "Payment Method", "text"),
            ("transaction_id", "Transaction ID", "text"),
            ("case_status", "Case Status", "text"),
            ("agreement_status", "Agreement Status", "text"),
            ("notes", "Notes", "textarea"),
        ],
        "columns": ["person_name", "role_type", "department_name", "amount_paid", "amount_pending", "case_status", "created_by", "is_locked"],
    },
    "risk": {
        "model": RiskRecord,
        "title": "Risk Records",
        "nav_group": "Risk",
        "fields": [
            ("person_name", "Person Name", "text"),
            ("phone", "Phone", "text"),
            ("risk_level", "Risk Level", "text"),
            ("background", "Background", "textarea"),
            ("notes", "Notes", "textarea"),
        ],
        "columns": ["person_name", "phone", "risk_level", "created_by", "is_locked"],
    },
    "lending": {
        "model": LendingRecord,
        "title": "Lending / Borrowing",
        "nav_group": "Lending",
        "fields": [
            ("person_name", "Person Name", "text"),
            ("entry_type", "Entry Type", "text"),
            ("reason", "Reason", "text"),
            ("amount_given", "Amount Given", "number"),
            ("amount_received_back", "Amount Received Back", "number"),
            ("currency", "Currency", "text"),
            ("payment_method", "Payment Method", "text"),
            ("entry_date", "Entry Date", "text"),
            ("notes", "Notes", "textarea"),
        ],
        "columns": ["person_name", "entry_type", "amount_given", "amount_received_back", "remaining_amount", "status", "created_by", "is_locked"],
    },
    "personal": {
        "model": PersonalFinance,
        "title": "Personal Finance",
        "nav_group": "Personal",
        "fields": [
            ("entry_type", "Entry Type", "text"),
            ("relation_name", "Relation Name", "text"),
            ("relation_type", "Relation Type", "text"),
            ("category", "Category", "text"),
            ("amount", "Amount", "number"),
            ("currency", "Currency", "text"),
            ("payment_method", "Payment Method", "text"),
            ("source_detail", "Source Detail", "text"),
            ("entry_date", "Entry Date", "text"),
            ("purpose", "Purpose", "text"),
            ("notes", "Notes", "textarea"),
        ],
        "columns": ["entry_type", "relation_name", "category", "amount", "currency", "created_by", "is_locked"],
    },
    "household": {
        "model": HouseholdExpense,
        "title": "Household & Family",
        "nav_group": "Household",
        "fields": [
            ("expense_group", "Expense Group", "text"),
            ("item_name", "Item Name", "text"),
            ("beneficiary", "Beneficiary", "text"),
            ("amount", "Amount", "number"),
            ("currency", "Currency", "text"),
            ("payment_method", "Payment Method", "text"),
            ("expense_date", "Expense Date", "text"),
            ("paid_status", "Paid Status", "text"),
            ("source_of_funds", "Source Of Funds", "text"),
            ("purpose", "Purpose", "text"),
            ("notes", "Notes", "textarea"),
        ],
        "columns": ["expense_group", "item_name", "beneficiary", "amount", "paid_status", "created_by", "is_locked"],
    },
    "construction_projects": {
        "model": ConstructionProject,
        "title": "Construction Projects",
        "nav_group": "Construction",
        "fields": [
            ("project_name", "Project Name", "text"),
            ("project_received_status", "Project Received Status", "text"),
            ("square_feet", "Square Feet", "number"),
            ("marla", "Marla", "number"),
            ("owner_name", "Owner Name", "text"),
            ("owner_phone", "Owner Phone", "text"),
            ("contractor_name", "Contractor Name", "text"),
            ("mason_name", "Mason Name", "text"),
            ("labour_details", "Labour Details", "textarea"),
            ("project_type", "Project Type", "text"),
            ("rate_used", "Rate Used", "number"),
            ("contract_amount", "Contract Amount", "number"),
            ("project_status", "Project Status", "text"),
            ("notes", "Notes", "textarea"),
        ],
        "columns": ["project_name", "owner_name", "project_type", "rate_used", "auto_total", "contract_amount", "project_status", "created_by", "is_locked"],
    },
}

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.get(uid)

@app.context_processor
def inject_globals():
    return {"current_user": current_user(), "MODULES": MODULES, "decimal_to_str": decimal_to_str, "attribute": getattr}

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please sign in first.", "danger")
            return redirect(url_for("access_portal"))
        return fn(*args, **kwargs)
    return wrapper

def role_required(*roles):
    def outer(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                return redirect(url_for("access_portal"))
            if user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return outer

def can_edit_record(user, record):
    if user.role == "director":
        return True
    return record.created_by == user.username and not record.is_locked

def apply_module_logic(module_key, obj):
    if module_key == "people":
        total = to_decimal(obj.total_amount)
        paid = to_decimal(obj.paid_amount)
        remain = total - paid
        obj.remaining_amount = remain
        obj.status = "cleared" if remain <= 0 else "pending"
    elif module_key == "lending":
        given = to_decimal(obj.amount_given)
        got = to_decimal(obj.amount_received_back)
        remain = given - got
        obj.remaining_amount = remain
        obj.status = "cleared" if remain <= 0 else "pending"
    elif module_key == "construction_projects":
        marla = to_decimal(obj.marla)
        square_feet = to_decimal(obj.square_feet)
        rate = to_decimal(obj.rate_used)
        auto_total = marla * rate if marla > 0 else square_feet * rate
        obj.auto_total = auto_total
        if to_decimal(obj.contract_amount) <= 0:
            obj.contract_amount = auto_total

def apply_client_logic(obj):
    total = to_decimal(obj.total_fee)
    received = to_decimal(obj.received_amount)
    remain = total - received
    obj.remaining_amount = remain
    obj.payment_status = "cleared" if remain <= 0 else "pending"

def fill_model_from_form(obj, fields):
    for field_name, _label, ftype in fields:
        val = request.form.get(field_name, "").strip()
        current = getattr(type(obj), field_name).property.columns[0]
        if str(current.type).startswith("NUMERIC"):
            setattr(obj, field_name, to_decimal(val))
        else:
            setattr(obj, field_name, val)

@app.route("/")
def home():
    projects = PortfolioProject.query.order_by(PortfolioProject.id.desc()).limit(6).all()
    return render_template("public/home.html", projects=projects)

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.route("/pakistan-real-estate")
def pakistan_real_estate():
    return render_template("public/pakistan_real_estate.html")

@app.route("/pakistan-construction")
def pakistan_construction():
    return render_template("public/pakistan_construction.html")

@app.route("/uk-real-estate-construction")
def uk_real_estate_construction():
    addresses = UKAddress.query.all()
    return render_template("public/uk_real_estate_construction.html", addresses=addresses)

@app.route("/projects")
def projects():
    items = PortfolioProject.query.order_by(PortfolioProject.id.desc()).all()
    return render_template("public/projects.html", items=items)

@app.route("/projects/<int:project_id>")
def project_detail(project_id):
    item = PortfolioProject.query.get_or_404(project_id)
    return render_template("public/project_detail.html", item=item)

@app.route("/contact")
def contact():
    return render_template("public/contact.html")

@app.route("/access-portal")
def access_portal():
    return render_template("public/access_portal.html")

@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    pretty = {"director": "Corporate Special Access", "manager": "Manager Access", "client": "Simple User"}.get(role)
    if not pretty:
        abort(404)
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = User.query.filter_by(username=username, is_active=True).first()
        if user and user.check_password(password):
            expected = "client" if role == "client" else role
            if user.role != expected:
                flash("Role mismatch for selected access entry.", "danger")
            else:
                session["user_id"] = user.id
                flash("Signed in successfully.", "success")
                return redirect(url_for("client_portal" if user.role == "client" else "dashboard"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("auth/login.html", role=role, pretty=pretty)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    if user.role == "director":
        stats = {
            "people_total": PeopleMatter.query.count(),
            "people_cleared": PeopleMatter.query.filter_by(status="cleared").count(),
            "legal_outflow": decimal_to_str(db.session.query(func.coalesce(func.sum(LegalCase.amount_paid), 0)).scalar() or 0),
            "lending_pending": decimal_to_str(db.session.query(func.coalesce(func.sum(LendingRecord.remaining_amount), 0)).scalar() or 0),
            "personal_total": decimal_to_str(db.session.query(func.coalesce(func.sum(PersonalFinance.amount), 0)).scalar() or 0),
            "household_total": decimal_to_str(db.session.query(func.coalesce(func.sum(HouseholdExpense.amount), 0)).scalar() or 0),
            "client_count": ClientProfile.query.count(),
            "construction_count": ConstructionProject.query.count(),
        }
        chart = [
            ("People", stats["people_total"]),
            ("Clients", stats["client_count"]),
            ("Construction", stats["construction_count"]),
            ("Cleared People", stats["people_cleared"]),
        ]
        return render_template("dashboard/director_dashboard.html", stats=stats, chart=chart)
    else:
        username = user.username
        counts = {
            "people": PeopleMatter.query.filter_by(created_by=username).count(),
            "legal": LegalCase.query.filter_by(created_by=username).count(),
            "risk": RiskRecord.query.filter_by(created_by=username).count(),
            "lending": LendingRecord.query.filter_by(created_by=username).count(),
            "personal": PersonalFinance.query.filter_by(created_by=username).count(),
            "household": HouseholdExpense.query.filter_by(created_by=username).count(),
            "construction": ConstructionProject.query.filter_by(created_by=username).count(),
        }
        return render_template("dashboard/staff_dashboard.html", counts=counts)

@app.route("/module/<module_key>")
@login_required
def module_list(module_key):
    user = current_user()
    config = MODULES.get(module_key)
    if not config:
        abort(404)
    model = config["model"]
    query = model.query.order_by(model.id.desc())
    if user.role in ["manager", "operator"]:
        query = query.filter_by(created_by=user.username)
    records = query.all()
    return render_template("shared/module_list.html", module_key=module_key, config=config, records=records)

@app.route("/module/<module_key>/new", methods=["GET", "POST"])
@login_required
def module_new(module_key):
    user = current_user()
    config = MODULES.get(module_key)
    if not config:
        abort(404)
    obj = config["model"]()
    if request.method == "POST":
        fill_model_from_form(obj, config["fields"])
        obj.created_by = user.username
        apply_module_logic(module_key, obj)
        db.session.add(obj)
        db.session.commit()
        flash(f'{config["title"]} record created.', "success")
        return redirect(url_for("module_list", module_key=module_key))
    return render_template("shared/module_form.html", module_key=module_key, config=config, record=obj, editing=False)

@app.route("/module/<module_key>/<int:record_id>/edit", methods=["GET", "POST"])
@login_required
def module_edit(module_key, record_id):
    user = current_user()
    config = MODULES.get(module_key)
    if not config:
        abort(404)
    obj = config["model"].query.get_or_404(record_id)
    if not can_edit_record(user, obj):
        abort(403)
    if request.method == "POST":
        fill_model_from_form(obj, config["fields"])
        apply_module_logic(module_key, obj)
        db.session.commit()
        flash("Record updated.", "success")
        return redirect(url_for("module_list", module_key=module_key))
    return render_template("shared/module_form.html", module_key=module_key, config=config, record=obj, editing=True)

@app.route("/module/<module_key>/<int:record_id>/submit", methods=["POST"])
@login_required
def module_submit(module_key, record_id):
    user = current_user()
    config = MODULES.get(module_key)
    if not config:
        abort(404)
    obj = config["model"].query.get_or_404(record_id)
    if user.role == "director":
        obj.is_locked = True
        obj.submitted_at = now_utc()
    else:
        if obj.created_by != user.username or obj.is_locked:
            abort(403)
        obj.is_locked = True
        obj.submitted_at = now_utc()
    db.session.commit()
    flash("Record submitted and locked.", "success")
    return redirect(url_for("module_list", module_key=module_key))

@app.route("/module/<module_key>/<int:record_id>/unlock", methods=["POST"])
@role_required("director")
def module_unlock(module_key, record_id):
    config = MODULES.get(module_key)
    if not config:
        abort(404)
    obj = config["model"].query.get_or_404(record_id)
    obj.is_locked = False
    db.session.commit()
    flash("Director override applied. Record unlocked.", "warning")
    return redirect(url_for("module_list", module_key=module_key))

@app.route("/module/<module_key>/<int:record_id>/delete", methods=["POST"])
@role_required("director")
def module_delete(module_key, record_id):
    config = MODULES.get(module_key)
    if not config:
        abort(404)
    obj = config["model"].query.get_or_404(record_id)
    db.session.delete(obj)
    db.session.commit()
    flash("Record deleted.", "danger")
    return redirect(url_for("module_list", module_key=module_key))

@app.route("/reports/<module_key>")
@login_required
def report_module(module_key):
    config = MODULES.get(module_key)
    if not config:
        abort(404)
    user = current_user()
    model = config["model"]
    query = model.query.order_by(model.id.desc())
    if user.role in ["manager", "operator"]:
        query = query.filter_by(created_by=user.username)
    records = query.all()
    return render_template("shared/report.html", config=config, records=records)

@app.route("/construction-rates", methods=["GET", "POST"])
@login_required
def construction_rates():
    user = current_user()
    if user.role not in ["director", "manager", "operator"]:
        abort(403)
    if request.method == "POST":
        r = ConstructionRate(
            rate_type=request.form.get("rate_type", "").strip(),
            unit_type=request.form.get("unit_type", "").strip(),
            rate_value=to_decimal(request.form.get("rate_value", "0")),
            effective_date=request.form.get("effective_date", "").strip(),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(r)
        db.session.commit()
        flash("Construction rate added.", "success")
        return redirect(url_for("construction_rates"))
    rates = ConstructionRate.query.order_by(ConstructionRate.id.desc()).all()
    return render_template("shared/construction_rates.html", rates=rates)

@app.route("/material-rates", methods=["GET", "POST"])
@login_required
def material_rates():
    user = current_user()
    if user.role not in ["director", "manager", "operator"]:
        abort(403)
    if request.method == "POST":
        m = MaterialRate(
            steel_rate=to_decimal(request.form.get("steel_rate", "0")),
            cement_rate=to_decimal(request.form.get("cement_rate", "0")),
            sand_rate=to_decimal(request.form.get("sand_rate", "0")),
            bajri_rate=to_decimal(request.form.get("bajri_rate", "0")),
            effective_date=request.form.get("effective_date", "").strip(),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(m)
        db.session.commit()
        flash("Material rates added.", "success")
        return redirect(url_for("material_rates"))
    rates = MaterialRate.query.order_by(MaterialRate.id.desc()).all()
    return render_template("shared/material_rates.html", rates=rates)

@app.route("/internal-users", methods=["GET", "POST"])
@role_required("director")
def internal_users():
    if request.method == "POST":
        role = request.form.get("role", "")
        if role not in ["manager", "operator"]:
            flash("Only manager and operator can be created here.", "danger")
            return redirect(url_for("internal_users"))
        user = User(
            full_name=request.form.get("full_name", "").strip(),
            username=request.form.get("username", "").strip(),
            role=role,
            is_active=request.form.get("is_active") == "on",
        )
        user.set_password(request.form.get("password", "").strip())
        db.session.add(user)
        db.session.commit()
        flash("Internal user created.", "success")
        return redirect(url_for("internal_users"))
    users = User.query.filter(User.role.in_(["manager", "operator"])).order_by(User.id.desc()).all()
    return render_template("director/internal_users.html", users=users)

@app.route("/internal-users/<int:user_id>/toggle", methods=["POST"])
@role_required("director")
def toggle_internal_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role not in ["manager", "operator"]:
        abort(403)
    user.is_active = not user.is_active
    db.session.commit()
    flash("User status updated.", "success")
    return redirect(url_for("internal_users"))

@app.route("/internal-users/<int:user_id>/reset", methods=["POST"])
@role_required("director")
def reset_internal_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role not in ["manager", "operator"]:
        abort(403)
    user.username = request.form.get("username", user.username).strip()
    user.set_password(request.form.get("password", "ChangeMe@123").strip())
    db.session.commit()
    flash("Credentials updated.", "success")
    return redirect(url_for("internal_users"))

@app.route("/clients", methods=["GET", "POST"])
@login_required
def clients():
    user = current_user()
    if user.role == "client":
        abort(403)
    if request.method == "POST":
        c = ClientProfile(
            unique_id=request.form.get("unique_id", "").strip(),
            client_name=request.form.get("client_name", "").strip(),
            phone=request.form.get("phone", "").strip(),
            email=request.form.get("email", "").strip(),
            destination_country=request.form.get("destination_country", "").strip(),
            case_type=request.form.get("case_type", "").strip(),
            current_stage=request.form.get("current_stage", "").strip(),
            case_status=request.form.get("case_status", "").strip(),
            total_fee=to_decimal(request.form.get("total_fee", "0")),
            received_amount=to_decimal(request.form.get("received_amount", "0")),
            payment_due_date=request.form.get("payment_due_date", "").strip(),
            payment_warning_note=request.form.get("payment_warning_note", "").strip(),
            documents_status=request.form.get("documents_status", "").strip(),
            form_submitted=request.form.get("form_submitted", "").strip(),
            embassy_status=request.form.get("embassy_status", "").strip(),
            work_permit_status=request.form.get("work_permit_status", "").strip(),
            mofa_status=request.form.get("mofa_status", "").strip(),
            notes=request.form.get("notes", "").strip(),
        )
        apply_client_logic(c)
        db.session.add(c)
        db.session.commit()
        flash("Client profile created.", "success")
        return redirect(url_for("clients"))
    items = ClientProfile.query.order_by(ClientProfile.id.desc()).all()
    return render_template("director/clients.html", items=items)

@app.route("/clients/<int:client_id>/edit", methods=["GET", "POST"])
@login_required
def edit_client(client_id):
    user = current_user()
    if user.role == "client":
        abort(403)
    c = ClientProfile.query.get_or_404(client_id)
    if request.method == "POST":
        for fld in ["unique_id","client_name","phone","email","destination_country","case_type","current_stage","case_status","payment_due_date","payment_warning_note","documents_status","form_submitted","embassy_status","work_permit_status","mofa_status","notes"]:
            setattr(c, fld, request.form.get(fld, "").strip())
        c.total_fee = to_decimal(request.form.get("total_fee", "0"))
        c.received_amount = to_decimal(request.form.get("received_amount", "0"))
        apply_client_logic(c)
        db.session.commit()
        flash("Client updated.", "success")
        return redirect(url_for("clients"))
    return render_template("director/client_form.html", c=c)

@app.route("/clients/<int:client_id>/credential", methods=["POST"])
@role_required("director")
def client_credential(client_id):
    c = ClientProfile.query.get_or_404(client_id)
    existing = User.query.filter_by(client_profile_id=c.id, role="client").first()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    is_active = request.form.get("is_active") == "on"
    if existing:
        existing.username = username
        existing.is_active = is_active
        existing.set_password(password)
    else:
        u = User(full_name=c.client_name, username=username, role="client", is_active=is_active, client_profile_id=c.id)
        u.set_password(password)
        db.session.add(u)
    db.session.commit()
    flash("Client credentials saved.", "success")
    return redirect(url_for("clients"))

@app.route("/clients/<int:client_id>/steps", methods=["GET", "POST"])
@login_required
def client_steps(client_id):
    user = current_user()
    if user.role not in ["director", "manager", "operator"]:
        abort(403)
    c = ClientProfile.query.get_or_404(client_id)
    if request.method == "POST":
        if user.role != "director":
            abort(403)
        s = CaseStep(
            client_id=c.id,
            step_name=request.form.get("step_name", "").strip(),
            step_status=request.form.get("step_status", "").strip(),
            step_note=request.form.get("step_note", "").strip(),
            step_date=request.form.get("step_date", "").strip(),
        )
        db.session.add(s)
        db.session.commit()
        flash("Case step added.", "success")
    return render_template("director/client_steps.html", c=c)

@app.route("/clients/<int:client_id>/upload", methods=["POST"])
@login_required
def upload_client_document(client_id):
    user = current_user()
    c = ClientProfile.query.get_or_404(client_id)
    if user.role == "client" and user.client_profile_id != c.id:
        abort(403)
    if user.role not in ["director", "client"]:
        abort(403)
    file = request.files.get("file")
    if not file or not file.filename:
        flash("Please choose a file.", "danger")
        return redirect(request.referrer or url_for("clients"))
    if not allowed_file(file.filename):
        flash("Unsupported file type.", "danger")
        return redirect(request.referrer or url_for("clients"))
    safe = secure_filename(file.filename)
    stamped = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{safe}"
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], stamped))
    d = ClientDocument(
        client_id=c.id,
        document_name=request.form.get("document_name", safe).strip() or safe,
        file_name=stamped,
        uploaded_by_role=user.role,
        notes=request.form.get("notes", "").strip(),
    )
    db.session.add(d)
    db.session.commit()
    flash("Document uploaded.", "success")
    return redirect(request.referrer or url_for("clients"))

@app.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):
    user = current_user()
    doc = ClientDocument.query.filter_by(file_name=filename).first_or_404()
    if user.role == "client" and user.client_profile_id != doc.client_id:
        abort(403)
    if user.role not in ["director", "client", "manager", "operator"]:
        abort(403)
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

@app.route("/secure-vault", methods=["GET", "POST"])
@role_required("director")
def secure_vault():
    if request.method == "POST":
        v = VaultEntry(
            entry_category=request.form.get("entry_category", "").strip(),
            label=request.form.get("label", "").strip(),
            url=request.form.get("url", "").strip(),
            username=request.form.get("username", "").strip(),
            password_value=request.form.get("password_value", "").strip(),
            bank_name=request.form.get("bank_name", "").strip(),
            account_title=request.form.get("account_title", "").strip(),
            account_number=request.form.get("account_number", "").strip(),
            iban=request.form.get("iban", "").strip(),
            private_note=request.form.get("private_note", "").strip(),
            hidden_flag=request.form.get("hidden_flag") == "on",
        )
        db.session.add(v)
        db.session.commit()
        flash("Vault entry saved.", "success")
        return redirect(url_for("secure_vault"))
    items = VaultEntry.query.order_by(VaultEntry.id.desc()).all()
    return render_template("director/secure_vault.html", items=items)

@app.route("/client-portal")
@role_required("client")
def client_portal():
    user = current_user()
    c = ClientProfile.query.get_or_404(user.client_profile_id)
    return render_template("client/portal.html", c=c)

@app.route("/about-internal")
@login_required
def about_internal():
    return render_template("dashboard/about_internal.html")

def seed_data():
    if User.query.first():
        return

    director = User(full_name="MFCB Director", username="MFCB0329", role="director", is_active=True)
    director.set_password("00447883169211@mfcb")
    manager = User(full_name="Operations Manager", username="manager01", role="manager", is_active=True)
    manager.set_password("Manager@123")
    operator = User(full_name="Data Entry Operator", username="operator01", role="operator", is_active=True)
    operator.set_password("Operator@123")

    sample_client = ClientProfile(
        unique_id="MFCB-CL-0001",
        client_name="Sample Client",
        phone="+92 300 1234567",
        email="client@example.com",
        destination_country="United Kingdom",
        case_type="Work Permit",
        current_stage="Embassy Review",
        case_status="in_progress",
        total_fee=Decimal("5000"),
        received_amount=Decimal("3000"),
        payment_due_date="2026-04-15",
        payment_warning_note="Final installment due before visa decision.",
        documents_status="in_progress",
        form_submitted="completed",
        embassy_status="in_progress",
        work_permit_status="pending",
        mofa_status="pending",
        notes="Client profile created for seeded portal testing.",
    )
    apply_client_logic(sample_client)
    db.session.add(sample_client)
    db.session.flush()

    client_user = User(full_name="Sample Client", username="simpleuser01", role="client", is_active=True, client_profile_id=sample_client.id)
    client_user.set_password("Client@123")

    db.session.add_all([director, manager, operator, client_user])

    sample_steps = [
        CaseStep(client_id=sample_client.id, step_name="Profile Created", step_status="completed", step_note="Initial onboarding completed.", step_date="2026-01-12"),
        CaseStep(client_id=sample_client.id, step_name="Form Submitted", step_status="completed", step_note="Primary application submitted.", step_date="2026-01-25"),
        CaseStep(client_id=sample_client.id, step_name="Embassy", step_status="in_progress", step_note="Embassy verification pending.", step_date="2026-03-01"),
    ]
    db.session.add_all(sample_steps)

    db.session.add(VaultEntry(
        entry_category="Corporate Banking",
        label="Primary Operating Account",
        url="https://examplebank.com",
        username="mfcb.operations",
        password_value="ChangeImmediately@123",
        bank_name="Sample Bank",
        account_title="MFCB (SMC) Private Limited",
        account_number="00112233445566",
        iban="PK00SAMP0000112233445566",
        private_note="Seed vault entry for protected executive access.",
        hidden_flag=True,
    ))

    db.session.add(ConstructionRate(rate_type="Gray Structure", unit_type="marla", rate_value=Decimal("280000"), effective_date="2026-01-01", notes="Seed rate"))
    db.session.add(MaterialRate(steel_rate=Decimal("255000"), cement_rate=Decimal("1450"), sand_rate=Decimal("120"), bajri_rate=Decimal("160"), effective_date="2026-01-01", notes="Seed materials"))

    db.session.add(ConstructionProject(
        project_name="Corporate Residence Package",
        project_received_status="received",
        square_feet=Decimal("0"),
        marla=Decimal("10"),
        owner_name="Client Owner",
        owner_phone="+92 333 4445566",
        contractor_name="MFCB Build Team",
        mason_name="Lead Mason",
        labour_details="Core grey structure team assigned.",
        project_type="gray structure",
        rate_used=Decimal("280000"),
        contract_amount=Decimal("0"),
        project_status="in_progress",
        notes="Seed construction project.",
        created_by="MFCB0329"
    ))
    db.session.flush()
    cp = ConstructionProject.query.first()
    apply_module_logic("construction_projects", cp)

    projects = [
        ("Executive Residences", "Pakistan", "Islamabad", "Real Estate", "2018", "Premium housing portfolio delivery.", "A premium residential development managed under the MFCB corporate model with strong planning, controlled execution, and investor confidence."),
        ("Commercial Tower Advisory", "Pakistan", "Lahore", "Construction", "2020", "Commercial construction support and advisory.", "This commercial tower engagement reflects structured planning support, contractor coordination, and business-grade project supervision by MFCB."),
        ("Waterfront Urban Build", "UK", "London", "Real Estate & Construction", "2024", "UK market-facing urban construction profile.", "A UK-facing positioning sample illustrating MFCB's premium construction and development presentation for corporate-grade projects."),
    ]
    for title, country, city, ptype, year, short, full in projects:
        db.session.add(PortfolioProject(title=title, country=country, city=city, project_type=ptype, year_label=year, short_description=short, full_description=full, image_url="https://images.unsplash.com/photo-1460317442991-0ec209397118"))

    uk_addresses = [
        "14 Bishopsgate, London EC2N 3AS",
        "22 King Street, Manchester M2 6AG",
        "71 Queen Street, Glasgow G1 3BZ",
        "8 Broad Street, Birmingham B1 2HF",
        "15 Castle Street, Edinburgh EH2 3AH",
        "110 High Holborn, London WC1V 6JS",
        "45 Temple Row, Birmingham B2 5JT",
        "33 Mosley Street, Newcastle NE1 1YE",
        "90 Deansgate, Manchester M3 2QG",
        "12 Park Square, Leeds LS1 2NL",
        "18 Colmore Circus, Birmingham B4 6AT",
        "40 Princess Street, Manchester M1 6DE",
        "5 Canada Square, London E14 5AQ",
        "21 St Andrew Square, Edinburgh EH2 1AF",
        "66 Queen Square, Bristol BS1 4BE",
        "29 Castle Meadow, Norwich NR1 3DH",
        "101 George Street, Glasgow G1 1RD",
        "7 Corn Street, Bristol BS1 1HT",
        "16 Grey Street, Newcastle NE1 6AE",
        "24 Chapel Walks, Liverpool L2 8QA",
    ]
    for label in uk_addresses:
        db.session.add(UKAddress(label=label))

    people = PeopleMatter(person_name="Ali Raza", phone="03001234567", total_amount=Decimal("250000"), paid_amount=Decimal("100000"), currency="PKR", payment_method="Bank Transfer", transaction_id="TXN-1001", contact_mode="Phone", case_flag="priority", case_details="Settlement support", notes="Initial record", status="pending", created_by="manager01")
    apply_module_logic("people", people)
    db.session.add(people)

    db.session.add(LegalCase(person_name="Barrister Ahmed", role_type="lawyer", phone="03005550000", case_purpose="Property documentation", department_name="Legal Chamber", amount_paid=Decimal("50000"), amount_pending=Decimal("25000"), payment_method="Cash", transaction_id="LG-001", case_status="in_progress", agreement_status="active", notes="Seed legal case", created_by="manager01"))
    db.session.add(RiskRecord(person_name="Subject One", phone="03009998888", risk_level="high", background="Open market dispute flag.", notes="Watch carefully.", created_by="operator01"))

    lending = LendingRecord(person_name="Recoverable Party", entry_type="recoverable", reason="Advance issued", amount_given=Decimal("120000"), amount_received_back=Decimal("20000"), currency="PKR", payment_method="Cash", entry_date="2026-02-01", notes="Seed lending record", status="pending", created_by="operator01")
    apply_module_logic("lending", lending)
    db.session.add(lending)

    db.session.add(PersonalFinance(entry_type="received", relation_name="Family Partner", relation_type="Brother", category="Support", amount=Decimal("45000"), currency="PKR", payment_method="Cash", source_detail="Internal support", entry_date="2026-02-18", purpose="Home support", notes="Seed personal finance", created_by="manager01"))
    db.session.add(HouseholdExpense(expense_group="electricity bill", item_name="January Electricity", beneficiary="Household", amount=Decimal("18500"), currency="PKR", payment_method="Online", expense_date="2026-01-30", paid_status="paid", source_of_funds="Business owner", purpose="Monthly utility", notes="Seed household expense", created_by="operator01"))

    db.session.commit()

with app.app_context():
    db.create_all()
    seed_data()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
