"""auto_migration_20260127_184731

Revision ID: c6fa46cde1da
Revises: 3b8199a7d413
Create Date: 2026-01-27 18:47:31.410083

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c6fa46cde1da'
down_revision = '3b8199a7d413'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create users and products tables with audit fields (created_at, updated_at).
    This migration creates the initial schema for the application.
    """
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('role', postgresql.ENUM('USER', 'ADMIN', 'MODERATOR', name='userrole'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])
    op.create_index('ix_users_updated_at', 'users', ['updated_at'])
    
    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_products_name', 'products', ['name'])
    op.create_index('ix_products_category', 'products', ['category'])
    op.create_index('ix_products_id', 'products', ['id'])
    op.create_index('ix_products_created_at', 'products', ['created_at'])
    op.create_index('ix_products_updated_at', 'products', ['updated_at'])


def downgrade() -> None:
    """
    Drop products and users tables.
    """
    op.drop_index('ix_products_updated_at', table_name='products')
    op.drop_index('ix_products_created_at', table_name='products')
    op.drop_index('ix_products_id', table_name='products')
    op.drop_index('ix_products_category', table_name='products')
    op.drop_index('ix_products_name', table_name='products')
    op.drop_table('products')
    op.drop_index('ix_users_updated_at', table_name='users')
    op.drop_index('ix_users_created_at', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    # Drop enum type
    op.execute('DROP TYPE IF EXISTS userrole')
