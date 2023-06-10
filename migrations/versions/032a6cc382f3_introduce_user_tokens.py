"""Introduce user tokens.

Revision ID: 032a6cc382f3
Revises: a7372a5674b9
Create Date: 2023-06-10 15:12:34.519990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '032a6cc382f3'
down_revision = 'a7372a5674b9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('token_expiration', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_token'), ['token'], unique=True)


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_token'))
        batch_op.drop_column('token_expiration')
        batch_op.drop_column('token')
