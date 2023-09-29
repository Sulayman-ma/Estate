from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager



class User(db.Model, UserMixin):
    """Base user model for appliactiion."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128), default='')
    last_name = db.Column(db.String(128))
    gender = db.Column(db.String(32))
    role = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    number = db.Column(db.String(64))
    is_active = db.Column(db.BOOLEAN, default=True)
    joined_date = db.Column(db.DateTime, default=datetime.now())
    is_staff = db.Column(db.BOOLEAN, default=False)
    # `is_new` boolean will reset to False after the user has completed signup
    # the field sets up to always redirect new tenants and owners to signup
    is_new = db.Column(db.BOOLEAN, default=True)
    
    """RELATIONSHIPS"""
    # payments = db.relationship('Payment', backref='tenant', lazy='dynamic')

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
        """Generates the username."""
        if self.username is None:
            # using first letter of role name
            prefix = self.role[0]
            # hash username of email and use the trimmed hash
            username = self.email.split('@')[0]
            hash = generate_password_hash(username)[-5:]
            tag = prefix + hash
            self.username = tag.lower()

    def __repr__(self) -> str:
        return '<{} - {}>'.format(self.role, self.username)
    
    def get(username: str) -> db.Query:
        """ Return the `User` instance of the user with the username given.

        :param username: User's username(unique) """
        return User.query.filter_by(username=username).first()

    def get_users(role: str) -> db.Query:
        """Returns a query of user objects for a specific user role.

        :param role: User role."""
        if role == 'staff':
            return User.query.filter_by(is_staff=True)
        return User.query.filter_by(role=role.upper())


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

""" The association table for the flats and users many-to-many relationship."""
flat_link = db.Table('flat_link',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('flat_id', db.Integer, db.ForeignKey('flats.id')),    
)


# class Payment(db.Model):
#     """Payment record model."""
#     __tablename__ = 'payments'

#     id = db.Column(db.Integer, primary_key=True)
#     # buy or rent
#     type = db.Column(db.String(64), nullable=False)
#     amount = db.Column(db.Integer, nullable=False)
#     # status; full or partial payment
#     status = db.Column(db.String(128), nullable=False)
#     # year corresponding to payment
#     year = db.Column(db.Integer, default=datetime.today().year)
#     timestamp = db.Column(db.DateTime, default=datetime.now())

#     """RELATIONSHIPS"""
#     user_id = db.Column(db.String(64), db.ForeignKey('users.id', name='fk_payment_user'))
#     flat_id = db.Column(db.Integer, db.ForeignKey('flats.id', name='fk_payment_flat'))

#     def __init__(self, **kwargs) -> None:
#         super().__init__(**kwargs)

#     def __repr__(self) -> str:
#         return '<Payment {} - {} ({})>'.format(self.timestamp, self.username, self.amount)


class Flat(db.Model):
    """Flat record per flat in every block in the estate."""
    __tablename__ = 'flats'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    block = db.Column(db.Integer, nullable=False)
    for_rent = db.Column(db.BOOLEAN, default=False)
    for_sale = db.Column(db.BOOLEAN, default=True)
    description = db.Column(db.Text())
    # payment_freq = db.Column(db.Integer, default=12)    
    # rent is set by the owner when the flat is bought
    rent = db.Column(db.Integer, default=0)
    # default cost of purchase from LSDPC is 1 mil
    cost = db.Column(db.Integer, default=1000000)
    lease_duration = db.Column(db.Integer, default=1)
    lease_start = db.Column(db.Date)
    # expiry date is DateTime of datetime.now() + lease duration years
    lease_expiry = db.Column(db.Date)
    rent_overdue = db.Column(db.Integer)

    """RELATIONSHIPS"""
    users = db.relationship(
        'User',
        secondary=flat_link,
        backref=db.backref('flats', lazy='dynamic'),
        lazy='dynamic'
    )
    # payments = db.relationship('Payment', backref='flat', lazy='dynamic')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def check_expiry(self) -> None:
        today = datetime.today().date()
        if today >= self.lease_expiry:
            self.rent_overdue = self.rent
        db.session.commit()

    def __repr__(self) -> str:
        return '<Block {}, Flat {}>'.format(self.block, self.number)
    
    def get_tenant(self) -> User:
        return self.users.filter_by(role='TENANT').first()

    def get_owner(self) -> User:
        return self.users.filter_by(role='OWNER').first()
    """ GET AND SET OWNER/TENANT

    Instead of setting owner and tenant, the current owner/tenant is simply removed and the new one is added. All implemented in the necessary view function.
    """

    def populate_flats(b: int, f: int) -> None:
        """Use to populate flats table with all 64 estate flats.
        :param b: number of blocks
        "param f: number of flats per block"""
        # 64 blocks
        for block in range(1, b+1):
            # 8 flats per block
            for number in range(1, f+1):
                flat = Flat(number=number, block=block)
                db.session.add(flat)
        db.session.commit()


class Notice(db.Model):
    __tablename__ = 'notices'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(128), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    target = db.Column(db.String(32), nullable=False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return '<#{} - {}>'.format(self.id, self.subject)