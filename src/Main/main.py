from datetime import date
from Household_Information import Individual, Dependent, Household
from Condition_Information import MassHealthEligibilityChecker
from Plan_Information import Plan 

def main(individual_data: dict, dependents_data: list[dict], total_income: float) -> dict:
    household = household_infos(individual_data, dependents_data, total_income)

    eligibility = MassHealthEligibilityChecker(household)
    plans = run_plan_check(household, eligibility)

    return {
        "eligibility": eligibility,
        "household_size": household.household_size,
        "eligible_plans": plans
    }






