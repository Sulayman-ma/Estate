from estate import create_app
from config import Config
from estate import db
from estate.models import (
    User,
    Role,
    Payment,
    Flat,
    FlatType,
    Block
)



app = create_app(Config)

@app.shell_context_processor
def context_processor():
    return dict(db=db, Role=Role, Payment=Payment, User=User, Flat=Flat, FlatType=FlatType, Block=Block)