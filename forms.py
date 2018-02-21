from wtforms import Form, StringField, IntegerField, PasswordField, RadioField, validators, TextAreaField

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

class RecipeForm(Form):
    title = StringField('Title', [validators.InputRequired(message="Cannot be empty")])
    time_needed = IntegerField('Time needed (min)', [validators.InputRequired(message="Cannot be empty")])
    ingredients = TextAreaField('Ingredients', [validators.InputRequired(message="Cannot be empty")])
    steps = TextAreaField('Steps', [validators.InputRequired(message="Cannot be empty")])
    is_public = RadioField('Status', choices=[(True, 'Public'), ('', 'Private')], default=True)
