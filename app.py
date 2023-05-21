from flask_migrate import Migrate
from estate import create_app
from config import Config
from estate import db
from estate.models import User, Role, Payment



app = create_app(Config)

# migration extension
migrate = Migrate(app, db)

@app.shell_context_processor
def context_processor():
    return dict(db=db, Role=Role, Payment=Payment, User=User)