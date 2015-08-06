"""del field slug, add field mail(IntEnum)

Revision ID: 46f4932e624
Revises: 49dee429367
Create Date: 2015-08-05 18:13:09.287819

"""

# revision identifiers, used by Alembic.
revision = '46f4932e624'
down_revision = '49dee429367'

from alembic import op
import sqlalchemy as sa
from project.lib.orm.types import TypeEnum
from project.models import MailTemplate


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mailtemplates', sa.Column('mail', TypeEnum(MailTemplate.MAIL), nullable=False,
                                             server_default=sa.DefaultClause("0")))
    op.drop_column('mailtemplates', 'slug')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mailtemplates', sa.Column('slug', sa.VARCHAR(), server_default=sa.text("'0'::character varying"), autoincrement=False, nullable=False))
    op.drop_column('mailtemplates', 'mail')
    ### end Alembic commands ###