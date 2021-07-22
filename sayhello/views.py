from flask import flash, redirect, url_for, render_template
from sayhello import app, db
from sayhello.models import Message
from sayhello.forms import HelloForm, SearchForm
from sqlalchemy import or_


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    searchForm = SearchForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('index'))
    messages = Message.query.all()
    return render_template('index_with_base.html',
                           form=form,
                           searchForm=searchForm,
                           messages=list(reversed(messages)))


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
