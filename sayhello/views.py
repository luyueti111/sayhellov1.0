from flask import flash, redirect, url_for, render_template
from sayhello import app, db
from sayhello.models import Message, Page
from sayhello.forms import HelloForm, SearchForm, ReplyForm
from sqlalchemy import or_
from datetime import datetime
from faker import Faker

fake = Faker()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        page = Page(body=body, name=name)
        db.session.add(message)
        db.session.add(page)
        message.pages.append(page)
        db.session.commit()
        return redirect(url_for('index'))
    form.name.data = fake.name()
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index_with_base.html',
                           form=form,
                           messages=messages)


@app.route('/search', methods=['GET', 'POST'])
def searchMessage():
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        searchRule = searchForm.body.data
        searchedMessage = Message.query.filter(or_(Message.body.like('%'+searchRule+'%'),
                                                   Message.name.like('%'+searchRule+'%')))

        return render_template('search.html',
                               searchNumber=searchedMessage.count(),
                               messages=searchedMessage,
                               searchForm=searchForm)


@app.route('/page/<int:message_id>', methods=['GET', 'POST'])
def replyPage(message_id):
    replyForm = ReplyForm()
    message = Message.query.get(message_id)
    message.clickNum += 1
    pages = message.pages
    db.session.commit()
    if replyForm.validate_on_submit():
        name = replyForm.name.data
        body = replyForm.body.data
        page = Page(body=body, name=name)
        message.timestamp = datetime.now()
        message.replyNum += 1
        db.session.add(page)
        message.pages.append(page)
        db.session.commit()
        return redirect(url_for('replyPage', message_id=message_id))
    replyForm.name.data = fake.name()
    return render_template('reply.html',
                           messages=pages,
                           form=replyForm)


@app.context_processor
def injectSearchForm():
    searchForm = SearchForm()
    return dict(searchForm=searchForm)


@app.route('/testIphone')
def testIndex():
    return render_template('testh.html')
