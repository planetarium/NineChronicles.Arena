from decimal import *
from functools import reduce
from typing import Optional, List

from sqlalchemy import select

from common.const import INT_MAX
from common.enums import StatType
from common.models.avatar import ArenaInfo, Equipment
from common.models.sheet import CharacterSheet, CostumeStatSheet, RuneOptionSheet


class CPCalculator:
    def __init__(self, sess):
        self.sess = sess
        self.__char_data = None
        self.__costume_data = None
        self.__rune_data = None

        self.avatar: Optional[ArenaInfo] = None

    def __get_char_data(self, char_id: int):
        self.__char_data = self.sess.scalar(select(CharacterSheet).where(CharacterSheet.id == char_id))

    def __get_costume_data(self, costume_id_list: List[int]):
        self.__costume_data = self.sess.scalars(
            select(CostumeStatSheet)
            .where(CostumeStatSheet.costume_id.in_(costume_id_list))
        )

    def __get_rune_data(self):
        self.__rune_data = {(x.rune_id, x.level): x.cp for x in self.sess.scalars(select(RuneOptionSheet))}

    def get_cp(self, avatar: ArenaInfo) -> int:
        self.avatar = avatar
        self.__get_char_data(self.avatar.character_id)

        char_cp: Decimal = self._get_char_cp()
        equipment_cp: Decimal = self._get_total_equipment_cp()
        costume_cp: Decimal = self._get_costume_cp()
        rune_cp: Decimal = self._get_rune_cp()

        return min(int(char_cp + equipment_cp + costume_cp + rune_cp), INT_MAX)

    def _get_char_cp(self) -> Decimal:
        return (
                self.__get_cp(
                    StatType.HP,
                    Decimal(self.__char_data.hp) + Decimal(self.__char_data.lv_hp) * Decimal(self.avatar.level - 1),
                    self.avatar.level
                ) +
                self.__get_cp(
                    StatType.ATK,
                    Decimal(self.__char_data.atk) + Decimal(self.__char_data.lv_atk) * Decimal(self.avatar.level - 1),
                    self.avatar.level
                ) +
                self.__get_cp(
                    StatType.DEF,
                    Decimal(self.__char_data.dfc) + Decimal(self.__char_data.lv_dfc) * Decimal(self.avatar.level - 1),
                    self.avatar.level
                ) +
                self.__get_cp(
                    StatType.CRI,
                    Decimal(self.__char_data.cri) + Decimal(self.__char_data.lv_cri) * Decimal(self.avatar.level - 1),
                    self.avatar.level
                ) +
                self.__get_cp(
                    StatType.HIT,
                    Decimal(self.__char_data.hit) + Decimal(self.__char_data.lv_hit) * Decimal(self.avatar.level - 1),
                    self.avatar.level
                ) +
                self.__get_cp(
                    StatType.SPD,
                    Decimal(self.__char_data.spd) + Decimal(self.__char_data.lv_spd) * Decimal(self.avatar.level - 1),
                    self.avatar.level
                )
        )

    def _get_total_equipment_cp(self) -> Decimal:
        return reduce(lambda cp, eq: cp + self._get_single_equipment_cp(eq), self.avatar.equipment_list, Decimal("0"))

    def _get_single_equipment_cp(self, eq: Equipment) -> Decimal:
        base_eq_cp = reduce(lambda cp, stat: cp + self.__get_cp(stat.stat_type, stat.stat_value), eq.stats_list,
                            Decimal("0"))
        return self.__apply_skill_multiplier(base_eq_cp, len(eq.all_skill_list))

    def _get_costume_cp(self) -> Decimal:
        self.__get_costume_data([x.sheet_id for x in self.avatar.costume_list])
        return reduce(lambda cp, cos: cp + self.__get_cp(cos.type, cos.value), self.__costume_data, Decimal("0"))

    def _get_rune_cp(self) -> Decimal:
        self.__get_rune_data()
        return reduce(lambda cp, rune: cp + self.__rune_data[(rune.item_id, rune.level)], self.__rune_data,
                      Decimal("0"))

    def __apply_skill_multiplier(self, base: Decimal, skill_count: int) -> Decimal:
        if skill_count == 0:
            return base
        elif skill_count == 1:
            return base * Decimal("1.15")
        else:  # skill_count >=2
            return base * Decimal("1.35")

    def __get_cp(self, stat_type: StatType, base: Decimal, level: int = 1) -> Decimal:
        match stat_type:
            case StatType.NONE:
                return Decimal("0")
            case StatType.HP:
                return base * Decimal("0.7")
            case StatType.ATK | StatType.DEF | StatType.DRV:
                return base * Decimal("10.5")
            case StatType.SPD | StatType.CDMG:
                return base * Decimal("3")
            case StatType.HIT:
                return base * Decimal("2.3")
            case StatType.CRI | StatType.DRR:
                return base * level * Decimal("20")
            case StatType.APTN:
                return base * Decimal("5")
            case StatType.THORN:
                return base * Decimal("1")
            case _:
                raise TypeError(f"{stat_type.name} is not supported in CP calculator.")
