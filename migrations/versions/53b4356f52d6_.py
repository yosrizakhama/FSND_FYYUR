"""empty message

Revision ID: 53b4356f52d6
Revises: 9363f75a0d12
Create Date: 2020-09-17 21:08:26.444331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53b4356f52d6'
down_revision = '9363f75a0d12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('datecreate', sa.DateTime(), nullable=True))
    op.add_column('Venue', sa.Column('datecreate', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'datecreate')
    op.drop_column('Artist', 'datecreate')
    # ### end Alembic commands ###
