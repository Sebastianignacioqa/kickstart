"""empty message

Revision ID: 9838c654520f
Revises: 
Create Date: 2021-12-01 20:07:52.092719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9838c654520f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sellerID', sa.Integer(), nullable=False),
    sa.Column('item_title', sa.String(length=50), nullable=False),
    sa.Column('item_description', sa.String(length=250), nullable=False),
    sa.Column('item_stock', sa.Integer(), nullable=False),
    sa.Column('item_price', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('imageID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['imageID'], ['images.id'], ),
    sa.ForeignKeyConstraint(['sellerID'], ['seller.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('images', 'productid')
    op.create_foreign_key(None, 'sale', 'product', ['productID'], ['id'])
    op.create_foreign_key(None, 'wishlist', 'product', ['productID'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wishlist', type_='foreignkey')
    op.drop_constraint(None, 'sale', type_='foreignkey')
    op.add_column('images', sa.Column('productid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_table('product')
    # ### end Alembic commands ###
