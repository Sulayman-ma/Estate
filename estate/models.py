from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager



class User(db.Model, UserMixin):
    """User model for all application users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_tag = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(128))
    number = db.Column(db.String(64))
    is_active = db.Column(db.BOOLEAN, default=True)
    # is_staff = db.Column(db.BOOLEAN, default=False)
    joined_date = db.Column(db.DateTime, default=datetime.now())
    # outstanding fees
    outstanding_rent = db.Column(db.Integer, default=0)
    outstanding_service_charge = db.Column(db.Integer, default=0)
    # lease duration in number of years
    lease_duration = db.Column(db.Integer, default=1)
    # expiry date is DateTime of datetime.now() + lease duration years
    lease_start = db.Column(db.DateTime)
    lease_expiry = db.Column(db.DateTime)
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '<User {}, since {}>'.format(self.user_tag, self.joined_date)

    """PASSWORD METHODS AND VERIFICATION"""
    @property
    def password(self) -> AttributeError:
        raise AttributeError('PROPERTY NOT ACCESSIBLE')

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    """RELATIONSHIPS"""
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', name='fk_user_role_id'))
    payments = db.relationship('Payment', backref='tenant', lazy='dynamic')
    flat = db.relationship('Flat', uselist=False, backref='tenant')

    def get_users(role: str) -> db.Query:
        """Returns a joint query of users given the role; staff for all managers and handymen, tenants, managers and handymen."""
        categs = {'handyman': 4, 'manager': 2, 'tenant': 3}
        if role == 'staff':
            managers = User.query.filter_by(role_id=2)
            handymen = User.query.filter_by(role_id=4)
            staff = managers.union(handymen)
            return staff
        return User.query.filter_by(role_id=categs[role])

    def generate_user_tag(self) -> None:
        """Generates a user's tag. For admin and residents only."""
        if self.user_tag is None:
            # using first letter of role name
            prefix = self.role.name[0]
            # hash part of email and use part of hash
            email_user = self.email.split('@')[0]
            hash = generate_password_hash(email_user)[-5:]
            tag = prefix + hash
            self.user_tag = tag.lower()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Role(db.Model):
    """User roles, including the tenants, managers, handymen and admin."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    """RELATIONSHIPS"""
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '<Role {} - {}>'.format(self.id, self.name)

    def create_roles() -> None:
        # run once upon database intiation
        roles = ['ADMIN', 'MANAGER', 'TENANT', 'HANDYMAN']
        for role in roles:
            rl = Role(name=role)
            db.session.add(rl)
        db.session.commit()


class Payment(db.Model):
    """Payment record model."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    # service charge or rent
    type = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    # status; full or partial payment
    status = db.Column(db.String(128))
    # year corresponding to payment
    year = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now())

    """RELATIONSHIPS"""
    user_tag = db.Column(db.Integer, db.ForeignKey('users.user_tag', name='fk_payment_tenant_tag'))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '<Payment {} - {}>'.format(self.user_id, self.timestamp)


class FlatType(db.Model):
    """Flat type for 2 or 3 bedroom"""
    __tablename__ = "flattypes"

    id = db.Column(db.Integer, primary_key=True)
    bedrooms = db.Column(db.Integer)
    rent = db.Column(db.Integer)
    service_charge = db.Column(db.Integer)

    """RELATIONSHIPS"""
    flats = db.relationship('Flat', backref='type', lazy='dynamic')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '<FlatType #{}, {} bedrooms>'.format(self.id, self.bedrooms)


class Flat(db.Model):
    """Flat record per flat in every block in the estate."""
    __tablename__ = 'flats'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    # blocks lettered A - D
    block = db.Column(db.CHAR)

    """RELATIONSHIPS"""
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_user_flat_id'))
    flattype_id = db.Column(db.Integer, db.ForeignKey('flattypes.id', name='fk_flat_type_id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '<Flat {}, Block {}>'.format(self.number, self.block)

    def populate_flats(block: str, type_id: int, count: int) -> None:
        """Use to populate flats table records with all estate flats.

        :param block: Block letter
        :param type_id: The FlatType to be set
        :param count: The total number of flats for the block"""
        for i in range(1, count+1):
            flat = Flat(number=i, block=block, flattype_id=type_id)
            db.session.add(flat)
        db.session.commit()