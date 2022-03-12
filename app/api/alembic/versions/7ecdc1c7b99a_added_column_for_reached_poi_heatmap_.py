"""Added column for reached_poi_heatmap_computed

Revision ID: 7ecdc1c7b99a
Revises: 3a4b84ae169b
Create Date: 2022-03-11 12:45:08.686484

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
import sqlmodel  



# revision identifiers, used by Alembic.
revision = '7ecdc1c7b99a'
down_revision = '3a4b84ae169b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data_upload', sa.Column('reached_poi_heatmap_computed', sa.Boolean(), nullable=True), schema='customer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data_upload', 'reached_poi_heatmap_computed', schema='customer')
    # ### end Alembic commands ###
