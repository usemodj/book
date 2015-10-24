"""empty message

Revision ID: 2c27b48ead1b
Revises: 4f0a4c7707dd
Create Date: 2015-08-23 11:03:09.849904

"""

# revision identifiers, used by Alembic.
revision = '2c27b48ead1b'
down_revision = '4f0a4c7707dd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ns_posts',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['ns_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ns_posts_timestamp', 'ns_posts', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_ns_posts_timestamp', 'ns_posts')
    op.drop_table('ns_posts')
    ### end Alembic commands ###
