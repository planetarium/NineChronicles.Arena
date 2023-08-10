"""Update models

- ArenaInfo needs `name` to save avatar name
- CostumeStatSheet needs `id` to identify costume-stat. costume_id can be duplicated.

Revision ID: 667ba2407113
Revises: 7dfff4099664
Create Date: 2023-08-03 23:18:56.606831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '667ba2407113'
down_revision = '7dfff4099664'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('arena_info', sa.Column('name', sa.Text(), nullable=False))
    op.add_column('costume_stat_sheet', sa.Column('costume_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('costume_stat_sheet', 'costume_id')
    op.drop_column('arena_info', 'name')
    # ### end Alembic commands ###
