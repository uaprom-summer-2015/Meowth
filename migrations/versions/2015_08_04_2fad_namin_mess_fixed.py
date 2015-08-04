"""naming mess removed


Revision ID: 2fadbf7a01a
Revises: 5984f22b0a6
Create Date: 2015-08-04 13:41:23.764054

"""

# revision identifiers, used by Alembic.
revision = '2fadbf7a01a'
down_revision = '5984f22b0a6'

from alembic import op


def upgrade():
    op.rename_table('block_page_association', 'block_page_associations')
    op.rename_table('category', 'categories')
    op.rename_table('city', 'cities')
    op.rename_table('vacancy', 'vacancies')


def downgrade():
    op.rename_table('block_page_associations', 'block_page_association')
    op.rename_table('categories', 'category')
    op.rename_table('cities', 'city')
    op.rename_table('vacancies', 'vacancy')
