"""add content column to posts table

Revision ID: 424b4b6efe7c
Revises: 4018f35e4c21
Create Date: 2022-04-05 18:58:06.011375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '424b4b6efe7c'
down_revision = '4018f35e4c21'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_column('posts', 'content')
    pass
