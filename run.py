from app import create_app, db
from app.models import User, Franchise
from werkzeug.security import generate_password_hash

app = create_app()

# ---------------------------------------------------------
# DATABASE CREATION + SEED USERS
# ---------------------------------------------------------
with app.app_context():
    db.create_all()

    # Only insert if DB is empty
    if not User.query.first():

        franchise = Franchise(name="Downtown Motors", address="123 Main St")
        db.session.add(franchise)
        db.session.commit()

        # Owner
        owner = User(
            username="owner1",
            password=generate_password_hash("owner123"),
            role="owner",
            franchise_id=franchise.id
        )

        # Customers of this franchise
        customer1 = User(
            username="customer1",
            password=generate_password_hash("cust123"),
            role="customer",
            franchise_id=franchise.id
        )

        customer2 = User(
            username="customer2",
            password=generate_password_hash("cust456"),
            role="customer",
            franchise_id=franchise.id
        )

        db.session.add_all([owner, customer1, customer2])
        db.session.commit()

        print("Database created and sample users added ✔")
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
