"""empty message

Revision ID: 97fba2b76c44
Revises: 
Create Date: 2019-08-08 16:04:18.078921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97fba2b76c44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('measurements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('measurements')
    # ### end Alembic commands ###
