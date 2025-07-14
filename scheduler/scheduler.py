import requests
from datetime import timedelta
from operator import itemgetter

from scheduler.exceptions import ScheduleError
from scheduler.utils import parse_date, parse_time, to_datetime


class Scheduler:
    ENDPOINT = "https://ofc-test-01.tspb.su/test-task/"

    def __init__(self):
        self.days = {}
        self.slots = []
        self.fetch_data()

    def fetch_data(self):
        try:
            response = requests.get(self.ENDPOINT)
            response.raise_for_status()
            data = response.json()

            for day in data["days"]:
                date = parse_date(day["date"])
                self.days[date] = {
                    "id": day["id"],
                    "start": parse_time(day["start"]),
                    "end": parse_time(day["end"]),
                }

            self.slots = data["timeslots"]

        except requests.RequestException:
            raise ScheduleError("Ошибка при получении данных с сервера")

    def get_day_schedule(self, date_str):
        try:
            date = parse_date(date_str)
            return self.days.get(date)

        except ValueError:
            return

    def get_busy_slots(self, date_str):
        """Возвращает занятые промежутки на дату"""
        day_info = self.get_day_schedule(date_str)
        if not day_info:
            return []
        day_id = day_info["id"]
        return sorted(
            [
                {
                    "start": parse_time(slot["start"]),
                    "end": parse_time(slot["end"])
                }
                for slot in self.slots
                if slot["day_id"] == day_id
            ],
            key=itemgetter("start"),
        )

    def get_free_slots(self, date_str):
        """Возвращает список свободных временных промежутков"""
        day_info = self.get_day_schedule(date_str)
        if not day_info:
            return []
        busy = self.get_busy_slots(date_str)

        start = day_info["start"]
        end = day_info["end"]
        free = []
        pointer = start

        for slot in busy:
            if slot["start"] > pointer:
                free.append({"start": pointer, "end": slot["start"]})
            pointer = max(pointer, slot["end"])

        if pointer < end:
            free.append({"start": pointer, "end": end})
        return free

    def is_free(self, date_str, start_str, end_str):
        """Проверить доступен ли интервал"""
        try:
            start = parse_time(start_str)
            end = parse_time(end_str)
            if start >= end:
                return False
            free_slots = self.get_free_slots(date_str)
            for slot in free_slots:
                if slot["start"] <= start and slot["end"] >= end:
                    return True
            return False
        except ValueError:
            return False

    def find_free_slot_for_duration(self, date_str, duration_min):
        """Найти свободный слот с необходимой длительностью в минутах"""
        try:
            duration = timedelta(minutes=duration_min)
            date = parse_date(date_str)
            free_slots = self.get_free_slots(date_str)

            for slot in free_slots:
                slot_start = to_datetime(date, slot["start"])
                slot_end = to_datetime(date, slot["end"])

                if slot_end - slot_start >= duration:
                    new_end = (slot_start + duration).time()
                    return {
                        "start": slot["start"].strftime("%H:%M"),
                        "end": new_end.strftime("%H:%M"),
                    }
            return
        except Exception:
            return

    def find_all_free_slots_for_duration(
            self, date_str: str, duration_min: int
    ):
        """
        Возвращает список всех свободных слотов указанной продолжительности
        """
        try:
            duration = timedelta(minutes=duration_min)
            date = parse_date(date_str)
            slots = self.get_free_slots(date_str)
            result = []

            for slot in slots:
                start_dt = to_datetime(date, slot["start"])
                end_dt = to_datetime(date, slot["end"])

                available = end_dt - start_dt
                if available >= duration:
                    chunk_start = start_dt
                    while chunk_start + duration <= end_dt:
                        chunk_end = chunk_start + duration
                        result.append(
                            {
                                "start": chunk_start.time().strftime("%H:%M"),
                                "end": chunk_end.time().strftime("%H:%M"),
                            }
                        )
                        chunk_start += duration  # следующая итерация

            return result
        except Exception:
            return []
