import unittest
from scheduler.scheduler import Scheduler


class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()

    def test_get_day_schedule_valid_date(self):
        schedule = self.scheduler.get_day_schedule("2025-02-18")
        self.assertIsNotNone(schedule)

    def test_get_day_schedule_invalid_format(self):
        schedule = self.scheduler.get_day_schedule("2025-02-189")
        self.assertIsNone(schedule)

    def test_get_busy_slots(self):
        busy = self.scheduler.get_busy_slots("2025-02-18")
        self.assertIsInstance(busy, list)

    def test_get_free_slots(self):
        free = self.scheduler.get_free_slots("2025-02-18")
        self.assertIsInstance(free, list)

    def test_is_free_valid(self):
        result = self.scheduler.is_free("2025-02-18", "13:00", "14:00")
        self.assertIn(result, [True, False])  # может быть и True и False

    def test_is_free_invalid_time(self):
        result = self.scheduler.is_free("2025-02-18", "25:00", "26:00")
        self.assertFalse(result)

    def test_find_free_slot_for_duration(self):
        slot = self.scheduler.find_free_slot_for_duration("2025-02-18", 30)
        if slot:
            self.assertIn("start", slot)
            self.assertIn("end", slot)

    def test_find_all_free_slots_for_duration(self):
        slots = self.scheduler.find_all_free_slots_for_duration("2025-02-18", 30)
        self.assertIsInstance(slots, list)
        for slot in slots:
            self.assertIn("start", slot)
            self.assertIn("end", slot)
