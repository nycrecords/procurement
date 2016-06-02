"""empty message

Revision ID: bc0ea960bc66
Revises: caa95af6fa3a
Create Date: 2016-06-02 13:03:43.984380

"""

# revision identifiers, used by Alembic.
revision = 'bc0ea960bc66'
down_revision = 'caa95af6fa3a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('division', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request', 'division')
    ### end Alembic commands ###
