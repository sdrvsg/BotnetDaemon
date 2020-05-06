from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from blueprints.main import blueprint as bp_main
from blueprints.bots import blueprint as bp_bots
from blueprints.roles import blueprint as bp_roles
from blueprints.support import blueprint as bp_support
from blueprints.admin import blueprint as bp_admin
from blueprints.auth import blueprint as bp_auth
from blueprints.gateway import blueprint as bp_gateway
from blueprints.api import blueprint as bp_api
from database import session
from models.user import User
from utils.filters import nl2br

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eg5e4a5a5v4j4fd4h'
app.config['DB_HOST'] = '95.216.2.95'
app.config['DB_USER'] = 'csbyteru_lyceum'
app.config['DB_PASSWORD'] = 'ghjdfk23'
app.config['DB_BASE'] = 'csbyteru_botnet'
app.jinja_env.filters['nl2br'] = nl2br

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(bp_main)
app.register_blueprint(bp_bots)
app.register_blueprint(bp_roles)
app.register_blueprint(bp_support)
app.register_blueprint(bp_admin)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_gateway)
app.register_blueprint(bp_api)

session.global_init(
    app.config['DB_HOST'],
    app.config['DB_USER'],
    app.config['DB_PASSWORD'],
    app.config['DB_BASE']
)

csrf = CSRFProtect()
csrf.init_app(app)
csrf.exempt(bp_api)


@login_manager.user_loader
def load_user(user_id):
    connect = session.create_session()
    return connect.query(User).get(user_id)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
