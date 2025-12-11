import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MassMedicaidPy')))

def test_medicaid():
    from Condition_Information.code_condition import MassHealthEligibilityChecker
    from Household_Information.code_household import Person, Household
    from datetime import date

    checker = MassHealthEligibilityChecker()

    
    birthdate = date.today().replace(year=date.today().year - 3)
    person = Person(
        gender="Male",
        citizenship="US Citizen",
        birthdate=birthdate,
        state="Massachusetts"
    )

    household = Household(primary_applicant=person, dependent_list=[])

    eligibility = checker.check_household_eligibility(household)
    assert eligibility["eligible"] is True

    result = checker.check_eligibility(
        age=person.calculate_age(),
        annual_income=20000,
        family_size=1
    )

    assert result["eligible"] is True
    assert "Children" in result["program"]
