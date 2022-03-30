"""init

Revision ID: 7a0d68a50035
Revises: 
Create Date: 2022-03-19 00:08:30.512844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a0d68a50035'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('postId', sa.Integer, primary_key=True),
        sa.Column('userId', sa.Integer, nullable=False),
        sa.Column('postText', sa.String(1000)),
        sa.Column('postDateTime', sa.String(100))
    )

    op.create_table(
        'reacts',
        sa.Column('reactId', sa.Integer, primary_key=True, unique=True),
        sa.Column('postId', sa.Integer, unique=True),
        sa.Column('smileReactCount', sa.Integer),
        sa.Column('loveReactCount', sa.Integer),
        sa.Column('likeReactCount', sa.Integer)
    )

    op.create_table(
        'comments',
        sa.Column('postId', sa.Integer, nullable=False),
        sa.Column('userId', sa.Integer, nullable=False),
        sa.Column('commentId', sa.Integer, primary_key=True),
        sa.Column('commentText', sa.String(1000)),
        sa.Column('commentDateTime', sa.String(100)),
    )

    op.create_table(
        'users',
        sa.Column('userId', sa.Integer, primary_key=True),
        sa.Column('userName', sa.String(50)),
        sa.Column('email', sa.String(50), unique=True, nullable=False),
        sa.Column('bio', sa.String(200)),
        sa.Column('occupation', sa.String(100)),
        sa.Column('password', sa.String(100))
    )


def downgrade():
    op.drop_table('posts')
    op.drop_table('reacts')
    op.drop_table('comments')
    op.drop_table('users')
