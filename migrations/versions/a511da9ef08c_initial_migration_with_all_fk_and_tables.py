"""Initial Migration with All FK and Tables

Revision ID: a511da9ef08c
Revises: None
Create Date: 2016-06-16 09:43:28.608550

"""

# revision identifiers, used by Alembic.
revision = 'a511da9ef08c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('division', sa.String(length=100), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('vendor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('fax', sa.String(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('tax_id', sa.String(length=100), nullable=True),
    sa.Column('mwbe', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_submitted', sa.DateTime(), nullable=True),
    sa.Column('date_closed', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('item', sa.String(length=100), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('unit_price', sa.Numeric(), nullable=True),
    sa.Column('total_cost', sa.Numeric(), nullable=True),
    sa.Column('funding_source', sa.String(length=100), nullable=True),
    sa.Column('funding_source_description', sa.String(length=100), nullable=True),
    sa.Column('justification', sa.String(length=255), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('filepath', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('request')
    op.drop_table('vendor')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    ### end Alembic commands ###