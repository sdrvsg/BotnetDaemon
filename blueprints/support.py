from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from database import session
from models.ticket import Ticket
from models.message import Message
from forms.ticket import TicketForm
from forms.message import MessageForm
from utils.decorators import ticket_owner_required, ticket_opened_required

blueprint = Blueprint('support', __name__, url_prefix='/support')


@blueprint.route('/')
@login_required
def index():
    connect = session.create_session()
    tickets = connect.query(Ticket).filter(Ticket.user == current_user).order_by(Ticket.is_closed).all()
    k = lambda x: x.created_at
    return render_template('support/index.html', title='Поддержка', tickets=tickets, k=k)


@blueprint.route('/ticket/<int:ticket_id>',  methods=['GET', 'POST'])
@login_required
@ticket_owner_required
@ticket_opened_required
def show(ticket_id):
    connect = session.create_session()
    ticket = connect.query(Ticket).get(ticket_id)
    form = MessageForm()
    if form.validate_on_submit():
        message = Message()
        message.text = form.text.data
        ticket.messages.append(message)
        message.user_id = current_user.id
        connect.commit()
        return redirect(url_for('support.show', ticket_id=ticket_id))
    messages = connect.query(Message).filter(Message.ticket == ticket).order_by(Message.created_at.desc()).all()
    return render_template('support/show.html', title=ticket.title, ticket=ticket, messages=messages, form=form)


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TicketForm()
    if form.validate_on_submit():
        connect = session.create_session()
        ticket = Ticket()
        ticket.title = form.title.data
        ticket.is_closed = False
        ticket.priority = current_user.role.support_priority
        message = Message()
        message.text = form.text.data
        ticket.messages.append(message)
        current_user.messages.append(message)
        current_user.tickets.append(ticket)
        connect.merge(current_user)
        connect.commit()
        ticket = connect.query(Ticket).all()[-1]
        return redirect(url_for('support.show', ticket_id=ticket.id))
    return render_template('support/create.html', title='Новое обращение', form=form)


@blueprint.route('/close/<int:ticket_id>')
@login_required
@ticket_owner_required
@ticket_opened_required
def close(ticket_id):
    connect = session.create_session()
    ticket = connect.query(Ticket).get(ticket_id)
    ticket.is_closed = True
    connect.commit()
    return redirect(url_for('support.index'))
