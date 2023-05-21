from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager



class User(UserMixin, db.Model):
    """Base user model for all application users"""
    __tablename__ = 'users'

    # properties
    id = db.Column(db.Integer, primary_key=True)
    user_tag = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    number = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True)
    joined_date = db.Column(db.DateTime, default=datetime.now())
    
    @property
    def password(self):
        raise AttributeError('PROPERTY NOT ACCESSIBLE')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # relationships
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    payments = db.relationship('Payment', backref='resident', lazy='dynamic')

    # model methods
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<User {}, since {}>'.format(self.user_tag, self.joined_date)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_users(role: str) -> list:
        """Returns a list of user query objects for a specific user role.

        :param role: User role."""
        staff = []
        # IDs by role
        ids = {'staff': [2, 3], 'residents':[1],'agents':[2], 'cleaners':[3]}
        for id in ids[role]:
            staff.append(User.query.filter_by(role_id=id))
        return staff

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
def load_user(user_tag):
    return User.query.get(user_tag)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # role to users relationship
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
    """Payment record class"""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    description = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.now())
    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return '<Payment {} - {}>'.format(self.user_id, self.timestamp)
