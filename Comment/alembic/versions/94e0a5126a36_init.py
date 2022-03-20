"""init

Revision ID: 94e0a5126a36
Revises: 
Create Date: 2022-03-18 23:25:38.685788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94e0a5126a36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('commentId', sa.Integer, primary_key=True),
        sa.Column('postId', sa.Integer, unique=True, nullable=False),
        sa.Column('userId', sa.Integer, unique=True, nullable=False),
        sa.Column('userName', sa.String(60)),
        sa.Column('commentText', sa.String(1000)),
        sa.Column('commentDateTime', sa.String(100)),
    )


def downgrade():
    op.drop_table('comments')
