"""init

Revision ID: d416a56ea4c6
Revises: 
Create Date: 2022-06-14 13:10:18.362396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd416a56ea4c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reacts',
        sa.Column('reactId', sa.Integer, primary_key=True, unique=True),
        sa.Column('postId', sa.Integer, unique=True),
        sa.Column('smileReactCount', sa.Integer),
        sa.Column('loveReactCount', sa.Integer),
        sa.Column('likeReactCount', sa.Integer)
    )


def downgrade():
    op.drop_table('reacts')
