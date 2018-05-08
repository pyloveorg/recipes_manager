from wtforms import Form, StringField, IntegerField, PasswordField, RadioField, validators, TextAreaField

class RegistrationForm(Form):
    email = StringField('Email Address', [
        validators.Email(message="Email is not valid"),
        validators.InputRequired(message="Cannot be empty")])
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
    # False has to be an empty string, because in Python a string is always true.
    status = RadioField('Status', choices=[('Public', 'Public'), ('Private', 'Private')], default='Public')

class SearchForm(Form):
    search = StringField('Search', [validators.InputRequired(message="Cannot be empty")])

class VoteForm(Form):
    value = RadioField(
        'Vote',
        [
            validators.InputRequired(message="Cannot be empty"),
            validators.AnyOf(["1","2","3","4","5"])
        ],
        choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]
    )