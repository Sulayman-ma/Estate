from estate import create_app, db
from estate.duckstack.transaction import Transaction
from config import Config
from estate.models import (
    User,
    Flat,
    flat_link
)

app = create_app(Config)

# PAYSTACK TRANSACTION OBJECT FOR WHOLE APP
transaction = Transaction(app.config.get('API_KEY'))
app.config.setdefault('API_OBJECT', transaction)

@app.shell_context_processor
def context_processor():
    return dict(
        db=db, 
        User=User, 
        Flat=Flat, 
        flat_link=flat_link
    )