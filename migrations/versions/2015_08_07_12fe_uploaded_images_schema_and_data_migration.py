"""uploaded_images scema and data migraion

Revision ID: 12fe8d110f7
Revises: 20b9c5b88f9
Create Date: 2015-08-07 14:12:11.893524

"""

# revision identifiers, used by Alembic.
revision = '12fe8d110f7'
down_revision = '20b9c5b88f9'

from alembic import op
import sqlalchemy as sa
from project.lib.orm.types import GUID


def upgrade():
    # Start migrating schema
    op.drop_constraint(
        name='uploaded_images_pkey',
        table_name='uploaded_images',
        type_='primary',
    )
    op.alter_column(
        'uploaded_images',
        'uid',
        nullable=True,
    )
    op.add_column(
        'uploaded_images',
        sa.Column('id', sa.Integer, primary_key=True)
    )
    op.add_column(
        'uploaded_images',
        sa.Column('ext', sa.VARCHAR(), nullable=True)
    )
    op.add_column(
        'uploaded_images',
        sa.Column('name', GUID(), nullable=True)
    )
    op.create_primary_key(
        name='uploaded_images_pkey',
        table_name='uploaded_images',
        cols=['id']
    )
    op.create_unique_constraint(
        name='uploaded_images_name_ext_img_category_key',
        source='uploaded_images',
        local_cols=['name', 'ext', 'img_category'],
    )
    # Migrate data:
    op.execute(
        'update uploaded_images set (ext, name) = '
        '(split_part(uid, \'.\', 2), split_part(uid, \'.\', 1)::uuid);'
    )
    # Set notnull and drop unnecessary columns:
    op.alter_column(
        'uploaded_images',
        'ext',
        nullable=False,
    )
    op.alter_column(
        'uploaded_images',
        'name',
        nullable=False,
    )
    op.drop_column('uploaded_images', 'uid')


def downgrade():
    # Drop not null restrictions
    op.add_column(
        'uploaded_images',
        sa.Column(
            'uid',
            sa.VARCHAR(length=40),
            nullable=True,
        )
    )
    op.alter_column(
        'uploaded_images',
        'name',
        nullable=True,
    )
    op.alter_column(
        'uploaded_images',
        'ext',
        nullable=True
    )
    # Restore data:
    op.execute(
        'update uploaded_images set (uid, ext, name) = '
        '(replace(format(\'%s.%s\', name, ext), \'-\', \'\'), NULL, NULL);'
    )
    # Finish schema restore
    op.drop_constraint(
        name='uploaded_images_pkey',
        table_name='uploaded_images',
        type_='primary',
    )
    op.drop_constraint(
        name='uploaded_images_name_ext_img_category_key',
        table_name='uploaded_images',
        type_='unique',
    )
    op.alter_column(
        'uploaded_images',
        'uid',
        nullable=False,
    )
    op.create_primary_key(
        'uploaded_images_pkey',
        'uploaded_images',
        ['uid', 'img_category', ],
    )
    op.drop_column('uploaded_images', 'id')
    op.drop_column('uploaded_images', 'name')
    op.drop_column('uploaded_images', 'ext')
