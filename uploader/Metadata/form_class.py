from random import choices
from wtforms import Form, TextAreaField, DateField, SelectField, StringField, validators, ValidationError

class MetadataForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)])
    division = SelectField('umcu-division', [validators.Length(min=1, max=255)])
    description = TextAreaField('Description', [validators.Length(min=1)])
    author = StringField('author', [validators.Length(min=1)])
    contributor = StringField('contributor')
    deposit_date = DateField('deposit-date', [validators.Length(min=1, max=255)])
    research_end_date = DateField('research-end-date', [validators.Length(min=1, max=255)])
    date_range_start = DateField('date-range-start', [validators.Length(min=1, max=255)])
    date_range_end = DateField('date-range-end', [validators.Length(min=1, max=255)])
    data_type = StringField('data-type', [validators.Length(min=1, max=255)])
    licence = SelectField('licence-type', [validators.Length(min=1, max=255)])
    research_type = StringField('research-type', [validators.Length(min=1, max=255)])
    software = StringField('software')
    language = StringField('language')
    related_publication = StringField('related-publication', [validators.Length(min=1, max=255)])
    keyword = StringField('keyword', [validators.Length(min=1, max=255)])
    package_type = SelectField('package-type', choices=[('Replication','replication'), ('Final', 'final')],)
