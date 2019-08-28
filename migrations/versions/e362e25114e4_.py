"""empty message

Revision ID: e362e25114e4
Revises: a958a3db84db
Create Date: 2019-08-28 10:29:23.519271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e362e25114e4'
down_revision = 'a958a3db84db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('education',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('college_name', sa.String(length=100), nullable=True),
    sa.Column('course', sa.String(length=100), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.Column('seekerId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['seekerId'], ['jobseeker.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('education')
    # ### end Alembic commands ###
