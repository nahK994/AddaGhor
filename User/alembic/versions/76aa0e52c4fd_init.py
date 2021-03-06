"""init

Revision ID: 76aa0e52c4fd
Revises: 
Create Date: 2022-06-06 09:46:59.886776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76aa0e52c4fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
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
    op.drop_table('users')
