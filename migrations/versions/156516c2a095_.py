"""empty message

Revision ID: 156516c2a095
Revises: 7f2986704bcf
Create Date: 2021-10-21 20:13:32.013469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '156516c2a095'
down_revision = '7f2986704bcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hola')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hola',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('hola', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='hola_pkey')
    )
    # ### end Alembic commands ###
