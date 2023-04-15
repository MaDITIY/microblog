"""Add posts table and user-posts relation.

Revision ID: 647e710a5a34
Revises: 82886aecfdfe
Create Date: 2023-04-15 17:23:16.737595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '647e710a5a34'
down_revision = '82886aecfdfe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('body', sa.String(length=140), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_posts_timestamp'), ['timestamp'], unique=False)


def downgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_posts_timestamp'))

    op.drop_table('posts')
