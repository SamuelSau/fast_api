"""create post table

Revision ID: 4018f35e4c21
Revises: 
Create Date: 2022-04-05 18:46:34.961118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4018f35e4c21'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id', sa.INTEGER(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_table('posts')
    pass
