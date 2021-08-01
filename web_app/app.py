from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Keyword
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY', 's3cr3t')    

# database information
host = os.environ.get('DB_HOST', 'localhost')
port = os.environ.get('DB_PORT', 5432)
user = os.environ.get('DB_USER', 'postgres')
password = os.environ.get('DB_PASSWORD', 'rootpass')
database = os.environ.get('DB_NAME', 'rank-search')
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
Session = sessionmaker(bind = engine)
session = Session()

@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/')
def index():
    keywords = session.query(Keyword).order_by(Keyword.is_active.desc(), Keyword.priority.desc()).all()
    return render_template("keyword/index.html", keywords=keywords)


@app.route('/keyword/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    keyword = session.query(Keyword).filter_by(id=id).first()
    if keyword is None:
        return redirect(url_for('error_not_found'))
    if request.method == 'POST':
        content = request.form['content']
        target_site = request.form['target_site']
        error = None

        if not content:
            error = 'Content is required.'
        elif not target_site:
            error = 'Target site is required.'
        elif content == keyword.content and target_site == keyword.target_site:
            error = 'Nothing to update.'

        if error is not None:
            flash(error)
        else:
            keyword.content = content
            keyword.target_site = target_site
            keyword.url = ''
            keyword.rank = 0
            keyword.error_code = 0
            keyword.last_update = datetime.now()
            session.commit()
            return redirect(url_for('index'))

    return render_template('keyword/update.html', keyword=keyword)


@app.route('/keywords/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        content = request.form['content']
        target_site = request.form['target_site']
        error = None

        if not content:
            error = 'Content is required.'
        elif not target_site:
            error = 'Target site is required.'

        if error is not None:
            flash(error)
        else:
            keyword = Keyword(content=content, target_site=target_site)
            session.add(keyword)
            session.commit()
            return redirect(url_for('index'))

    return render_template('keyword/create.html')


@app.route('/keywords/<int:id>/delete', methods=('POST',))
def delete(id):
    keyword = session.query(Keyword).filter_by(id=id).first()
    if not keyword:
        return redirect(url_for('error_not_found'))
    session.delete(keyword)
    session.commit()
    return redirect(url_for('index'))


@app.route('/keywords/<int:id>/activeToggle', methods=('POST',))
def active_toggle(id):
    keyword = session.query(Keyword).filter_by(id=id).first()
    if not keyword:
        return redirect(url_for('error_not_found'))
    keyword.is_active = not keyword.is_active
    session.commit()
    return redirect(url_for('index'))


@app.route('/error_404')
def error_not_found():
    return render_template('error_404.html')


if __name__ == '__main__':
    app.run(debug=True)

