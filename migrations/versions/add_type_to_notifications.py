"""add type column to notifications

Revision ID: add_type_to_notifications
Revises: 6fd6e1e9ed9d
Create Date: 2024-01-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_type_to_notifications'
down_revision = '6fd6e1e9ed9d'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('notifications', 
        sa.Column('type', sa.String(20), nullable=False, server_default='internal')
    )

def downgrade():
    op.drop_column('notifications', 'type')
