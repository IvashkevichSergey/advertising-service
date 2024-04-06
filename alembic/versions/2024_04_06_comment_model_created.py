"""comment model created

Revision ID: d0632c8c1122
Revises: b4dd97162dba
Create Date: 2024-04-06 20:29:19.402457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0632c8c1122'
down_revision: Union[str, None] = 'b4dd97162dba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('body', sa.String(length=500), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('adv_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['adv_id'], ['advertisement.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
