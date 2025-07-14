from functools import wraps
from datetime import datetime
import logging


def is_valid_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_date_input(return_value_on_error=None):
    """Декоратор для проверки корректности даты."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            date_str = args[0] if args else kwargs.get("date_str")
            if not is_valid_date(date_str):
                logging.warning(f"Неверный формат даты: '{date_str}'")
                return return_value_on_error
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_time_inputs(start_arg=1, end_arg=2, return_value_on_error=False):
    """Декоратор для проверки start_time и end_time"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_str = args[start_arg]
                end_str = args[end_arg]
            except IndexError:
                logging.warning("Отсутствуют аргументы start_time и end_time.")
                print("Не удалось получить аргументы времени.")
                return return_value_on_error

            if not (is_valid_time(start_str) and is_valid_time(end_str)):
                msg = (
                    f"Неверный формат времени:"
                    f"start='{start_str}',end='{end_str}'"
                )
                logging.warning(msg)
                print(msg)
                return return_value_on_error

            start = datetime.strptime(start_str, "%H:%M")
            end = datetime.strptime(end_str, "%H:%M")

            if start >= end:
                msg = (
                    f"Время начала должно быть меньше конца:"
                    f"start='{start_str}', end='{end_str}'"
                )
                logging.warning(msg)
                print(msg)
                return return_value_on_error

            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_duration_input(arg_index: int = -1, return_value_on_error=None):
    """Декоратор для проверки аргумента duration."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                try:
                    duration = args[arg_index]
                except IndexError:
                    duration = kwargs.get("duration")

                if duration is None:
                    logging.warning("Длительность не указана.")
                    return return_value_on_error

                if not isinstance(duration, (int, float)):
                    logging.warning(
                        f"Длительность должна быть числом."
                        f"Получено: {duration}"
                    )
                    return return_value_on_error

                if duration <= 0:
                    logging.warning(
                        f"Длительность должна быть больше нуля."
                        f"Получено: {duration}"
                    )
                    return return_value_on_error

                return func(*args, **kwargs)

            except Exception as e:
                logging.error(f"Ошибка в validate_duration_input: {e}")
                return return_value_on_error

        return wrapper

    return decorator
