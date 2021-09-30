"""added order tables that tracks down user order.

Revision ID: 0e343c394634
Revises: 7f6f1c32aec7
Create Date: 2021-09-30 10:31:33.566012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e343c394634'
down_revision = '7f6f1c32aec7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('orderid', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('total_price', sa.DECIMAL(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('orderid', 'userid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    # ### end Alembic commands ###
