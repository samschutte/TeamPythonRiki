"""
    Forms
    ~~~~~
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import FileField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError
from wtforms.validators import regexp

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users


class URLForm(FlaskForm):
    url = StringField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)


class SearchForm(FlaskForm):
    term = StringField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(FlaskForm):
    title = StringField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = StringField('')
    file = FileField(u'Upload File')
    referenceTitle = StringField(u'Add a Reference:')
    referenceAuthor = StringField('')
    referenceDate = StringField('')
    referenceLink = StringField('')
    referenceISBN = StringField('')


class LoginForm(FlaskForm):
    name = StringField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')

class SignupForm(FlaskForm):
    name = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    confirm_password = PasswordField('Confirm Password', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if user:
            raise ValidationError('This username already exists')
    
    def validate_confirm_password(form, field):
        if form.password.data != form.confirm_password.data:
            raise ValidationError('Password must match')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#A - new form for search_by_tags. Not super clean.
#forms of varried length can be generated with setattr()
def create_TagsForm(tag_list):
    
    class TagsForm(FlaskForm):
        def get_selected_tags(self):
            selected_tags = [field.name for field in self if isinstance(field, BooleanField) and field.data]
            return selected_tags
    
    for tag in tag_list:
        setattr(TagsForm, tag[0], BooleanField(f"{tag[0]} ({tag[1]})"))

    return TagsForm()