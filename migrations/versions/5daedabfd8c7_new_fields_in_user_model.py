"""New fields in user model.

Revision ID: 5daedabfd8c7
Revises: 647e710a5a34
Create Date: 2023-04-23 16:14:34.778622
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5daedabfd8c7'
down_revision = '647e710a5a34'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_me', sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('about_me')
