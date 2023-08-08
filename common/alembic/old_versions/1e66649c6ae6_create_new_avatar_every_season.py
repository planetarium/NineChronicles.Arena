"""Create new avatar every season

Revision ID: 1e66649c6ae6
Revises: b4abe38403e5
Create Date: 2023-07-28 11:35:06.274443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e66649c6ae6'
down_revision = 'b4abe38403e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_avatar_addr', table_name='avatar')
    op.drop_constraint('arena_info_avatar_addr_fkey', 'arena_info', type_='foreignkey')
    op.drop_table('avatar')
    op.add_column('arena_info', sa.Column('agent_addr', sa.Text(), nullable=True))
    op.add_column('arena_info', sa.Column('level', sa.Integer(), nullable=False))
    op.add_column('arena_info', sa.Column('costume_armor_id', sa.Integer(), nullable=False))
    op.add_column('arena_info', sa.Column('title_id', sa.Integer(), nullable=True))
    op.create_index('avatar_arena_id_idx', 'arena_info', ['avatar_addr', 'arena_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('avatar_arena_id_idx', table_name='arena_info')
    op.drop_column('arena_info', 'title_id')
    op.drop_column('arena_info', 'costume_armor_id')
    op.drop_column('arena_info', 'level')
    op.drop_column('arena_info', 'agent_addr')
    op.create_table('avatar',
    sa.Column('addr', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('agent_addr', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('level', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('costume_armor_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('addr', name='avatar_pkey')
    )
    op.create_foreign_key('arena_info_avatar_addr_fkey', 'arena_info', 'avatar', ['avatar_addr'], ['addr'])
    op.create_index('ix_avatar_addr', 'avatar', ['addr'], unique=False)
    # ### end Alembic commands ###