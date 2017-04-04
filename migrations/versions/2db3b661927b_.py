"""empty message

Revision ID: 2db3b661927b
Revises: 62eafb70058e
Create Date: 2017-03-24 10:48:03.376934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2db3b661927b'
down_revision = '62eafb70058e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('editable', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('address', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('phone', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone')
    op.drop_column('user', 'address')
    op.drop_column('comment', 'editable')
    # ### end Alembic commands ###
