import click
from sayhello import app, db


@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized database')
