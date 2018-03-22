from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, IntegerField, SelectField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User, Expense, Income
from flask_babel import _, lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))

class EditIncomeForm(FlaskForm):
    id = IntegerField('Id', validators=[])
    description = StringField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    
    def __init__(self, *args, **kwargs):
        super(EditIncomeForm, self).__init__(*args, **kwargs)
        # disable the fields if you want to
        self.id.render_kw = {'disabled': True}

class EditExpenseForm(FlaskForm):
    id = IntegerField('Id', validators=[])
    description = StringField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    
    def __init__(self, *args, **kwargs):
        super(EditExpenseForm, self).__init__(*args, **kwargs)
        # disable the fields if you want to
        self.id.render_kw = {'disabled': True}

class EditPostExpenseForm(FlaskForm):
    id = IntegerField('Id', validators=[])
    expense_id = SelectField('ExpenseId', validators=[])
    description = StringField(_l('Description'), validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[])
    submit = SubmitField(_l('Submit'))
    
    def __init__(self, *args, **kwargs):
        super(EditPostExpenseForm, self).__init__(*args, **kwargs)
        # disable the fields if you want to
        self.id.render_kw = {'disabled': True}

class EditPostIncomeForm(FlaskForm):
    id = IntegerField('Id', validators=[])
    income_id = SelectField('IncomeId', validators=[])
    description = StringField(_l('Description'), validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[])
    submit = SubmitField(_l('Submit'))
    
    def __init__(self, *args, **kwargs):
        super(EditPostIncomeForm, self).__init__(*args, **kwargs)
        # disable the fields if you want to
        self.id.render_kw = {'disabled': True}
