"""empty message

Revision ID: 17202d48ca39
Revises: 
Create Date: 2022-06-09 18:23:17.097962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17202d48ca39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prediction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('test_number', sa.Integer(), nullable=False),
    sa.Column('result', sa.String(length=150), nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prediction')
    # ### end Alembic commands ###