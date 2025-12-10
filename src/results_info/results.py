import sys
import os

# Add src folder to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Household_Information.code_household import Individual, Dependent, Household
from Condition_Information.code_condition import MassHealthEligibilityChecker
from Plan_Information.code_plan import Plan


def get_eligibility_and_plans(primary_applicant, dependent_list, total_income):

    if not isinstance(primary_applicant, dict):
        raise TypeError("primary_applicant must be a dictionary")
    if not isinstance(dependent_list, list):
        raise TypeError("dependent_list must be a list of dictionaries")

    primary = Individual(
        gender=primary_applicant["gender"],
        citizenship=primary_applicant["citizenship"],
        birthdate=primary_applicant["birthdate"],
        state=primary_applicant["state"],
        disability_status=primary_applicant["disability_status"],
        pregnancy_status=primary_applicant["pregnancy_status"],
        is_primary_caretaker=primary_applicant["is_primary_caretaker"]
    )

    dependents = [
        Dependent(
            gender=dependent["gender"],
            citizenship=dependent["citizenship"],
            birthdate=dependent["birthdate"],
            state=dependent["state"],
            relationship_to_the_applicant=dependent["relationship_to_the_applicant"],
            disability_status=dependent["disability_status"],
            pregnancy_status=dependent["pregnancy_status"]
        )
        for dependent in dependent_list
    ]

    household = Household(
        primary_applicant=primary,
        dependent_list=dependents,
        total_income=total_income
    )
    checker = MassHealthEligibilityChecker()
    eligibility = checker.check_household_eligibility(household)

    if eligibility.get("eligible"):
        plan_checker = Plan(program=eligibility.get("program"))
        
        result = {
            "eligible": True,
            "program": eligibility.get("program"),
            "plan": plan_checker.get_plan(),
            "plan_details": plan_checker.get_plan_details(),
            "has_premium": plan_checker.has_premium(),
            "has_deductible": plan_checker.has_deductible(),
            "coverage": plan_checker.get_coverage(),
            # Include household info here if needed
            "family_size": household.household_size(),
            "annual_income": household.get_income(),
        }
    else:
        result = {
            "eligible": False,
            "program": eligibility.get("program"),
            "reason": eligibility.get("reason"),
            "message": eligibility.get("message"),
            "plan": None,
            "family_size": household.household_size(),
            "annual_income": household.get_income(),
        }
    
    return result


#Test the information

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
        "pregnancy_status": False
    }
]
total_income = 25000

result = get_eligibility_and_plans(individual_data, dependents_data, total_income)
print(result)

if result['eligible']:
        print(f"ELIGIBLE")
        print(f"Program: {result['program']}")
        print(f"Plan: {result['plan']}")
        print(f"Family Size: {result['family_size']}")
        print(f"Annual Income: ${result['annual_income']}")
        
        details = result['plan_details']
        print(f"\nDescription: {details['description']}")
        print(f"Coverage: {', '.join(details['coverage'])}")
        print(f"Copay: {details['copay']}")
        print(f"Premium: {details['premium']}")
        print(f"Deductible: {details['deductible']}")
else:
        print(f"NOT ELIGIBLE")
        print(f"Reason: {result['reason']}")
        print(f"Message: {result['message']}")