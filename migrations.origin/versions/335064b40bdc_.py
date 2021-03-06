"""empty message

Revision ID: 335064b40bdc
Revises: None
Create Date: 2015-08-21 13:47:12.330663

"""

# revision identifiers, used by Alembic.
revision = '335064b40bdc'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ns_room_books')
    op.drop_table('ns_books')
    op.drop_table('ns_rooms')
    op.add_column('ns_users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ns_users', 'password_hash')
    op.create_table('ns_rooms',
    sa.Column('id', mysql.BIGINT(display_width=20), nullable=False),
    sa.Column('number', mysql.VARCHAR(length=5), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.create_table('ns_books',
    sa.Column('id', mysql.BIGINT(display_width=20), nullable=False),
    sa.Column('room_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('checkin_on', sa.DATE(), nullable=True),
    sa.Column('checkout_on', sa.DATE(), nullable=True),
    sa.Column('user_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], [u'ns_users.id'], name=u'ns_books_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.create_table('ns_room_books',
    sa.Column('room_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('book_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['book_id'], [u'ns_books.id'], name=u'ns_room_books_ibfk_2'),
    sa.ForeignKeyConstraint(['room_id'], [u'ns_rooms.id'], name=u'ns_room_books_ibfk_1'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
