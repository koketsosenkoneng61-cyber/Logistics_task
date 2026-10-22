import unittest
import app as app_module


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()

    def test_health_endpoint(self):
        self.assertEqual(self.client.get("/health").get_json(), {"status": "ok"})

    def test_driver_list_is_priority_sorted(self):
        data = self.client.get("/drivers/Thabo/tasks").get_json()
        self.assertEqual(data[0]["priority"], "high")

    def test_create_task_then_see_it(self):
        r = self.client.post("/tasks", json={"title": "Extra run", "driver": "Lerato",
                                              "priority": "low", "due": "16:00"})
        self.assertEqual(r.status_code, 201)
        listed = self.client.get("/drivers/Lerato/tasks").get_json()
        self.assertEqual(listed[0]["title"], "Extra run")

    def test_invalid_task_returns_400(self):
        r = self.client.post("/tasks", json={"title": "", "driver": "A", "priority": "low", "due": "10:00"})
        self.assertEqual(r.status_code, 400)

    def test_complete_unknown_task_returns_404(self):
        self.assertEqual(self.client.post("/tasks/999/complete").status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
