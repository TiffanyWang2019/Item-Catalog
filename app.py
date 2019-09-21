# -*- coding: utf-8 -*-

from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import (
   Flask,
   redirect,
   url_for,
   render_template,
   request,
   session,
   jsonify
)
from flask_oauthlib.client import OAuth
from functools import wraps
import json
import os
import google.oauth2.credentials
import googleapiclient.discovery
from flask_migrate import Migrate


app = Flask(__name__)
app.config['GOOGLE_ID'] = "17614516131-qf2o1gn2cop4l200agt15ke45r9hqqgf.apps.googleusercontent.com"  # noqa
app.config['GOOGLE_SECRET'] = "-bTgr4zCGgDEk7gaGd1yZmBF"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

# google authorization
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] is True:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


# ======== Routing ========== #
# -------- Login ------------ #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    session['logged_in'] = True
    session['username'] = user.username
    session['userid'] = user.id
    return redirect(url_for('showcatalogs'))


@app.route('/loginGoogle')
def loginGoogle():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    data = me.data
    email = data['email']
    session['logged_in'] = True
    session['username'] = email
    if helpers.is_registered(email) == 0:
        password = helpers.hash_password(email)
        helpers.add_user(email, password, email)
    user = helpers.get_user_by_email(email)
    id = user.id
    session['userid'] = id
    return redirect(url_for('showcatalogs'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/showcatalogs', methods=['GET', 'POST'])
@login_required
def showcatalogs():
    # if the request is not ajax
    # then render page
    if not request.is_xhr:
        catalog = helpers.query_catalog()
        item_details = helpers.query_catalog_and_item()
        return render_template('home.html',
                               catalog=catalog,
                               item_details=item_details)
    else:
        item_details = helpers.query_bycatalogid_and_item(request.form['id'])
        list = []
        for item in item_details:
            list.append({"catalog_name": item.catalog_name,
                         "id": item.id, "item_name": item.item_name})
        return json.dumps({"ret": list})


@app.route('/showall/api/v1.0/all.json', methods=['GET'])
@login_required
def get_tasks():
    item_details = helpers.query_catalog_and_item()
    ret = []
    for item in item_details:
        ret.append({"item": item.item_name, "category": item.catalog_name})
    return jsonify({'Category': ret})


@app.route('/queryitem/api/v1.0/item/<item_id>', methods=['GET'])
@login_required
def get_item(item_id):
    item_details = helpers.query_item(item_id)
    if (len(item_details) == 0):
        return jsonify({'Category': "empty"})
    ret = []
    for item in item_details:
        ret.append({"item": item.item_name, "category": item.catalog_name})
    return jsonify({'Category': ret})


@app.route('/addcategory', methods=['GET', 'POST'])
@login_required
def addcategory():
    if request.method == 'GET':
        return render_template('addCategory.html')
    else:
        category = request.form['category'].lower()
        helpers.add_catalog(category)
        return redirect(url_for('showcatalogs'))


@app.route('/additem', methods=['GET', 'POST'])
@login_required
def additem():
    if request.method == 'GET':
        catalog = helpers.query_catalog()
        return render_template('additem.html', catalog=catalog)
    else:
        item_text = request.form['item_text'].lower()
        description_text = request.form['description_text'].lower()
        id = request.form['categoryId']
        user_id = session['userid']
        helpers.add_item(item_text, description_text, id, user_id)
        return redirect(url_for('showcatalogs'))


@app.route('/showitem/<item_id>', methods=['GET', 'POST'])
@login_required
def showedititem(item_id):
    if request.method == 'GET':
        item = helpers.query_item(item_id)
        return render_template('showitem.html', item=item[0])
    elif request.method == 'POST' and 'action' in request.form and request.form['action'] == 'save':  # noqa
        # save action
        item_text_value = request.form['item_text']
        description_text = request.form['description_text']
        user_id = session['userid']
        item = helpers.query_item(item_id)[0]
        if (item.user_id == user_id):
            helpers.update_item(item_id, item_text_value, description_text)
            return redirect(url_for('showcatalogs'))
        else:
            # no permission to do update
            return render_template('message.html', msg="update")
    elif request.method == 'POST' and 'action' in request.form and request.form['action'] == 'delete':  # noqa
        # delete action
        user_id = session['userid']
        item = helpers.query_item(item_id)[0]
        if (item.user_id == user_id):
            helpers.delete_item(item_id)
            return redirect(url_for('showcatalogs'))
        else:
            return render_template('message.html', msg="delete")
    else:
        return redirect(url_for('showcatalogs'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('google_token', None)
    session.clear()
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings -------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# ======== Main ============ #
if __name__ == "__main__":
    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    # app.run(debug=True, use_reloader=True)
    app.run(host='3.14.14.218', port=80, debug=True, use_reloader=True)
