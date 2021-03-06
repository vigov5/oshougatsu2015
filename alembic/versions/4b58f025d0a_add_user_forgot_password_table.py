"""Add user forgot password table

Revision ID: 4b58f025d0a
Revises: 26ba94b8e796
Create Date: 2015-07-16 13:16:13.164040

"""

# revision identifiers, used by Alembic.
revision = '4b58f025d0a'
down_revision = '26ba94b8e796'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_forgot_passwords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=40), nullable=True),
    sa.Column('expire_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_forgot_passwords')
    ### end Alembic commands ###
