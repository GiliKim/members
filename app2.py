import os
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

db_url = os.getenv("DATABASE_URL", "sqlite:///members.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=True)
    membership_type = db.Column(db.String(20), nullable=False, default="monthly")
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    expiry_date = db.Column(db.Date, nullable=False)

    def is_expired(self, today=None):
        today = today or date.today()
        return self.expiry_date < today

with app.app_context():
    db.create_all()

DURATIONS = {"monthly": 1, "quarterly": 3, "yearly": 12}

def calc_expiry(start: date, membership_type: str) -> date:
    months = DURATIONS.get(membership_type, 1)
    return start + relativedelta(months=+months)

@app.get("/")
def index():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "all")
    mtype = request.args.get("mtype", "all")
    today = date.today()
    query = Member.query
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Member.name.ilike(like), Member.phone.ilike(like)))
    if mtype in DURATIONS or mtype == "yearly":
        query = query.filter_by(membership_type=mtype)
    members = query.order_by(Member.id.desc()).all()
    if status == "active":
        members = [m for m in members if not m.is_expired(today)]
    elif status == "expired":
        members = [m for m in members if m.is_expired(today)]
    return render_template("index.html", members=members, q=q, status=status, mtype=mtype, today=today)

@app.post("/add")
def add_member():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip() or None
    membership_type = request.form.get("membership_type", "monthly")
    start_str = request.form.get("start_date", "")
    expiry_str = request.form.get("expiry_date", "")
    if not name:
        flash("이름은 필수입니다.", "error")
        return redirect(url_for("index"))
    try:
        if start_str:
            y, m, d = map(int, start_str.split("-"))
            start = date(y, m, d)
        else:
            start = date.today()
    except Exception:
        flash("시작일 형식이 올바르지 않습니다. (YYYY-MM-DD)", "error")
        return redirect(url_for("index"))
    if expiry_str:
        try:
            y, m, d = map(int, expiry_str.split("-"))
            expiry = date(y, m, d)
        except Exception:
            flash("만료일 형식이 올바르지 않습니다. (YYYY-MM-DD)", "error")
            return redirect(url_for("index"))
    else:
        expiry = calc_expiry(start, membership_type)
    member = Member(name=name, phone=phone, membership_type=membership_type, start_date=start, expiry_date=expiry)
    db.session.add(member)
    db.session.commit()
    flash("회원이 추가되었습니다.", "success")
    return redirect(url_for("index"))

@app.post("/delete/<int:member_id>")
def delete_member(member_id):
    m = Member.query.get_or_404(member_id)
    db.session.delete(m)
    db.session.commit()
    flash("회원이 삭제되었습니다.", "success")
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return {"ok": True}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)
