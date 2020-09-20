"""empty message

Revision ID: b5ac73deaafd
Revises: f6d2e47685bd
Create Date: 2020-09-16 11:21:39.981344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5ac73deaafd'
down_revision = 'f6d2e47685bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('City', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('City', sa.Column('name', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###