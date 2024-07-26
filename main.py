from abc import ABC, abstractmethod
import asyncio
from decimal import Decimal, ROUND_HALF_UP
import random
from typing import List


# Стандартный набор характеристик
ATTACK = 15.0
HEALTH = 150.0
ARMOR = 5.0

# Коэффициеты усиления в зависимости от класса
ASSASIN_ATTACK_COEF = 1.5
ADVENTURER_HEALTH_COEF = 1.25
ARTISAN_ARMOR_COEF = 2


class Toad(ABC):
    """Родительский класс жабки."""

    def __init__(self) -> None:
        self.attack = Decimal(str(ATTACK))
        self.health = Decimal(str(HEALTH))
        self.armor = Decimal(str(ARMOR))

    @abstractmethod
    def change_params_values(self) -> None:
        """Измение значений параметров жабки."""
        pass

    @staticmethod
    def rounding_to_one_decimal_point(param: Decimal) -> Decimal:
        """
        Округление значения параметра жабки до одного десятичного знака
        (Округляет число в сторону повышения,
        если после него идет число 5 или выше).
        """
        return param.quantize(Decimal("1.0"), ROUND_HALF_UP)

    def hit(self) -> Decimal:
        """
        Расчет урона
        (Выбирается случайное значение в диапазоне [урон / 2 ; урон]
        и округляется до одного десятичного знака).
        """
        value = random.uniform(float(self.attack) / 2, float(self.attack))
        return self.rounding_to_one_decimal_point(Decimal(str(value)))

    def block(self) -> Decimal:
        """
        Расчет блока
        (Выбирается случайное значение в диапазоне [0 ; броня]
        и округляется до одного десятичного знака).
        """
        value = random.uniform(0, float(self.armor))
        return self.rounding_to_one_decimal_point(Decimal(str(value)))


class ToadAssasin(Toad):
    """
    Дочерний класс жабки-ассасина
    (Урон увеличен на 50%).
    """
    def change_params_values(self) -> None:
        self.attack *= Decimal(str(ASSASIN_ATTACK_COEF))
        self.attack = self.rounding_to_one_decimal_point(self.attack)


class ToadAdventurer(Toad):
    """
    Дочерний класс жабки-авантюриста
    (Здоровье увеличено на 25%).
    """
    def change_params_values(self) -> None:
        self.health *= Decimal(str(ADVENTURER_HEALTH_COEF))
        self.health = self.rounding_to_one_decimal_point(self.health)


class ToadArtisan(Toad):
    """
    Дочерний класс жабки-ремесленника
    (Броня увеличена на 100%).
    """
    def change_params_values(self) -> None:
        self.armor *= Decimal(str(ARTISAN_ARMOR_COEF))
        self.armor = self.rounding_to_one_decimal_point(self.armor)


async def battle(toad_1: Toad, toad_2: Toad) -> int:
    """
    Функция реализующая бой между двумя жабками
    (При победе первой жабки - возвращает 0,
     При победе второй жабки - возвращает 1).
    """
    while True:
        if toad_1.health > 0:
            damage = toad_1.hit() - toad_2.block()
            if damage > 0:
                toad_2.health -= damage
        else:
            return 1
        if toad_2.health > 0:
            damage = toad_1.hit() - toad_2.block()
            toad_1.health -= damage
        else:
            return 0


async def match() -> None:
    """Функция реализующая матч содержащий 100 боев."""

    match_score: List[int] = [0, 0]
    toad_classes: List[type] = [ToadAssasin, ToadAdventurer, ToadArtisan]

    for _ in range(100):
        toad_1: Toad = random.choice(toad_classes)()
        toad_1.change_params_values()
        toad_2: Toad = random.choice(toad_classes)()
        toad_2.change_params_values()
        winner_index: int = await battle(toad_1, toad_2)
        match_score[winner_index] += 1

    print(
        "Исход матча:\n"
        f"Победы первой жабки: {match_score[0]}\n"
        f"Победы второй жабки: {match_score[1]}\n"
    )


async def main() -> None:
    """
    Главная функция.
    Проводит параллельно два матча.
    """
    await asyncio.gather(match(), match())


if __name__ == "__main__":
    asyncio.run(main())
