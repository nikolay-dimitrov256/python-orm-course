"""Create Order model

Revision ID: 33be3d1c02dc
Revises: f01b6db02071
Create Date: 2024-07-20 14:36:57.245658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33be3d1c02dc'
down_revision: Union[str, None] = 'f01b6db02071'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_completed', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###