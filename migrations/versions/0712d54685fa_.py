"""empty message

Revision ID: 0712d54685fa
Revises: 
Create Date: 2019-08-16 16:47:04.082268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0712d54685fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('since', sa.String(length=64), nullable=True),
    sa.Column('teamSize', sa.String(length=64), nullable=True),
    sa.Column('domain', sa.String(length=64), nullable=True),
    sa.Column('desc', sa.String(length=3024), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('website', sa.String(length=256), nullable=True),
    sa.Column('address', sa.String(length=512), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('logo_url', sa.String(), nullable=True),
    sa.Column('logo_img_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employer_email'), 'employer', ['email'], unique=True)
    op.create_index(op.f('ix_employer_name'), 'employer', ['name'], unique=True)
    op.create_index(op.f('ix_employer_password_hash'), 'employer', ['password_hash'], unique=False)
    op.create_table('job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('jobdesc', sa.String(length=10000), nullable=True),
    sa.Column('exp', sa.String(length=128), nullable=True),
    sa.Column('qualification', sa.String(length=128), nullable=True),
    sa.Column('career_level', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.Column('fulltime', sa.Boolean(), nullable=True),
    sa.Column('salary', sa.String(length=100), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('expiry_date', sa.DateTime(), nullable=True),
    sa.Column('openings', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['employer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job')
    op.drop_index(op.f('ix_employer_password_hash'), table_name='employer')
    op.drop_index(op.f('ix_employer_name'), table_name='employer')
    op.drop_index(op.f('ix_employer_email'), table_name='employer')
    op.drop_table('employer')
    # ### end Alembic commands ###
