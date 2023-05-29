from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager



class User(UserMixin, db.Model):
    """User model for all application users."""
    __tablename__ = 'users'

    # properties
    id = db.Column(db.Integer, primary_key=True)
    user_tag = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(128))
    number = db.Column(db.String(64))
    is_active = db.Column(db.BOOLEAN)
    is_staff = db.Column(db.BOOLEAN, default=False)
    joined_date = db.Column(db.DateTime, default=datetime.now())
    # lease duration in number of years
    lease_duration = db.Column(db.Integer)
    # expiry date is DateTime of datetime.now() + lease duration years
    lease_expiry = db.Column(db.DateTime)
    lease_start = db.Column(db.DateTime)
    
    @property
    def password(self):
        raise AttributeError('PROPERTY NOT ACCESSIBLE')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # relationships
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), name='fk_user_role_id')
    payments = db.relationship('Payment', backref='resident', lazy='dynamic')
    # flat = db.relationship('Flat', uselist=False, backref='resident')
    flattype_id = db.Column(db.Integer, db.ForeignKey('flattypes.id'), name='fk_resident_flattype_id')

    # model methods
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<User {}, since {}>'.format(self.user_tag, self.joined_date)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_users(role: str) -> list:
        """Returns a query of user objects for a specific user role.

        :param role: User role."""
        if role == 'staff':
            return User.query.filter_by(is_staff=True)
        ids = {'resident': 1, 'agent': 2, 'cleaner': 3}
        return User.query.filter_by(role_id=ids[role])


    def generate_user_tag(self) -> None:
        """Generates a user's tag."""
        # if user has no tag, generate one.
        if self.user_tag is None:
            prefix = self.role.name[0]
            email_user = self.email.split('@')[0]
            hash = generate_password_hash(email_user)[-5:]
            tag = prefix + hash
            self.user_tag = tag.upper()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    # relationships
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Role {} - {}>'.format(self.id, self.name)

    def create_roles() -> None:
        # run once as needed and never again
        roles = ['RESIDENT', 'AGENT', 'CLEANER', 'ADMIN']
        for role in roles:
            rl = Role(name=role)
            db.session.add(rl)
        db.session.commit()


class Payment(db.Model):
    """Payment record model."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    description = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.now())

    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), name='fk_payment_resident_id')
    # flat_id = db.Column(db.Integer, db.ForeignKey('flats.id'), name='fk_payment_flat')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Payment {} - {}>'.format(self.user_id, self.timestamp)


class FlatType(db.Model):
    """Flat types model with flat description, specifics and rent amount."""
    __tablename__ = 'flattypes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text())
    rent = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer, default=bedrooms)
    total = db.Column(db.Integer)
    num_available = db.Column(db.Integer, default=total)
    
    # relationships
    # flats = db.relationship('Flat', backref='flattype', lazy='dynamic')
    residents = db.relationship('User', backref='flattype', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<{} - ₦{:,}>'.format(self.name, self.rent)


# class Flat(db.Model):
#     """Flat record per flat in every block in the estate."""
#     __tablename__ = 'flats'

#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.Integer)
#     # block = db.Column(db.CHAR)

#     # relationships
#     flattype_id = db.Column(db.Integer, db.ForeignKey('flattypes.id'), name='fk_flat_flattype')
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), name='fk_flat_resident')
#     payment = db.relationship('Payment', backref='flat', uselist=False)
#     block_id = db.Column(db.Integer, db.ForeignKey('blocks.id', name='fk_flat_block'))

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#     def __repr__(self):
#         return '<Flat {}, Block {}>'.format(self.number, self.block_id)

    
# class Block(db.Model):
#     """Block model. To be managed only on the admin side and used for tracking and any necessary features and grouping of flats."""  
#     __tablename__ = 'blocks'

#     id = db.Column(db.Integer, primary_key=True)
#     letter = db.Column(db.CHAR)

#     # relationships
#     # flats = db.relationship('Flat', backref='block', lazy='dynamic')

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
    
#     def __repr__(self):
#         return '<Block {}>'.format(self.letter)