"""empty message

Revision ID: 9b8652632f5b
Revises: 
Create Date: 2021-11-11 20:41:06.339434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b8652632f5b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buyer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=50), nullable=False),
    sa.Column('lastname', sa.String(length=50), nullable=False),
    sa.Column('rut', sa.String(length=12), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'favorite', 'buyer', ['buyerID'], ['id'])
    op.create_foreign_key(None, 'payment', 'buyer', ['buyerID'], ['id'])
    op.create_foreign_key(None, 'sale', 'buyer', ['buyerID'], ['id'])
    op.create_foreign_key(None, 'wishlist', 'buyer', ['buyerID'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wishlist', type_='foreignkey')
    op.drop_constraint(None, 'sale', type_='foreignkey')
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.drop_constraint(None, 'favorite', type_='foreignkey')
    op.drop_table('buyer')
    # ### end Alembic commands ###
