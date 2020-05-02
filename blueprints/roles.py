from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from database import session
from models.role import Role

blueprint = Blueprint('roles', __name__, url_prefix='/roles')


@blueprint.route('/')
def index():
    connect = session.create_session()
    roles = connect.query(Role).filter(Role.cost >= 0).all()
    description = [
        [
            'Низкий приоритет тех. поддержки',
            'Только чат-боты'
        ],
        [
            'Техническая поддержка: 24 / 7',
            'Средний приоритет тех. поддержки'
        ],
        [
            'Высокий приоритет тех. поддержки',
            'Уникальные боты'
        ]
    ]
    return render_template('roles/index.html', title='Статусы', roles=roles, description=description)


@blueprint.route('/buy/<int:role_id>')
def buy(role_id):
    connect = session.create_session()
    role = connect.query(Role).get(role_id)
    if not role or role.cost < 0 or current_user.role.id >= role.id:
        return redirect(url_for('roles.index'))
    if current_user.money < role.cost:
        return redirect(url_for('gateway.payment'))
    current_user.money -= role.cost
    current_user.role_id = role.id
    connect.merge(current_user)
    connect.commit()
    return redirect(url_for('roles.success', role_id=role.id))


@blueprint.route('/success/<int:role_id>')
def success(role_id):
    connect = session.create_session()
    return render_template('roles/success.html', title='Успешно', role=connect.query(Role).get(role_id))
