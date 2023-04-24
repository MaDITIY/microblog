"""Add many to many followers-followed relationship.

Revision ID: 107032409faf
Revises: 5daedabfd8c7
Create Date: 2023-04-24 20:57:48.854657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '107032409faf'
down_revision = '5daedabfd8c7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'followers',
        sa.Column('follower_id', sa.Integer(), nullable=True),
        sa.Column('followed_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['follower_id'], ['users.id'], )
    )


def downgrade():
    op.drop_table('followers')
