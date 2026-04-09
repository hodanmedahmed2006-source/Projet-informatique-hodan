import unittest
from unittest.mock import patch
import sys
import os

# Add the project root to the path so that src can be imported
# This allows the test to find the modules inside the src/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the modules we want to test
from src import registry
from src import validation
from src import report_utils


class TestValidation(unittest.TestCase):
    """Test the validation functions in validation.py."""
    # This class tests all input validation functions (ID, name, phone, grade)

    def test_validate_id_positive_new(self):
        """Valid positive ID not in dictionary."""
        students = {}  # empty student dictionary
        # validate_id should convert "123" to int 123 because it's a new ID
        self.assertEqual(validation.validate_id(students, "123", True), 123)

    def test_validate_id_zero(self):
        """ID must be positive."""
        students = {}
        # Passing "0" should raise a ValueError saying "positive"
        with self.assertRaises(ValueError) as context:
            validation.validate_id(students, "0", True)
        self.assertIn("positive", str(context.exception))

    def test_validate_id_non_integer(self):
        """ID must be an integer."""
        students = {}
        # Non-numeric string should raise ValueError about "integer"
        with self.assertRaises(ValueError) as context:
            validation.validate_id(students, "abc", True)
        self.assertIn("integer", str(context.exception))

    def test_validate_id_exists_new(self):
        """When adding, ID must be unique."""
        students = {101: {}}  # existing student with ID 101
        # Trying to add another student with same ID should raise "already exists"
        with self.assertRaises(ValueError) as context:
            validation.validate_id(students, "101", True)
        self.assertIn("already exists", str(context.exception))

    def test_validate_id_not_exists_existing(self):
        """When updating/deleting, ID must exist."""
        students = {}  # empty dictionary
        # For update/delete (is_new=False), missing ID should raise "No student with ID"
        with self.assertRaises(ValueError) as context:
            validation.validate_id(students, "101", False)
        self.assertIn("No student with ID", str(context.exception))

    def test_validate_name_valid(self):
        """Name should be stripped and title‑cased."""
        # Input with extra spaces becomes "John Doe"
        self.assertEqual(validation.validate_name("  john doe  "), "John Doe")

    def test_validate_name_empty(self):
        """Empty name should raise ValueError."""
        with self.assertRaises(ValueError):
            validation.validate_name("   ")  # only spaces

    def test_validate_phone_digits_only(self):
        """Phone should keep only digits."""
        # Removes non-digits: "77-88 99 00" -> "77889900"
        self.assertEqual(validation.validate_phone("77-88 99 00"), "77889900")

    def test_validate_phone_no_digits(self):
        """Phone without digits is invalid."""
        with self.assertRaises(ValueError):
            validation.validate_phone("abc")  # no digits at all

    def test_validate_grade_valid(self):
        """Valid grade between 0 and 100."""
        # Should convert string to float 85.5
        self.assertEqual(validation.validate_grade("85.5", "midterm"), 85.5)

    def test_validate_grade_out_of_range(self):
        """Grade outside 0‑100 raises error."""
        with self.assertRaises(ValueError):
            validation.validate_grade("120", "final")  # >100
        with self.assertRaises(ValueError):
            validation.validate_grade("-5", "midterm")  # <0


class TestRegistry(unittest.TestCase):
    """Test the registry functions that modify the student dictionary."""
    # This class tests the main registry operations: add, update, delete, search

    def setUp(self):
        """Create a fresh empty dictionary before each test."""
        # This runs before every test method, giving a clean student list
        self.students = {}

    @patch('builtins.input')
    def test_add_student_valid(self, mock_input):
        """Successfully add a student with valid data."""
        # Simulate user inputs: ID, name, phone, midterm grade, final grade
        mock_input.side_effect = ["101", "Alice Wonder", "5551234", "85", "90"]
        registry.add_student(self.students)
        # Check that student was added with correct data
        self.assertIn(101, self.students)
        self.assertEqual(self.students[101]["name"], "Alice Wonder")
        self.assertEqual(self.students[101]["phone"], "5551234")
        self.assertEqual(self.students[101]["midterm"], 85.0)
        self.assertEqual(self.students[101]["final"], 90.0)

    @patch('builtins.input')
    def test_add_student_duplicate_id(self, mock_input):
        """If ID already exists, user is asked again."""
        # Pre‑add a student with ID 101
        self.students[101] = {"name": "Existing", "phone": "111", "midterm": 70, "final": 80}
        # First input 101 (fails because duplicate), then 102 (works)
        mock_input.side_effect = ["101", "102", "Bob", "555", "75", "80"]
        registry.add_student(self.students)
        # Only student with ID 102 should be added
        self.assertIn(102, self.students)
        self.assertEqual(self.students[102]["name"], "Bob")

    @patch('builtins.input')
    def test_update_student_valid(self, mock_input):
        """Update a student field (name)."""
        # Existing student
        self.students[101] = {"name": "Alice", "phone": "111", "midterm": 70, "final": 80}
        # Inputs: ID, field choice (1 = name), new name
        mock_input.side_effect = ["101", "1", "Alice Wonder"]
        registry.update_student(self.students)
        # Name should be updated
        self.assertEqual(self.students[101]["name"], "Alice Wonder")

    @patch('builtins.input')
    def test_delete_student_valid(self, mock_input):
        """Delete an existing student with confirmation."""
        self.students[101] = {"name": "Alice", "phone": "111", "midterm": 70, "final": 80}
        mock_input.side_effect = ["101", "y"]  # confirm deletion
        registry.delete_student(self.students)
        self.assertNotIn(101, self.students)  # student removed

    @patch('builtins.input')
    def test_delete_student_not_found(self, mock_input):
        """Try to delete a non‑existent ID; operation is cancelled."""
        mock_input.side_effect = ["999", ""]  # invalid ID, then empty to cancel
        registry.delete_student(self.students)
        self.assertEqual(self.students, {})   # dictionary unchanged (still empty)

    @patch('builtins.input')
    def test_search_by_id_found(self, mock_input):
        """Search by ID should not crash when student exists."""
        self.students[101] = {"name": "Alice", "phone": "111", "midterm": 70, "final": 80}
        mock_input.side_effect = ["101"]
        # Just ensure no exception is raised (the function prints the student)
        registry.search_by_id(self.students)

    @patch('builtins.input')
    def test_search_by_name_partial(self, mock_input):
        """Search by name should find partial matches."""
        self.students[101] = {"name": "Alice Wonder", "phone": "111", "midterm": 70, "final": 80}
        self.students[102] = {"name": "Bob Wonder", "phone": "222", "midterm": 75, "final": 85}
        mock_input.side_effect = ["Wonder"]  # search for "Wonder"
        # Should print both students without error
        registry.search_by_name(self.students)

    def test_class_report_empty(self):
        """Class report should handle empty dictionary gracefully."""
        # Should print "No students registered." without raising an error
        report_utils.print_class_report(self.students)

    def test_class_report_non_empty(self):
        """Class report should compute statistics without errors."""
        self.students[101] = {"name": "Alice", "phone": "111", "midterm": 70, "final": 80}
        self.students[102] = {"name": "Bob", "phone": "222", "midterm": 85, "final": 90}
        # Should compute averages, min, max, etc. and print without crashing
        report_utils.print_class_report(self.students)


if __name__ == '__main__':
    unittest.main()  # Run all tests when this script is executed directly