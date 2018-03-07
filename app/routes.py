from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, EditIncomeForm
from app.email import send_password_reset_email 
from app.models import User, Expense, Income
from flask_babel import _, get_locale
import sys

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    
    if 'lang' in session:
        g.locale = session['lang']
    else:
        g.locale = 'en'
    
    if g.locale == 'de':
        g.locale_description = _('German')
    elif g.locale == 'sr':
        g.locale_description = _('Serbian')
    else:
        g.locale_description = _('English')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title=_('Home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=_('Sign In'), form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html', title=_('Register'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    e = Expense.query.filter_by(user_id=current_user.id)
    return render_template('expenses.html', title=_('Expenses'),expenses=e)

@app.route('/incomes', methods=['GET', 'POST'])
@login_required
def incomes():
    i = Income.query.filter_by(user_id=current_user.id)
    return render_template('incomes.html', title=_('Incomes'),incomes=i)

@app.route('/incomes/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_income(id):
    i = Income.query.filter_by(id=id).first_or_404()
    form = EditIncomeForm()
    if form.validate_on_submit():
        i.description = form.description.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('incomes'))
    elif request.method == 'GET':
        form.id.data = i.id
        form.description.data = i.description
    return render_template('edit_income.html', title=_('Edit Income'),
                           form=form) 

@app.route('/incomes/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_income(id):
    flash(_('Deleted.'))
    return redirect(url_for('incomes'))

@app.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    return render_template('posts.html', title=_('Posts'))

@app.route('/lang/<lang>')
def lang(lang):
    g.locale = lang
    session['lang']=lang
    return redirect(url_for('index'))