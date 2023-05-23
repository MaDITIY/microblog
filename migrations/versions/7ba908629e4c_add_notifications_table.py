"""Add notifications table.

Revision ID: 7ba908629e4c
Revises: 5f05c0fb48c4
Create Date: 2023-05-23 20:46:32.640871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ba908629e4c'
down_revision = '5f05c0fb48c4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.Float(), nullable=True),
        sa.Column('payload_json', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_notifications_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_notifications_timestamp'), ['timestamp'], unique=False)


def downgrade():
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_notifications_timestamp'))
        batch_op.drop_index(batch_op.f('ix_notifications_name'))

    op.drop_table('notifications')
