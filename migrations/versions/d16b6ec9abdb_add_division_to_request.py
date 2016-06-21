"""Add division to request

Revision ID: d16b6ec9abdb
Revises: 7ca8572a872e
Create Date: 2016-06-21 00:47:07.581050

"""

# revision identifiers, used by Alembic.
revision = 'd16b6ec9abdb'
down_revision = '7ca8572a872e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('division', sa.String(length=100), nullable=True))
    op.drop_column('request', 'name')
    op.add_column('user', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=100), nullable=True))
    op.drop_column('user', 'username')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    op.add_column('request', sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('request', 'division')
    ### end Alembic commands ###