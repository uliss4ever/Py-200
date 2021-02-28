from typing import Optional, overload
import logging

logger = logging.getLogger(__name__)


class TimeDelta:
    def __init__(self, days: Optional[int] = None, months: Optional[int] = None, years: Optional[int] = None):
        logger.debug("start init")
        self.day = days or 0
        self.month = months or 0
        self.year = years or 0


class Date:
    """Класс для работы с датами"""
    days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    days_leap = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    @overload
    def __init__(self, day: int, month: int, year: int):
        """Создание даты из трех чисел"""

    @overload
    def __init__(self, date: str):
        """Создание даты из строки формата dd.mm.yyyy"""

    def __init__(self, *args):
        """ ВАЖНО! Сначала устанавливаются год и месяц, и только потом - день. Потому
что при установке дня проверяется правильность даты, для чего нужны год и
месяц. Например, 29 число может быть неправильным в феврале, но только
если год не високосный"""
        if len(args) == 3 and all(isinstance(i, int) for i in args):
            self.year = int(args[2])
            self.month = int(args[1])
            self.day = int(args[0])
        elif len(args) == 1 and isinstance(args[0], str):
            values = args[0].split('.')

            if len(values) != 3:
                raise ValueError("Incorrect init value")

            self.year, self.month, self.day = int(values[2]), int(values[1]), int(values[0])
        else:
            raise ValueError("Incorrect init value")

    def __str__(self) -> str:
        """Возвращает дату в формате dd.mm.yyyy"""
        return f"{self.day:02d}.{self.month:02d}.{self.year:04d}"

    def __repr__(self) -> str:
        """Возвращает дату в формате Date(day, month, year)"""
        return f"Date({self._day}, {self._month}, {self._year})"

    @classmethod
    def is_leap_year(cls, year) -> bool:
        """Проверяет, является ли год високосным"""
        if not isinstance(year, int):
            raise ValueError
        if year % 4 != 0 or (year % 100 == 0 and year % 400 != 0):  # надо ли тут cls.year или просто year
            return False
        return True

    @classmethod
    def get_max_day(cls, month: int, year: int) -> int:
        """Возвращает максимальное количество дней в месяце для указанного года"""
        if cls.is_leap_year(year):
            return cls.days_leap[month - 1]
        else:
            return cls.days[month - 1]

    @classmethod
    def is_valid_date(cls, day: int, month: int, year: int):
        """Проверяет, является ли дата корректной"""
        if month < 1 or month > 12:
            return False
        """TODO: разобраться тут"""
        if day < 0 or day > cls.get_max_day(month, year):
            return False
        return True

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value: int):
        """value от 1 до 31. Проверять значение и корректность даты"""
        if not self.is_valid_date(value, self.month, self.year): # self.is_valid.. or Date
            raise ValueError("Incorrect day")
        self._day = value

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value: int):
        """value от 1 до 12. Проверять значение и корректность даты"""
        if 1 <= value <= 12:
            self._month = value
            if not self.is_valid_date(self.day, value, self.year):
                raise ValueError
        else:
            raise ValueError("Incorrect month")



    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value: int):
        """value от 1 до ... . Проверять значение и корректность даты"""
        self._year = value
        if not self.is_valid_date(self.day, self.month, value):
            raise ValueError

    def __sub__(self, other: "Date") -> int:
        """Разница между датой self и other (-)"""

        days_my = self.day
        days_other = other.day
        for ye in range(self.year):
            days_my += 366 if self.is_leap_year(ye) else 365
        for ye in range(other.year):
            days_other += 366 if self.is_leap_year(ye) else 365

        for i in range(self.month - 1):
            days_my += self.days[i]
        for i in range(other.month - 1):
            days_other += other.days[i]

        if self.is_leap_year(self.year) and self.month > 2:
            days_my += 1
        if self.is_leap_year(other.year) and other.month > 2:
            days_other += 1

        return days_my - days_other

    def __add__(self, other: TimeDelta) -> "Date":
        """Складывает self и некий timedeltа. Возвращает НОВЫЙ инстанс Date, self не меняет (+)"""

        c = Date(self.day, self.month, self.year)
        c += other
        return c

    def __iadd__(self, other: TimeDelta) -> "Date":
        """Добавляет к self некий timedelta меняя сам self (+=)"""

        self.year += other.year
        self._month += other.month  # если month (без _) то он проверит его в сеттере и выкинет error
        self._day += other.day
        while self._month > 12:
            self.year += 1
            self._month -= 12
        while self._day > self.get_max_day(self.month, self.year):
            self._day -= self.get_max_day(self.month, self.year)
            self._month += 1
            if self._month > 12:
                self.year += 1
                self._month -= 12
        return self


def main():
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    logger.debug("start main")
    d1 = Date(30, 12, 2021)
    # print(d1)
    # print(str(d1))
    d3 = Date("30.12.2021")
    # print(d1.day)
    d1.day = 31
    d2 = Date(31, 1, 2020)
    # d2.day = 29
    d1 += TimeDelta(1)
    d2.month = 2
    print(d2.day)
    # print(repr(d1-d2))
    # print(d1)


if __name__ == "__main__":
    main()
