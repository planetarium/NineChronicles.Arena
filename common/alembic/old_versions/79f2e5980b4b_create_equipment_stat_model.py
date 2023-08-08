"""Create equipment stat model

Revision ID: 79f2e5980b4b
Revises: 3a2eb22178c2
Create Date: 2023-08-03 02:57:11.777914

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '79f2e5980b4b'
down_revision = '3a2eb22178c2'
branch_labels = None
depends_on = None

stat_type_enum = postgresql.ENUM(
    "NONE", "HP", "ATK", "DEF", "CRI", "HIT", "SPD", "DRV", "DRR", "CDMG", "APTN", "THORN",
    name="stattype", create_type=False
)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipment_stat',
                    sa.Column('equipment_id', sa.Text(), nullable=False),
                    sa.Column('stat_type', stat_type_enum, nullable=False),
                    sa.Column('stat_value', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.ForeignKeyConstraint(['equipment_id'], ['equipment.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipment_stat')
    # ### end Alembic commands ###