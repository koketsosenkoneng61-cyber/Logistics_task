import unittest
from tasks import TaskManager, ValidationError


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.tm = TaskManager()
        self.tm.add_task("Deliver parcels to Soweto", "Thabo", "medium", "10:00")
        self.tm.add_task("Collect pallets Smith Street", "Thabo", "high", "09:00")
        self.tm.add_task("Return empty crates", "Lerato", "low", "15:30")

    def test_01_add_valid_task(self):
        t = self.tm.add_task("New delivery", "Thabo", "low", "12:00")
        self.assertEqual(t.id, 4)
        self.assertEqual(t.status, "assigned")

    def test_02_blank_title_rejected(self):
        with self.assertRaises(ValidationError):
            self.tm.add_task("   ", "Thabo", "low", "12:00")

    def test_03_bad_priority_rejected(self):
        with self.assertRaises(ValidationError):
            self.tm.add_task("X", "Thabo", "urgent", "12:00")

    def test_04_midnight_edge_case(self):
        t = self.tm.add_task("Night run", "Thabo", "low", "00:00")
        self.assertEqual(t.due, "00:00")

    def test_05_invalid_time_rejected(self):
        with self.assertRaises(ValidationError):
            self.tm.add_task("X", "Thabo", "low", "25:99")

    def test_06_binary_search_finds_task(self):
        self.assertEqual(self.tm.get_by_id(3).title, "Return empty crates")

    def test_07_binary_search_missing_id(self):
        self.assertIsNone(self.tm.get_by_id(99))

    def test_08_high_priority_comes_first(self):
        self.assertEqual(self.tm.next_task("Thabo").id, 2)

    def test_09_search_is_not_case_sensitive(self):
        found = self.tm.search_title("smith")
        self.assertEqual([t.id for t in found], [2])

    def test_10_complete_task_removes_it_from_list(self):
        self.tm.complete_task(2)
        self.assertEqual([t.id for t in self.tm.task_list("Thabo")], [1])

    def test_11_complete_unknown_task(self):
        with self.assertRaises(KeyError):
            self.tm.complete_task(50)

    def test_12_reassign_when_driver_sick(self):
        self.tm.reassign(1, "Lerato")
        self.assertEqual(self.tm.get_by_id(1).driver, "Lerato")


if __name__ == "__main__":
    unittest.main(verbosity=2)
