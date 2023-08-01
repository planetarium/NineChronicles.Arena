"""Create avatar related models

Revision ID: 3a2eb22178c2
Revises: 1e66649c6ae6
Create Date: 2023-08-01 17:23:06.901908

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3a2eb22178c2'
down_revision = '1e66649c6ae6'
branch_labels = None
depends_on = None

item_type_enum = postgresql.ENUM('CONSUMABLE', 'COSTUME', 'EQUIPMENT', 'MATERIAL',
                                 name="itemtype", create_type=False)
item_subtype_enum = postgresql.ENUM(
    'FOOD',
    'FULL_COSTUME', 'HAIR_COSTUME', 'EAR_COSTUME', 'EYE_COSTUME', 'TAIL_COSTUME',
    'WEAPON', 'ARMOR', 'BELT', 'NECKLACE', 'RING',
    'EQUIPMENT_MATERIAL', 'FOOD_MATERIAL', 'MONSTER_PART', 'NORMAL_MATERIAL',
    'HOURGLASS', 'AP_STONE',
    'CHEST',  # Obsoleted
    'TITLE',
    name="itemsubtype", create_type=False)
elemental_type_enum = postgresql.ENUM('NORMAL', 'FIRE', 'WATER', 'LAND', 'WIND', name="elementaltype",
                                      create_type=False)

skill_type_enum = postgresql.ENUM("SKILL", "BUFF_SKILL", name="skilltype", create_type=False)

# This is already exist
old_stat_type_list = ('HP', 'ATK', 'DEF', 'CRI', 'HIT', 'SPD', 'DRV', 'DRR', 'CDMG', 'APTN', 'THORN')
new_stat_type_list = sorted(old_stat_type_list + ("NONE",))
old_stat_type_enum = postgresql.ENUM(*old_stat_type_list, name='stattype', create_type=False)
new_stat_type_enum = postgresql.ENUM(*new_stat_type_list, name="stattype", create_type=False)
tmp_stat_type_enum = postgresql.ENUM(*new_stat_type_list, name="_stattype", create_type=False)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    item_type_enum.create(op.get_bind(), checkfirst=False)
    item_subtype_enum.create(op.get_bind(), checkfirst=False)
    elemental_type_enum.create(op.get_bind(), checkfirst=False)
    skill_type_enum.create(op.get_bind(), checkfirst=False)

    tmp_stat_type_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE costume_stat_sheet ALTER COLUMN "type" TYPE _stattype USING type::text::_stattype')
    op.execute('ALTER TABLE equipment_item_sheet ALTER COLUMN "type" TYPE _stattype USING type::text::_stattype')
    old_stat_type_enum.drop(op.get_bind(), checkfirst=False)
    new_stat_type_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE costume_stat_sheet ALTER COLUMN "type" TYPE stattype USING type::text::stattype')
    op.execute('ALTER TABLE equipment_item_sheet ALTER COLUMN "type" TYPE stattype USING type::text::stattype')
    tmp_stat_type_enum.drop(op.get_bind(), checkfirst=False)

    op.create_table(
        'costume',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('arena_info_id', sa.Integer(), nullable=False),
        sa.Column('sheet_id', sa.Integer(), nullable=False),
        sa.Column('item_type', item_type_enum, nullable=True),
        sa.Column('item_subtype', item_subtype_enum, nullable=True),
        sa.Column('equipped', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['arena_info_id'], ['arena_info.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'equipment',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('arena_info_id', sa.Integer(), nullable=False),
        sa.Column('sheet_id', sa.Integer(), nullable=False),
        sa.Column('item_type', item_type_enum, nullable=True),
        sa.Column('item_subtype', item_subtype_enum, nullable=True),
        sa.Column('elemental_type', elemental_type_enum, nullable=True),
        sa.Column('level', sa.Integer(), nullable=True),
        sa.Column('set_id', sa.Integer(), nullable=True),
        sa.Column('stat_type', new_stat_type_enum, nullable=True),
        sa.Column('stat_value', sa.Integer(), nullable=True),
        sa.Column('equipped', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['arena_info_id'], ['arena_info.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'skill',
        sa.Column('type', skill_type_enum, nullable=False),
        sa.Column('equipment_id', sa.Text(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('referenced_stat_type', new_stat_type_enum, nullable=True),
        sa.Column('stat_power_ratio', sa.Integer(), nullable=True),
        sa.Column('power', sa.Integer(), nullable=True),
        sa.Column('chance', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(['equipment_id'], ['equipment.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('arena_info', sa.Column('cp', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('arena_info', 'cp')
    op.drop_table('skill')
    op.drop_table('equipment')
    op.drop_table('costume')

    skill_type_enum.drop(op.get_bind(), checkfirst=False)
    elemental_type_enum.drop(op.get_bind(), checkfirst=False)
    item_subtype_enum.drop(op.get_bind(), checkfirst=False)
    item_type_enum.drop(op.get_bind(), checkfirst=False)

    tmp_stat_type_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE costume_stat_sheet ALTER COLUMN "type" TYPE _stattype USING type::text::_stattype')
    op.execute('ALTER TABLE equipment_item_sheet ALTER COLUMN "type" TYPE _stattype USING type::text::_stattype')
    new_stat_type_enum.drop(op.get_bind(), checkfirst=False)
    old_stat_type_enum.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE costume_stat_sheet ALTER COLUMN "type" TYPE stattype USING type::text::stattype')
    op.execute('ALTER TABLE equipment_item_sheet ALTER COLUMN "type" TYPE stattype USING type::text::stattype')
    tmp_stat_type_enum.drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
