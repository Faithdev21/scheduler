import unittest
from scheduler.utils import (
    format_time_interval_list,
    return_is_free,
    return_found_slot,
    return_slots_for_duration,
)


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.valid_date = "2025-02-18"
        self.invalid_date = "2025-02-189"
        self.valid_time = "12:00"
        self.invalid_time = "99:00"
        self.valid_duration = 20
        self.invalid_duration = -5

        self.slots = [
            {'start': self._time("09:00"), 'end': self._time("10:00")},
            {'start': self._time("11:00"), 'end': self._time("12:00")},
        ]

        self.slot_dict = {"start": "09:00", "end": "09:20"}

    def _time(self, time_str):
        from datetime import datetime
        return datetime.strptime(time_str, "%H:%M").time()

    def test_format_time_interval_list(self):
        output = format_time_interval_list(self.valid_date, self.slots, "Тест")
        self.assertIn("09:00 – 10:00", output)

    def test_format_time_interval_list_invalid_date(self):
        output = format_time_interval_list(self.invalid_date, self.slots, "Проверка")
        self.assertEqual(output, "Неверный формат даты.")

    def test_return_is_free_true(self):
        result = return_is_free(self.valid_date, "10:00", "11:00", True)
        self.assertIn("Доступен", result)

    def test_return_is_free_invalid_date(self):
        result = return_is_free(self.invalid_date, "10:00", "11:00", False)
        self.assertEqual(result, "Неверный формат даты.")

    def test_return_found_slot_success(self):
        result = return_found_slot(self.valid_date, self.slot_dict, 20)
        self.assertIn("09:00", result)

    def test_return_found_slot_invalid_duration(self):
        result = return_found_slot(self.valid_date, self.slot_dict, self.invalid_duration)
        self.assertEqual(result, "Неверная длительность.")

    def test_return_slots_for_duration(self):
        result = return_slots_for_duration(self.valid_date, [self.slot_dict], 20)
        self.assertIsNone(result)
