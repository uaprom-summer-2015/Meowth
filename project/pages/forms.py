from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import Length
from project.models import PageBlock


class PageBlockForm(Form):
    title = StringField(
        label='Title',
        validators=[
            Length(
                max=128,
                message='Must not exceed 128 symbols',
            ),
        ],
    )
    short_description = TextAreaField(
        label='Short description',
        validators=[
            Length(
                max=256,
                message='Must not exceed 256 symbols',
            ),
        ],
    )
    text = TextAreaField(
        label='Text',
        validators=[
            Length(
                max=1024,
                message='Must not exceed 1024 symbols',
            ),
        ],
    )
    image = StringField(
        label='Image (url for now)',
    )


class PageForm(Form):
    title = StringField(
        label='Title',
        validators=[
            Length(
                max=128,
                message='Must not exceed 128 symbols',
            ),
        ],
    )
    url = StringField(
        label='Url',
    )
    blocks = QuerySelectMultipleField(
        label='Blocks',
        query_factory=(
            lambda: PageBlock.query.filter(
                PageBlock.page_id == None
            ).all()
        )
    )
