from datetime import datetime, timedelta
from scheduler.validators import (
    validate_time_inputs,
    validate_date_input,
    validate_duration_input,
)


def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()


def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def to_datetime(date, time):
    return datetime.combine(date, time)


def timedelta_minutes(minutes):
    return timedelta(minutes=minutes)


@validate_date_input(return_value_on_error="Неверный формат даты.")
def format_time_interval_list(date_str, interval_list, title="Интервалы"):
    if not isinstance(interval_list, list) or not all(
        isinstance(i, dict) for i in interval_list
    ):
        return (
            f"Ошибка: невозможно отформатировать интервалы на {date_str}"
            f"– некорректные данные."
        )

    if not interval_list:
        return f"{title} на {date_str}: Нет доступных интервалов."

    formatted_list = [
        (
            f"- {interval['start'].strftime('%H:%M')} "
            f"– {interval['end'].strftime('%H:%M')}"
        )

        for interval in interval_list
    ]
    return f"{title} на {date_str}:\n" + "\n".join(formatted_list)


@validate_date_input(return_value_on_error="Неверный формат даты.")
@validate_time_inputs(return_value_on_error="Неверный формат времени.")
def return_is_free(date_str, start_time, end_time, is_available):
    print(f"Промежуток {start_time} – {end_time} на {date_str}:")
    return (
        "Доступен" if is_available
        else "Занят или выходит за рамки расписания"
    )


@validate_date_input(return_value_on_error="Неверный формат даты.")
@validate_duration_input(return_value_on_error="Неверная длительность.")
def return_found_slot(date_str, found_slot, duration):
    print(
        f"Ближайшее свободное окно на {date_str}"
        f"для заявки длительностью {duration} мин:"
    )

    if found_slot:
        return f"{found_slot['start']} – {found_slot['end']}"
    return "Нет подходящего свободного окна"


@validate_date_input(return_value_on_error="Неверный формат даты.")
@validate_duration_input(return_value_on_error="Неверная длительность.")
def return_slots_for_duration(date_str, slots, duration_min):
    if not slots:
        return (
            f"Нет свободных промежутков на {date_str}"
            f"для длительности {duration_min} минут."
        )
    print(
        f"Свободные промежутки на {date_str}"
        f"для длительности {duration_min} минут:"
    )
    for slot in slots:
        print(f"• {slot['start']} – {slot['end']}")
    return
