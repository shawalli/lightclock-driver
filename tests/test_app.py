from unittest import TestCase, mock

from app import Colors, Database
from arrow import now


class TestDatabase(TestCase):
    def setUp(self) -> None:
        self.db = Database()

    def test_create_event(self) -> None:
        self.assertEqual(0, len(self.db))

        start_time = now()
        end_time = start_time.shift(minutes=5)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        self.assertEqual(1, len(self.db))
        self.assertEqual(start_time, self.db.events[0].start_time)
        self.assertEqual(end_time, self.db.events[0].end_time)
        self.assertEqual(color, self.db.events[0].color)
        self.assertEqual(0, self.db.events[0].record_id)

    def test_create_event_order(self):
        start_time = now()
        end_time = start_time.shift(minutes=5)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        start_time = end_time
        end_time = start_time.shift(minutes=10)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        self.assertEqual(2, len(self.db))
        self.assertEqual(start_time, self.db.events[1].start_time)
        self.assertEqual(end_time, self.db.events[1].end_time)
        self.assertEqual(color, self.db.events[1].color)
        self.assertEqual(1, self.db.events[1].record_id)

    def test_find_current_event(self):
        start_time = now()
        end_time = start_time.shift(minutes=5)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        start_time = end_time
        end_time = start_time.shift(minutes=10)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        mock_now = start_time.shift(minutes=6)
        with mock.patch("app.now", return_value=mock_now):
            actual_event = self.db.find_current_event()

            self.assertEqual(self.db.events[1], actual_event)

    def test_find_current_event_no_event_match(self):
        start_time = now()
        end_time = start_time.shift(minutes=5)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        start_time = end_time
        end_time = start_time.shift(minutes=10)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        mock_now = start_time.shift(minutes=30)
        with mock.patch("app.now", return_value=mock_now):
            actual_event = self.db.find_current_event()

            self.assertIs(actual_event, None)

    def test_find_current_event_lower_boundary(self):
        start_time = now()
        end_time = start_time.shift(minutes=5)
        color = Colors.RED

        mock_now = start_time

        self.db.create_event(start_time, end_time, color)

        start_time = end_time
        end_time = start_time.shift(minutes=10)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        with mock.patch("app.now", return_value=mock_now):
            actual_event = self.db.find_current_event()

            self.assertEqual(self.db.events[0], actual_event)

    def test_find_current_event_upper_boundary(self):
        start_time = now()
        end_time = start_time.shift(minutes=5)
        color = Colors.RED

        mock_now = end_time

        self.db.create_event(start_time, end_time, color)

        start_time = end_time
        end_time = start_time.shift(minutes=10)
        color = Colors.RED

        self.db.create_event(start_time, end_time, color)

        with mock.patch("app.now", return_value=mock_now):
            actual_event = self.db.find_current_event()

            self.assertEqual(self.db.events[1], actual_event)
