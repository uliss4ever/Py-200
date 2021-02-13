from typing import Optional, overload


class TimeDelta:
    def __init__(self, days: Optional[int] = None, months: Optional[int] = None, years: Optional[int] = None):
        if not days:
            self.day = 0
        else:
            self.day = days

        if not months:
            self.month = 0
        else:
            self.month = months

        if not years:
            self.year = 0
        else:
            self.year = years


class Date:
    """Класс для работы с датами"""
    days = ((1, 31), (2, 28), (3, 31), (4, 30), (5, 31), (6, 30),
            (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31))

    days_leap = ((1, 31), (2, 29), (3, 31), (4, 30), (5, 31), (6, 30),
                 (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31))

    @overload
    def __init__(self, day: int, month: int, year: int):
        """Создание даты из трех чисел"""

    @overload
    def __init__(self, date: str):
        """Создание даты из строки формата dd.mm.yyyy"""

    def __init__(self, *args):
        if len(args) == 3 and all(isinstance(i, int) for i in args):
            self.day = int(args[0])
            self.month = int(args[1])
            self.year = int(args[2])
        elif len(args) == 1 and isinstance(args[0], str):
            values = args[0].split('.')
            if len(values) != 3:
                raise ValueError("Incorrect init value")
            self.day, self.month, self.year = int(values[0]), int(values[1]), int(values[2])
        else:
            raise ValueError("Incorrect init value")

        self.days = ((1, 31), (2, 28), (3, 31), (4, 30), (5, 31), (6, 30),
                     (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31))
        self.days_leap = ((1, 31), (2, 29), (3, 31), (4, 30), (5, 31), (6, 30),
                          (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31))

    def __str__(self) -> str:
        """Возвращает дату в формате dd.mm.yyyy"""
        return str(self.day // 10) + str(self.day % 10) + "." + \
               str(self.month // 10) + str(self.month % 10) + "." + \
               str(self.year // 1000) + str((self.year // 100) % 10) + str((self.year // 10) % 10) + str(self.year % 10)

    def __repr__(self) -> str:
        """Возвращает дату в формате Date(day, month, year)"""
        return f"Date({self.day})"

    def is_leap_year(self, year) -> bool:
        """Проверяет, является ли год високосным"""
        if not isinstance(year, int):
            raise ValueError
        if year % 4 != 0 or (year % 100 == 0 and year % 400 != 0):
            return False
        return True

    def get_max_day(self, month: int, year: int) -> int:
        """Возвращает максимальное количество дней в месяце для указанного года"""
        if self.is_leap_year(year):
            return self.days_leap[month - 1][1]
        else:
            return self.days[month - 1][1]

    def is_valid_date(self, day: int, month: int, year: int):
        """Проверяет, является ли дата корректной"""
        if month > 12:
            return False

        if self.is_leap_year(year):
            if day > self.days_leap[month - 1][1]:
                return False
        elif day > self.days[month - 1][1]:
            return False
        return True

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value: int):
        """value от 1 до 31. Проверять значение и корректность даты"""
        if 1 <= value <= 31:
            self._day = value
        else:
            raise ValueError("Incorrect day")

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value: int):
        """value от 1 до 12. Проверять значение и корректность даты"""
        if 1 <= value <= 12:
            self._month = value
        else:
            raise ValueError("Incorrect month")

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value: int):
        """value от 1 до ... . Проверять значение и корректность даты"""
        self._year = value

    def __sub__(self, other: "Date") -> int:
        """Разница между датой self и other (-)"""
        days_my = self.day
        days_other = other.day
        for i in range(self.month - 1):
            days_my += self.days[i][1]
        for i in range(other.month - 1):
            days_other += other.days[i][1]

        if self.month > 2:
            days_my += 1
        if other.month > 2:
            days_other += 1

        days_my += self.year * 365 + self.year // 4
        days_other += other.year * 365 + other.year // 4

        return max(days_my, days_other) - min(days_my, days_other)

    def __add__(self, other: TimeDelta) -> "Date":
        """Складывает self и некий timedeltа. Возвращает НОВЫЙ инстанс Date, self не меняет (+)"""
        day = self.day
        month = self.month
        year = self.year

        all_days = other.day
        for i in range(other.month - 1):
            all_days += self.days[i][1]
        if other.month > 2:
            all_days += 1

        all_days += other.year * 365 + other.year // 4

        for i in range(0, all_days):
            day += 1
            if self.is_leap_year(year):
                if day > self.days_leap[month - 1][1]:
                    day = 1
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
            else:
                if day > self.days[month - 1][1]:
                    day = 1
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1

        return Date(day, month, year)

    def __iadd__(self, other: TimeDelta) -> "Date":
        """Добавляет к self некий timedelta меняя сам self (+=)"""
        return self + other


if __name__ == "__main__":
    d1 = Date(30, 12, 2021)
    d2 = Date(1, 3, 2029)
    d1 += TimeDelta(1)
    print(d1.__str__())
