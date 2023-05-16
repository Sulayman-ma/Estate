from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager



class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def password(self):
        raise AttributeError('PROPERTY NOT ACCESSIBLE.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies admin password upon login"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """To string method of the object"""
        return "<Admin {}>".format(self.admin_id)


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(admin_id)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # relate role back to staff
    staffs = db.relationship('Staff', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Staff(db.Model):
    __tablename__ = 'staffs'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128))
    staff_id = db.Column(db.String(64), unique=True)
    number = db.Column(db.String(128))
    email = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    # relate staff table and role table with role id as foreign key
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<Role {}, {} - {}>".format(self.role_id, self.staff_id, self.fullname)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Resident(db.Model):
    __tablename__ = 'residents'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128))
    resident_id  = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    number = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=False)
    joined_since = db.Column(db.DateTime, default=datetime.now())
    payments = db.relationship('Payment', backref='resident', lazy='dynamic')

    def __repr__(self):
        return '<Resident {}, joined {}>'.format(self.resident_id, self.joined_since)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('PROPERTY NOT ACCESSIBLE.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies resident password"""
        return check_password_hash(self.password_hash, password)


class Payment(db.Model):
    """Payment record class"""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    # color code to show bought or currently renting
    color_id = db.Column(db.String(64))
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


