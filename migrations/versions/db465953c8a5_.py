"""empty message

Revision ID: db465953c8a5
Revises: e0f7df8e16fe
Create Date: 2024-12-07 02:27:37.258128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db465953c8a5'
down_revision = 'e0f7df8e16fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favoritos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favoritos')
    # ### end Alembic commands ###
