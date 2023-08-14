from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager



class User(db.Model, UserMixin):
    """Base user model for appliactiion."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    user_tag = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    gender = db.Column(db.String(32))
    role = db.Column(db.String(32))
    email = db.Column(db.String(128), unique=True)
    number = db.Column(db.String(64))
    is_active = db.Column(db.BOOLEAN, default=True)
    joined_date = db.Column(db.DateTime, default=datetime.now())
    is_staff = db.Column(db.BOOLEAN, default=False)
    # `is_new` boolean will reset to False after the user has completed signup
    # the field sets up to always redirect new tenants and owners to signup
    is_new = db.Column(db.BOOLEAN, default=True)
    # outstanding fees
    outstanding_rent = db.Column(db.Integer, default=0)
    outstanding_service_charge = db.Column(db.Integer, default=0)
    # lease duration in number of years
    lease_duration = db.Column(db.Integer, default=1)
    # expiry date is DateTime of datetime.now() + lease duration years
    lease_start = db.Column(db.DateTime)
    lease_expiry = db.Column(db.DateTime)
    
    """RELATIONSHIPS"""
    payments = db.relationship('Payment', backref='tenant', lazy='dynamic')

    """PASSWORD METHODS AND VERIFICATION"""
    @property
    def password(self) -> AttributeError:
        raise AttributeError('PROPERTY NOT ACCESSIBLE')

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    """----------------------------------------------------------"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '<{} - {}>'.format(self.__class__.__name__, self.user_tag)

    def generate_tag(self) -> None:
        """Generates a user's tag. For staff, owners and residents only."""
        if self.user_tag is None:
            # using first letter of role name
            prefix = self.role[0]
            # hash username of email and use the trimmed hash
            username = self.email.split('@')[0]
            hash = generate_password_hash(username)[-5:]
            tag = prefix + hash
            self.user_tag = tag.lower()

    def get_users(role: str) -> db.Query:
        """Returns a query of user objects for a specific user role.

        :param role: User role."""
        if role == 'staff':
            return User.query.filter_by(is_staff=True)
        return User.query.filter_by(role=role.upper())


@login_manager.user_loader
def load_user(user_tag):
    return User.query.get(user_tag)

""" The association table for the flats and users many-to-many relationship."""
flat_link = db.Table('flat_link',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('flat_id', db.Integer, db.ForeignKey('flats.id'))
)


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


class Flat(db.Model):
    """Flat record per flat in every block in the estate."""
    __tablename__ = 'flats'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    block = db.Column(db.Integer)

    """RELATIONSHIPS"""
    users = db.relationship(
        'User',
        secondary=flat_link,
        backref=db.backref('flats', lazy='dynamic'),
        lazy='dynamic'
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '<Block {} Flat {}>'.format(self.block, self.number)

    def populate_flats() -> None:
        """Use to populate flats table with all 64 estate flats."""
        # 64 blocks
        for block in range(1, 65):
            # 8 flats per block
            for number in range(1, 9):
                flat = Flat(number=number, block=block)
                db.session.add(flat)
        db.session.commit()