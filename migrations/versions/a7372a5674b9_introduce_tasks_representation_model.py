"""Introduce tasks representation model.

Revision ID: a7372a5674b9
Revises: 7ba908629e4c
Create Date: 2023-06-02 16:43:30.425937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7372a5674b9'
down_revision = '7ba908629e4c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=True),
        sa.Column('description', sa.String(length=128), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('complete', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tasks_name'), ['name'], unique=False)


def downgrade():
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tasks_name'))

    op.drop_table('tasks')
