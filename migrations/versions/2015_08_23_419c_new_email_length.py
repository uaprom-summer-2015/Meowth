"""new_email_length

Revision ID: 419ca5bbd2f
Revises: 18d21075187
Create Date: 2015-08-23 22:44:58.513242

"""

# revision identifiers, used by Alembic.
revision = '419ca5bbd2f'
down_revision = '18d21075187'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=320),
               existing_nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email',
               existing_type=sa.String(length=320),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
    ### end Alembic commands ###
