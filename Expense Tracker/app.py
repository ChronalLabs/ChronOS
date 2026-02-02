from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Expense, Budget
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_change_in_production'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    # Get expenses for current month only
    today = date.today()
    first_day = today.replace(day=1)
    
    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).filter(Expense.date >= first_day).order_by(
        Expense.date.desc()
    ).all()
    
    total_spent = sum(e.amount for e in expenses)
    
    budget_obj = Budget.query.filter_by(user_id=current_user.id).first()
    monthly_budget = budget_obj.monthly_budget if budget_obj else 0
    remaining = max(0, monthly_budget - total_spent)

    # Category breakdown for chart - JSON SAFE
    categories = {}
    for e in expenses:
        categories[e.category] = categories.get(e.category, 0) + e.amount

    return render_template('index.html', 
                         expenses=expenses, 
                         total_spent=total_spent,
                         monthly_budget=monthly_budget, 
                         remaining=remaining,
                         chart_data=categories)  # ✅ Fixed: chart_data for template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']

        if not all([name, email, password]):
            flash('Please fill all fields.')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists.')
            return redirect(url_for('signup'))

        try:
            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!')
            return redirect(url_for('login'))
        except Exception:
            db.session.rollback()
            flash('Error creating account. Try again.')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/add-expense', methods=['POST'])
@login_required
def add_expense():
    try:
        amount = float(request.form['amount'])
        category = request.form['category'].strip()
        note = request.form.get('note', '').strip()

        if amount <= 0:
            flash('Amount must be greater than 0.')
            return redirect(url_for('index'))

        expense = Expense(
            amount=amount, 
            category=category, 
            note=note, 
            date=datetime.utcnow().date(),
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!')
    except ValueError:
        flash('Invalid amount.')
    except Exception:
        db.session.rollback()
        flash('Error adding expense.')
    
    return redirect(url_for('index'))

@app.route('/set-budget', methods=['POST'])
@login_required
def set_budget():
    try:
        amount = float(request.form['budget'])
        if amount < 0:
            flash('Budget cannot be negative.')
            return redirect(url_for('index'))

        # Delete existing budget and create new one
        Budget.query.filter_by(user_id=current_user.id).delete()
        budget = Budget(monthly_budget=amount, user_id=current_user.id)
        db.session.add(budget)
        db.session.commit()
        flash('Budget updated successfully!')
    except ValueError:
        flash('Invalid budget amount.')
    except Exception:
        db.session.rollback()
        flash('Error setting budget.')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
