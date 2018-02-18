from wtforms import Form, StringField, PasswordField, validators

class RegistrationForm(Form):
    email = StringField('Email Address', [validators.Email, validators.input_required])
    password = PasswordField('Password', [
        validators.Length(min=8, message='Password too short'),
        validators.input_required,
        validators.equal_to('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm password', [validators.input_required])

class LoginForm(Form):
    email = StringField('Email Address', [validators.Email, validators.input_required])
    password = PasswordField('Password', [validators.input_required])