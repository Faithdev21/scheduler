from scheduler.scheduler import Scheduler
from scheduler.utils import format_time_interval_list, return_is_free, return_found_slot, return_slots_for_duration

scheduler = Scheduler()
date = "2025-02-18"

# 1. Занятые промежутки
busy = scheduler.get_busy_slots(date)
print(format_time_interval_list(date, busy, "Занятые промежутки"))
print()

# 2. Свободные промежутки
free = scheduler.get_free_slots(date)
print(format_time_interval_list(date, free, "Свободные промежутки"))
print()

# 3. Проверка свободен ли промежуток
start = "10:00"
end = "11:30"

is_available = scheduler.is_free(date, start, end)
print(return_is_free(date, start, end, is_available))
print()

# 4. Поиск свободного интервала заданной длительности
duration = 30

slot = scheduler.find_free_slot_for_duration(date, duration)
print(return_found_slot(date, slot, duration))
print()

slots = scheduler.find_all_free_slots_for_duration(date, duration)
return_slots_for_duration(date, slots, duration)

