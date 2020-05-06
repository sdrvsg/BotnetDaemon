from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from database import session
from models.ticket import Ticket
from models.message import Message
from models.role import Role
from forms.message import MessageForm
from forms.role import RoleForm
from utils.decorators import role_required, ticket_opened_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@login_required
@role_required('admin')
def index():
    connect = session.create_session()
    tickets = connect.query(Ticket).filter(Ticket.is_closed == 0).all()
    waiting_tickets_num = 0
    for ticket in tickets:
        if ticket.messages[-1].user == ticket.user:
            waiting_tickets_num += 1
    roles_num = connect.query(Role).count()
    return render_template('admin/index.html', title='Главная', **{
        'waiting_tickets_num': waiting_tickets_num,
        'roles_num': roles_num
    })


@blueprint.route('/support')
@login_required
@role_required('admin')
def support_index():
    connect = session.create_session()
    tickets = connect.query(Ticket)\
        .filter(Ticket.is_closed == 0)\
        .order_by(Ticket.is_closed)\
        .order_by(Ticket.priority.desc())\
        .all()
    tickets_new = filter(lambda x: x.user_id == sorted(x.messages, key=lambda y: y.created_at)[-1].user_id, tickets)
    tickets_old = filter(lambda x: x.user_id != sorted(x.messages, key=lambda y: y.created_at)[-1].user_id, tickets)
    return render_template('admin/support/index.html', title='Поддержка', **{
        'tickets_new': tickets_new,
        'tickets_old': tickets_old,
        'Message': Message
    })


@blueprint.route('/support/ticket/<int:ticket_id>',  methods=['GET', 'POST'])
@login_required
@role_required('admin')
@ticket_opened_required
def support_show(ticket_id):
    connect = session.create_session()
    ticket = connect.query(Ticket).get(ticket_id)
    form = MessageForm()
    if form.validate_on_submit():
        message = Message()
        message.text = form.text.data
        ticket.messages.append(message)
        message.user_id = current_user.id
        connect.commit()
        return redirect(url_for('admin.support_show', ticket_id=ticket_id))
    messages = connect.query(Message).filter(Message.ticket == ticket).order_by(Message.created_at.desc()).all()
    return render_template('admin/support/show.html', title=ticket.title, ticket=ticket, messages=messages, form=form)


@blueprint.route('support/close/<int:ticket_id>')
@login_required
@role_required('admin')
@ticket_opened_required
def support_close(ticket_id):
    connect = session.create_session()
    ticket = connect.query(Ticket).get(ticket_id)
    ticket.is_closed = True
    connect.commit()
    return redirect(url_for('admin.support_index'))


@blueprint.route('/roles')
@login_required
@role_required('admin')
def roles_index():
    connect = session.create_session()
    roles = connect.query(Role).all()
    return render_template('admin/roles/index.html', title='Роли', roles=roles)


@blueprint.route('/roles/edit/<int:role_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def roles_edit(role_id):
    form = RoleForm()
    if request.method == 'GET':
        connect = session.create_session()
        role = connect.query(Role).get(role_id)
        form.name.data = role.name
        form.styles.data = role.styles
        form.cost.data = role.cost
        form.bots_limit.data = role.bots_limit
        form.support_priority.data = role.support_priority
    if form.validate_on_submit():
        connect = session.create_session()
        role = connect.query(Role).get(role_id)
        role.name = form.name.data
        role.styles = form.styles.data
        role.cost = form.cost.data
        role.bots_limit = form.bots_limit.data
        role.support_priority = form.support_priority.data
        connect.commit()
        return redirect(url_for('admin.roles_index'))
    return render_template('admin/roles/edit.html', title='Редактирование роли', form=form)
