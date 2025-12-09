import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from Household_Information.code_household import Individual, Dependent, Household
from Condition_Information.code_condition import MassHealthEligibilityChecker
from Plan_Information.code_plan import Plan
individual_data = {
    "gender": "Female",
    "citizenship": "US Citizen",
    "birthdate": "1995-06-10",
    "state": "Massachusetts",
    "disability_status": False,
    "pregnancy_status": True,
    "is_primary_caretaker": True
}

dependents_data = [
    {
        "gender": "Male",
        "citizenship": "US Citizen",
        "birthdate": "2018-03-20",
        "state": "Massachusetts",
        "relationship_to_the_applicant": "Child",
        "disability_status": False,
        "pregnancy_status": False,
        "has_special_status": False
    }
]

total_income = 25000


import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from Household_Information.code_household import Individual, Dependent, Household
from Condition_Information.code_condition import MassHealthEligibilityChecker
from Plan_Information.code_plan import Plan

individual_data = {
    "gender": "Female",
    "citizenship": "US Citizen",
    "birthdate": "1995-06-10",
    "state": "California",
    "disability_status": False,
    "pregnancy_status": True,
    "is_primary_caretaker": True
}

dependents_data = [
    {
        "gender": "Male",
        "citizenship": "US Citizen",
        "birthdate": "2003-03-20",
        "state": "California",
        "relationship_to_the_applicant": "Child",
        "disability_status": False,
        "pregnancy_status": False
    }
]

total_income = 25000


#Ask Professor Gillian on how to run it or combine it 
individual = Individual(**individual_data)
dependents = [Dependent(**dep) for dep in dependents_data]
household = Household(individual, dependents, total_income)


result = household.get_eligibility_and_plans()


# ✅ PRINT RESULT
print("\n✅ TEST RESULT:")
print(result)
