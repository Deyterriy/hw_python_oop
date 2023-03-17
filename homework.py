from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.message.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Классы-наследники реализуют метод')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message: InfoMessage = InfoMessage(self.__class__.__name__,
                                                self.duration,
                                                self.get_distance(),
                                                self.get_mean_speed(),
                                                self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        Running.calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                            * self.get_mean_speed()
                            + self.CALORIES_MEAN_SPEED_SHIFT)
                            * self.weight / self.M_IN_KM
                            * (self.duration * self.MIN_IN_H))
        return Running.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    K_W1: float = 0.035
    K_W2: float = 0.029
    KMH_IN_MS: float = 0.278
    CM_IN_M: int = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        calories = ((self.K_W1 * self.weight
                     + (((self.get_mean_speed() * self.KMH_IN_MS)**2)
                        / (self.height / self.CM_IN_M))
                    * self.K_W2 * self.weight)
                    * self.duration * self.MIN_IN_H)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    K_SW1: float = 1.1
    K_SW2: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения(Плавание)."""
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.get_mean_speed() + self.K_SW1)
                    * self.K_SW2 * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list[int,
                                               float,
                                               float,
                                               float,
                                               int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    types_of_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in types_of_training:
        training_type: Training = types_of_training[workout_type](*data)
        return training_type
    else:
        raise KeyError('Неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
