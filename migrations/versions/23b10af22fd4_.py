"""empty message

Revision ID: 23b10af22fd4
Revises: 89b255aca090
Create Date: 2021-10-16 12:33:39.074398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23b10af22fd4'
down_revision = '89b255aca090'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seller', sa.Column('storename', sa.String(length=30), nullable=False))
    op.drop_column('seller', 'store_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seller', sa.Column('store_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.drop_column('seller', 'storename')
    # ### end Alembic commands ###