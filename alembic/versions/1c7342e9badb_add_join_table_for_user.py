"""Add join table for user

Revision ID: 1c7342e9badb
Revises: 2d73b23556cf
Create Date: 2016-01-13 18:55:01.125420

"""

# revision identifiers, used by Alembic.
revision = '1c7342e9badb'
down_revision = '2d73b23556cf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_join',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('contest_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['contest_id'], ['contests.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_join')
    ### end Alembic commands ###
