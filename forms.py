from wtforms import Form, StringField, PasswordField, validators

class RegistrationForm(Form):
    email = StringField('Email Address', [validators.Email(message="Email is not valid"), validators.InputRequired(message="Cannot be empty")])
    password = PasswordField('Password', [
        validators.Length(min=8, message='Password too short'),
        validators.InputRequired(message="Cannot be empty"),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm password')

class LoginForm(Form):
    email = StringField('Email Address', [validators.InputRequired(message="Cannot be empty")])
    password = PasswordField('Password', [validators.InputRequired(message="Cannot be empty")])
