"""empty message

Revision ID: 5af0eade0b7a
Revises: a0a3712e3a3b
Create Date: 2020-09-16 08:27:51.947987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5af0eade0b7a'
down_revision = 'a0a3712e3a3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('city_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Artist', 'City', ['city_id'], ['id'])
    op.drop_column('Artist', 'city')
    op.drop_column('Artist', 'state')
    op.alter_column('Venue', 'city_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'city_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('Artist', sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Artist', type_='foreignkey')
    op.drop_column('Artist', 'city_id')
    # ### end Alembic commands ###