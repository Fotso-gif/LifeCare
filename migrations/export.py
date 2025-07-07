import click
from flask import current_app
from flask.cli import with_appcontext
from your_app.models import db

@app.cli.command('export-db')
@with_appcontext
def export_db():
    """Export database to SQL file"""
    from sqlalchemy import create_engine
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    
    with engine.connect() as conn:
        with open('db_export.sql', 'w') as f:
            for line in conn.connection.iterdump():
                f.write('%s\n' % line)
    
    click.echo("Database exported to db_export.sql")