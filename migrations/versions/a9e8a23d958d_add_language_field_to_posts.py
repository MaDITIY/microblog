"""Add language field to posts.

Revision ID: a9e8a23d958d
Revises: 107032409faf
Create Date: 2023-04-30 14:46:44.546166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9e8a23d958d'
down_revision = '107032409faf'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('language', sa.String(length=10), nullable=True))


def downgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('language')
