"""Added users table

Revision ID: 4503a2e36a01
Revises: 
Create Date: 2015-06-01 15:30:52.565284

"""

# revision identifiers, used by Alembic.
revision = '4503a2e36a01'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('encrypted_password', sa.String(length=255), nullable=False),
    sa.Column('reset_password_token', sa.String(length=255), nullable=True),
    sa.Column('reset_password_sent_at', sa.DateTime(), nullable=True),
    sa.Column('remember_created_at', sa.DateTime(), nullable=True),
    sa.Column('sign_in_count', sa.Integer(), nullable=False),
    sa.Column('current_sign_in_at', sa.DateTime(), nullable=True),
    sa.Column('last_sign_in_at', sa.DateTime(), nullable=True),
    sa.Column('current_sign_in_ip', sa.String(length=255), nullable=True),
    sa.Column('last_sign_in_ip', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('locale', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('reset_password_token')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###
