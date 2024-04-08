"""
Test custom Django management commands.
"""

from unittest.mock import patch  # mock the errors
from psycopg2 import OperationalError as Psycopg2Error
# errro that we might get if we connect db and db is not available
from django.core.management import call_command
# simulate the command and check if it works
from django.db.utils import OperationalError
# check if the command is available
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """testing commands"""
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db if db is ready"""
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])
        # self.assertEqual(mock_check_db.call_count, 1)

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db"""
        patched_check.side_effect = [Psycopg2Error] * 3 + \
            [OperationalError] * 3 + [True]  # created errror for 6 time
        call_command('wait_for_db')  # for each call
        # checking how many times check is called
        self.assertEqual(patched_check.call_count, 7)

        patched_check.assert_called_with(databases=['default'])
