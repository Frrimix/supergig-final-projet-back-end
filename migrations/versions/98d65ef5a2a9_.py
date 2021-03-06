"""empty message

Revision ID: 98d65ef5a2a9
Revises: 09c64b7db56e
Create Date: 2020-09-25 00:26:12.256960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98d65ef5a2a9'
down_revision = '09c64b7db56e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone', sa.String(length=120), nullable=False))
    op.create_unique_constraint(None, 'user', ['phone'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'phone')
    # ### end Alembic commands ###
