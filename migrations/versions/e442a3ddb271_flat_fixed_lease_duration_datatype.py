"""FLAT: fixed lease_duration datatype

Revision ID: e442a3ddb271
Revises: 71d75faba4d4
Create Date: 2023-08-24 11:15:19.963641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e442a3ddb271'
down_revision = '71d75faba4d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flats', schema=None) as batch_op:
        batch_op.alter_column('lease_duration',
               existing_type=sa.DATE(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flats', schema=None) as batch_op:
        batch_op.alter_column('lease_duration',
               existing_type=sa.Integer(),
               type_=sa.DATE(),
               existing_nullable=True)

    # ### end Alembic commands ###
