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


    plan_checker = Plan(
        program=eligibility.get("program"),
        family_size=household.household_size(),
        age=household.primary_applicant.calculate_age(),
        annual_income=household.get_income(),
        is_pregnant=household.has_pregnancy(),
        is_parent=household.is_parent(),
        is_disabled=household.has_disabled_member(),
        citizenship_eligibility=household.primary_applicant.citizenship
    )

    return {
        "eligible": eligibility.get("eligible"),
        "eligible_plans": plan_checker.eligible_plans()
    }


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
