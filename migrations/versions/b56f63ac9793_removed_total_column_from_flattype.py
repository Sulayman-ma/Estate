"""removed total column from FlatType

Revision ID: b56f63ac9793
Revises: 7bda507b00ed
Create Date: 2023-05-29 20:40:26.329363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b56f63ac9793'
down_revision = '7bda507b00ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flattypes', schema=None) as batch_op:
        batch_op.drop_column('total')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flattypes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
