"""mwbe is now boolean with a defualt value of False

Revision ID: 626d6071278c
Revises: 54bdffeafe4f
Create Date: 2016-06-13 15:13:25.278042

"""

# revision identifiers, used by Alembic.
revision = '626d6071278c'
down_revision = '54bdffeafe4f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vendor', 'mwbe',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vendor', 'mwbe',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    ### end Alembic commands ###