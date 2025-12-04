from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Vehicle
from .forms import LoginForm, VehicleForm, CustomerForm
from . import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash

main = Blueprint('main', __name__)

# ------------------------------
# LOGIN MANAGER
# ------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------------------
# LOGIN
# ------------------------------
@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))

        flash("Invalid username or password")

    return render_template('login.html', form=form)


# ------------------------------
# DASHBOARD
# ------------------------------
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'owner':
        vehicles = Vehicle.query.filter_by(franchise_id=current_user.franchise_id).all()
    else:
        vehicles = Vehicle.query.filter_by(owner_id=current_user.id).all()

    return render_template('dashboard.html', vehicles=vehicles)


# ------------------------------
# ADD VEHICLE — OWNER ONLY
# ------------------------------
@main.route('/vehicle/add', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    if current_user.role != 'owner':
        flash("Only owners can add vehicles.")
        return redirect(url_for('main.dashboard'))

    form = VehicleForm()

    customers = User.query.filter_by(franchise_id=current_user.franchise_id, role='customer').all()
    form.owner_id.choices = [(c.id, c.username) for c in customers]

    if form.validate_on_submit():

        # Duplicate check for vehicle number
        existing = Vehicle.query.filter_by(vehicle_number=form.vehicle_number.data).first()
        if existing:
            return render_template(
                'vehicle_form.html',
                form=form,
                duplicate_error="Vehicle number already exists!"
            )

        vehicle = Vehicle(
            vehicle_number=form.vehicle_number.data,
            make=form.make.data,
            model=form.model.data,
            color=form.color.data,
            issue_date=form.issue_date.data,
            registration_status=form.registration_status.data,
            owner_id=form.owner_id.data,
            franchise_id=current_user.franchise_id
        )

        db.session.add(vehicle)
        db.session.commit()
        flash("Vehicle added successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('vehicle_form.html', form=form)


# ------------------------------
# EDIT VEHICLE — OWNER ONLY
# ------------------------------
@main.route('/vehicle/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)

    if current_user.role != 'owner':
        flash("Only owners can edit vehicles.")
        return redirect(url_for('main.dashboard'))

    form = VehicleForm(obj=vehicle)

    customers = User.query.filter_by(franchise_id=current_user.franchise_id, role='customer').all()
    form.owner_id.choices = [(c.id, c.username) for c in customers]

    if form.validate_on_submit():

        # Duplicate check on edit
        existing = Vehicle.query.filter_by(vehicle_number=form.vehicle_number.data).first()
        if existing and existing.id != vehicle.id:
            return render_template(
                'vehicle_form.html',
                form=form,
                duplicate_error="Vehicle number already exists!"
            )

        form.populate_obj(vehicle)
        db.session.commit()
        flash("Vehicle updated successfully.")
        return redirect(url_for('main.dashboard'))

    return render_template('vehicle_form.html', form=form)


# ------------------------------
# DELETE VEHICLE — OWNER ONLY
# ------------------------------
@main.route('/vehicle/delete/<int:id>', methods=['POST'])
@login_required
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)

    if current_user.role != 'owner':
        flash("Only owners can delete vehicles.")
        return redirect(url_for('main.dashboard'))

    db.session.delete(vehicle)
    db.session.commit()
    flash("Vehicle deleted successfully.")
    return redirect(url_for('main.dashboard'))


# ------------------------------
# CUSTOMER LIST — OWNER ONLY
# ------------------------------
@main.route('/customers')
@login_required
def customers():
    if current_user.role != 'owner':
        flash("Only owners can manage customers.")
        return redirect(url_for('main.dashboard'))

    customers = User.query.filter_by(franchise_id=current_user.franchise_id, role='customer').all()
    return render_template('customers.html', customers=customers)


# ------------------------------
# ADD CUSTOMER — OWNER ONLY
# ------------------------------
@main.route('/customer/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if current_user.role != 'owner':
        flash("Not allowed")
        return redirect(url_for('main.dashboard'))

    form = CustomerForm()

    if form.validate_on_submit():
        new_customer = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
            role='customer',
            franchise_id=current_user.franchise_id
        )

        db.session.add(new_customer)
        db.session.commit()
        flash("Customer added successfully.")
        return redirect(url_for('main.customers'))

    return render_template('customer_form.html', form=form)


# ------------------------------
# EDIT CUSTOMER
# ------------------------------
@main.route('/customer/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):

    if current_user.role == 'customer' and current_user.id != id:
        flash("Not allowed")
        return redirect(url_for('main.dashboard'))

    customer = User.query.get_or_404(id)
    form = CustomerForm()

    if request.method == 'POST':
        customer.username = form.username.data

        if form.password.data:
            customer.password = generate_password_hash(form.password.data)

        db.session.commit()
        flash("Customer updated successfully.")

        if current_user.role == 'owner':
            return redirect(url_for('main.customers'))
        return redirect(url_for('main.dashboard'))

    form.username.data = customer.username
    return render_template('customer_form.html', form=form)


# ------------------------------
# DELETE CUSTOMER — BLOCK IF VEHICLES EXIST
# ------------------------------
@main.route('/customer/delete/<int:id>', methods=['POST'])
@login_required
def delete_customer(id):
    if current_user.role != 'owner':
        flash("Not allowed")
        return redirect(url_for('main.dashboard'))

    customer = User.query.get_or_404(id)

    # Prevent self-deletion
    if customer.id == current_user.id:
        flash("You cannot delete yourself!")
        return redirect(url_for('main.customers'))

    # ❗ PREVENT DELETE IF CUSTOMER OWNS VEHICLES
    if customer.vehicles and len(customer.vehicles) > 0:
        customers = User.query.filter_by(franchise_id=current_user.franchise_id, role='customer').all()
        return render_template(
            'customers.html',
            customers=customers,
            vehicle_error=f"Customer '{customer.username}' cannot be deleted because they have assigned vehicles."
        )

    db.session.delete(customer)
    db.session.commit()
    flash("Customer deleted successfully.")
    return redirect(url_for('main.customers'))


# ------------------------------
# LOGOUT
# ------------------------------
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
