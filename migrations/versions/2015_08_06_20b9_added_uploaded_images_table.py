"""added uploaded_images table

Revision ID: 20b9c5b88f9
Revises: 46f4932e624
Create Date: 2015-08-06 15:35:09.129482

"""

# revision identifiers, used by Alembic.
revision = '20b9c5b88f9'
down_revision = '46f4932e624'

from alembic import op
import sqlalchemy as sa
from project.lib.orm.types import TypeEnum
from project.models import UploadedImage


def upgrade():
    # commands auto generated by Alembic - please adjust!
    op.create_table(
        'uploaded_images',
        sa.Column('uid', sa.VARCHAR(length=40), nullable=False),
        sa.Column(
            'img_category',
            TypeEnum(UploadedImage.IMG_CATEGORY),
            nullable=False
        ),
        sa.Column('title', sa.VARCHAR(length=32), nullable=True),
        sa.Column('description', sa.VARCHAR(length=128), nullable=True),
        sa.PrimaryKeyConstraint('uid', 'img_category')
    )
    # end Alembic commands ###


def downgrade():
    # commands auto generated by Alembic - please adjust!
    op.drop_table('uploaded_images')
    # end Alembic commands