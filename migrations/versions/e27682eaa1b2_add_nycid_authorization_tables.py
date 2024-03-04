"""add nycid authorization tables

Revision ID: e27682eaa1b2
Revises: f0bf9ad93a6d
Create Date: 2024-02-06 14:21:41.213890

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import false
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e27682eaa1b2'
down_revision = 'f0bf9ad93a6d'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('user', 'users')
    op.rename_table('request', 'requests')
    op.rename_table('vendor', 'vendors')
    op.rename_table('comment', 'comments')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('guid', sa.String(length=32), nullable=True))
        batch_op.create_unique_constraint('uq_user_guid', ['guid'])
        batch_op.add_column(sa.Column('middle_initial', sa.String(length=1), nullable=True))
        batch_op.add_column(sa.Column('email_validated', sa.Boolean(), nullable=False, server_default=false()))
        batch_op.add_column(sa.Column('last_sign_in_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('session_id', sa.String(length=254), nullable=True))
        batch_op.drop_column('password_hash')
        batch_op.alter_column('login', new_column_name='is_active')

    op.create_table('auth_events',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_guid', sa.String(length=64), nullable=True),
                    sa.Column('type', sa.Enum('user_created', 'user_logged_in', 'user_failed_login', 'user_logged_out',
                                              'user_role_changed', 'user_enabled', 'user_disabled',
                                              name='auth_event_type'), nullable=False),
                    sa.Column('previous_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('new_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('timestamp', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['user_guid'], ['users.guid'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('auth_events')

    # Drop the enum type using raw SQL
    op.execute('DROP TYPE IF EXISTS auth_event_type')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_guid', type_='unique')
        batch_op.add_column(sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
        batch_op.drop_column('guid')
        batch_op.drop_column('email_validated')
        batch_op.drop_column('last_sign_in_at')
        batch_op.drop_column('session_id')
        batch_op.drop_column('middle_initial')
        batch_op.alter_column('is_active', new_column_name='login')

    op.rename_table('users', 'user')
    op.rename_table('requests', 'request')
    op.rename_table('vendors', 'vendor')
    op.rename_table('comments', 'comment')

