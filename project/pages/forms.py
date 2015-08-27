from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, FieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length
from project.models import PageBlock


class PageBlockForm(Form):
    block_type = SelectField(
        label='Тип блока',
        choices=[
            (PageBlock.TYPE.img_left.value, 'Блок с картинкой слева'),
            (PageBlock.TYPE.img_right.value, 'Блок с картинкой справа'),
            (PageBlock.TYPE.no_img.value, 'Блок без картинки'),
        ],
        coerce=lambda x: PageBlock.TYPE(int(x)),
        default=PageBlock.TYPE.img_left,
    )
    title = StringField(
        label='Заголовок',
        validators=[
            Length(
                max=128,
                message='Не должен превышать 128 символов',
            ),
        ],
    )
    short_description = TextAreaField(
        label='Короткое описание '
              '(используется для отображения в списке в админке)',
        validators=[
            Length(
                max=256,
                message='Не должен превышать 256 символов',
            ),
        ],
    )
    text = TextAreaField(
        label='Текст',
    )
    image = StringField(
        label='Картинка (на данный момент URL)',
    )


class PageForm(Form):
    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        pageblocks = PageBlock.query.all()
        for block in self.blocks:
            block.query = pageblocks

    title = StringField(
        label='Заголовок',
        validators=[
            Length(
                max=128,
                message='Не должен превышать 128 символов',
            ),
        ],
    )
    blocks = FieldList(
        QuerySelectField(),
        min_entries=1,
    )
