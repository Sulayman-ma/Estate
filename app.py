from estate import create_app, db
from config import Config
from estate.models import (
    User,
    Payment,
    Flat,
    flat_link
)

app = create_app(Config)

@app.shell_context_processor
def context_processor():
    return dict(
        db=db, 
        Payment=Payment, 
        User=User, 
        Flat=Flat, 
        flat_link=flat_link
    )