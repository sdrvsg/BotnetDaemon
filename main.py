from flask import Flask
from flask_login import LoginManager
from database import session
from blueprints.main import blueprint as bp_main
from blueprints.auth import blueprint as bp_auth
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eg5e4a5a5v4j4fd4h'

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(bp_main)
app.register_blueprint(bp_auth)

session.global_init('database/bot_net.sqlite')


@login_manager.user_loader
def load_user(user_id):
    connect = session.create_session()
    return connect.query(User).get(user_id)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
