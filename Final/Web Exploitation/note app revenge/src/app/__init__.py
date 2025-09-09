from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    limiter = Limiter(
        get_remote_address,
        storage_uri="memory://",
    )
        
    app.config['SECRET_KEY'] = 'kiseki-top-secr3t-P4$$-KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    @app.before_request
    def generate_nonce():
        g.nonce = uuid.uuid4().hex

    @app.context_processor
    def inject_nonce():
        return {'nonce': getattr(g, 'nonce', '')}
    
    from .auth import auth_bp
    from .notes import notes_bp
    from .bot import bot_bp

    limiter.limit("3 per hour")(bot_bp)
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(bot_bp, url_prefix='/bot')

    with app.app_context():
        db.create_all()
        
        from .models import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin_user = User(
                username='admin',
                email='admin@itsec.asia',
                is_admin=True
            )
            admin_user.set_password('SecUr3ADM00NP4$$')
            db.session.add(admin_user)
            db.session.commit()

    limiter.init_app(app)
    
    return app
