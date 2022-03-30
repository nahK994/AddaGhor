"""init

Revision ID: b2aae83b13e4
Revises: 
Create Date: 2022-03-13 16:18:35.958862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2aae83b13e4'
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
        'users',
        sa.Column('userId', sa.Integer, primary_key=True),
        sa.Column('userName', sa.String(50)),
        sa.Column('email', sa.String(50), unique=True, nullable=False),
        sa.Column('bio', sa.String(200)),
        sa.Column('occupation', sa.String(100)),
        sa.Column('password', sa.String(100)),
        sa.Column('avatar', sa.String(50)),
    )


def downgrade():
    op.drop_table('posts')
    op.drop_table('users')