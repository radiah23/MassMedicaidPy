import unittest
import sys
import os
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Household_Information.code_household import Household, Individual, Dependent, Person


class TestPerson(unittest.TestCase):

    def test_calculate_age_valid(self):
        person = Person("Female", "US Citizen", "2004-05-05", "MA")

        today = date.today()
        birth_year = 2004
        birth_month = 5
        birth_day = 5

        age_expected = today.year - birth_year - (
            (today.month, today.day) < (birth_month, birth_day)
        )

        self.assertEqual(person.calculate_age(), age_expected)

    def test_calculate_age_not_valid(self):
        person = Person("Female", "US Citizen", "2029-05-05", "MA")
        with self.assertRaises(ValueError):
            person.calculate_age()

    def test_child_true(self):
        person = Person("Female", "US Citizen", "2022-05-05", "MA")
        self.assertTrue(person.is_child_acc_to_mass())

    def test_child_false(self):
        person = Person("Female", "US Citizen", "2000-05-05", "MA")
        self.assertFalse(person.is_child_acc_to_mass())

    def test_senior_true(self):
        person = Person("Female", "US Citizen", "1900-05-05", "MA")
        self.assertTrue(person.is_senior_acc_to_mass())

    def test_senior_false(self):
        person = Person("Female", "US Citizen", "2000-05-05", "MA")
        self.assertFalse(person.is_senior_acc_to_mass())

    def test_adult_false(self):
        # senior should return False for adult according to your rules
        person = Person("Female", "US Citizen", "1900-05-05", "MA")
        self.assertFalse(person.is_adult())

    def test_adult_true(self):
        person = Person("Female", "US Citizen", "2000-05-05", "MA")
        self.assertTrue(person.is_adult())


class TestHousehold(unittest.TestCase):

    def setUp(self):

        self.primary = Individual(
            gender="Female",
            citizenship="US Citizen",
            birthdate="1995-06-10",
            state="Massachusetts",
            disability_status=False,
            pregnancy_status=False,
            is_primary_caretaker=True
        )

        self.child1 = Dependent(
            gender="Male",
            citizenship="US Citizen",
            birthdate="2018-03-20",
            state="Massachusetts",
            relationship_to_the_applicant="Child",
            disability_status=False,
            pregnancy_status=False
        )

        self.child2 = Dependent(
            gender="Female",
            citizenship="US Citizen",
            birthdate="2025-05-20",
            state="Massachusetts",
            relationship_to_the_applicant="Child",
            disability_status=False,
            pregnancy_status=False
        )

        self.senior1 = Dependent(
            gender="Female",
            citizenship="US Citizen",
            birthdate="1960-05-20",
            state="Massachusetts",
            relationship_to_the_applicant="Child",
            disability_status=False,
            pregnancy_status=False
        )

        self.disabled1 = Dependent(
            gender="Female",
            citizenship="US Citizen",
            birthdate="1960-05-20",
            state="Massachusetts",
            relationship_to_the_applicant="Child",
            disability_status=True,
            pregnancy_status=False
        )

        self.pregnant1 = Dependent(
            gender="Female",
            citizenship="US Citizen",
            birthdate="1960-05-20",
            state="Massachusetts",
            relationship_to_the_applicant="Child",
            disability_status=False,
            pregnancy_status=True
        )

        self.household1 = Household(
            self.primary,
            [self.child1, self.child2, self.pregnant1, self.disabled1, self.senior1],10000.00
        )

        self.household2 = Household(self.primary,[],10000.00)

    def test_get_income(self):
        self.assertEqual(self.household1.get_income(), 10000.00)

    def test_household_size_with_zero_dependents(self):
        self.assertEqual(self.household2.household_size(), 1)

    def test_household_size_with_dependents(self):
        self.assertEqual(self.household1.household_size(), 6)

    def test_dependent_count(self):
        self.assertEqual(self.household1.dependent_count(), 5)

    def test_no_dependent_count(self):
        self.assertEqual(self.household2.dependent_count(), 0)

    def test_has_pregnancy(self):
        self.assertTrue(self.household1.has_pregnancy())

    def test_has_no_pregnancy(self):
        self.assertFalse(self.household2.has_pregnancy())

    def test_has_disabled_member(self):
        self.assertTrue(self.household1.has_disabled_member())

    def test_has_no_disabled_member(self):
        self.assertFalse(self.household2.has_disabled_member())

    def test_has_seniors(self):
        self.assertTrue(self.household1.has_seniors())

    def test_get_seniors(self):
        self.assertEqual(self.household1.get_seniors(), 3)

    def test_has_no_seniors(self):
        self.assertFalse(self.household2.has_seniors())

    def test_get_adults(self):
        self.assertEqual(self.household2.get_adults(), 1)

    def test_is_parent(self):
        self.assertFalse(self.household2.is_parent())

    def test_get_children(self):
        self.assertEqual(self.household1.get_children(), 2)

    def test_add_dependents(self):
        household3 = Household(self.primary, [self.child2], 50000.0)
        household3.add_dependent(self.disabled1)
        self.assertEqual(household3.dependent_count(), 2)
