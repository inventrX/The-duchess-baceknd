from app.core.database import SessionLocal
from app.models.models import AdminUser
from app.core.security import hash_password

def create_first_admin():
    db = SessionLocal()
    
    # Change these to whatever you want your admin login to be
    admin_email = "admin@theduchess.com"
    admin_password = "supersecretpassword123"
    
    # Check if admin already exists
    existing_admin = db.query(AdminUser).filter(AdminUser.email == admin_email).first()
    if existing_admin:
        print(f"Admin {admin_email} already exists!")
        db.close()
        return

    # Create new admin
    hashed_pw = hash_password(admin_password)
    new_admin = AdminUser(email=admin_email, hashed_password=hashed_pw)
    
    db.add(new_admin)
    db.commit()
    db.close()
    
    print(f"Success! Admin created with email: {admin_email}")

if __name__ == "__main__":
    create_first_admin()