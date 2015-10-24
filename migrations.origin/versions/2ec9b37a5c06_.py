"""empty message

Revision ID: 2ec9b37a5c06
Revises: 1d97cb5f4d6b
Create Date: 2015-08-24 16:24:27.588911

"""

# revision identifiers, used by Alembic.
revision = '2ec9b37a5c06'
down_revision = '1d97cb5f4d6b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ns_comments',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('author_id', sa.BigInteger(), nullable=True),
    sa.Column('post_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['ns_users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['ns_posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ns_comments_timestamp', 'ns_comments', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_ns_comments_timestamp', 'ns_comments')
    op.drop_table('ns_comments')
    ### end Alembic commands ###