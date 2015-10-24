"""empty message

Revision ID: 2e5706473890
Revises: 335064b40bdc
Create Date: 2015-08-22 18:37:38.917782

"""

# revision identifiers, used by Alembic.
revision = '2e5706473890'
down_revision = '335064b40bdc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ns_roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('ns_roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index('ix_ns_roles_default', 'ns_roles', ['default'], unique=False)
    op.add_column('ns_users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ns_users', 'confirmed')
    op.drop_index('ix_ns_roles_default', 'ns_roles')
    op.drop_column('ns_roles', 'permissions')
    op.drop_column('ns_roles', 'default')
    ### end Alembic commands ###
