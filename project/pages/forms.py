from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, FieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length
from project.models import PageBlock


class PageBlockForm(Form):
    block_type = SelectField(
        label='Select layout',
        choices=[
            (PageBlock.TYPE.img_left.value, 'Layout with image left'),
            (PageBlock.TYPE.img_right.value, 'Layout with image right'),
            (PageBlock.TYPE.no_img.value, 'Layout with no image'),
        ],
        coerce=lambda x: PageBlock.TYPE(int(x)),
        default=PageBlock.TYPE.img_left,
    )
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
        label='Short description (used to display pageblock in list)',
        validators=[
            Length(
                max=256,
                message='Must not exceed 256 symbols',
            ),
        ],
    )
    text = TextAreaField(
        label='Text',
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
    blocks = FieldList(
        QuerySelectField(),  # query should be provided in view
        min_entries=1,
    )
