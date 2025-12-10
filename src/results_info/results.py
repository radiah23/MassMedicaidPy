import sys
import os

# Add src folder to Python path
# Added this because of importing issues
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Household_Information.code_household import Individual, Dependent, Household
from Condition_Information.code_condition import MassHealthEligibilityChecker
from Plan_Information.code_plan import Plan


def get_household_eligibility(primary_applicant, dependent_list, total_income):

    """
    Check eligibility for the entire household
    
    :param primary_applicant: Primary applicant for the household
    :param dependent_list: Dependent(s) of the household
    :param total_income: Total household income
    """

    if not isinstance(primary_applicant, dict):
        raise TypeError("primary_applicant must be a dictionary")
    if not isinstance(dependent_list, list):
        raise TypeError("dependent_list must be a list of dictionaries")
    
    # Create primary applicant(individual) and dependents objects
   
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
    # Create household object that contains primary and dependent info, as well as total income
    household = Household(
        primary_applicant=primary,
        dependent_list=dependents,
        total_income=total_income
    )

    # Call eligibility checker from condition class
    checker = MassHealthEligibilityChecker()

    # Create a results dictionary that contained household info, family size, and total income,
    #  also a list that contains all the members
    results = {
            "household_info": {
            "family_size": household.household_size(),
            "total_income": household.get_income(),
            "members": []
        }
    }
    # First, check the initial eligibilty of the entire household
    # which is that primary applicant has to meet the residency and citizenship criterias
    household_validation = checker.check_household_eligibility(household)
    # If not, we will return not eligible and the reason
    if not household_validation.get("eligible"):
         return {
              "household_info":{
                   "family_size": household.household_size(),
                   "total_income": household.get_income(),
                   
              },
              "eligible": False,
              "reason": household_validation.get('reason'),
              "message": household_validation.get('message')
         }
    
    # If household eligibility passes, check eligibility of the primary applicant
    primary_eligibility = checker.check_eligibility(
         age = primary.calculate_age(),
         annual_income=household.get_income(),
         family_size=household.household_size(),
         is_pregnant=primary.pregnancy_status,
         is_parent=household.is_parent()
    )
    # Return result from primary applicant check
    primary_result= {
        "type": "Primary Applicant",
        "name": "Primary Applicant",  
        "age" : primary.calculate_age(),
        "gender" : primary.gender,
        "citizenship": primary.citizenship,
        "eligible": primary_eligibility.get('eligible'),
        "program": primary_eligibility.get('program'),
        "plan": None,
        "plan_details": None,
        "fpl_percentage": primary_eligibility.get('fpl_percentage')
    }
    # Return plan and plan details if primary applicant is eligible
    if primary_result["eligible"]:
        plan = Plan(program=primary_eligibility.get('program'))  
        primary_result['plan'] = plan.get_plan()
        primary_result['plan_details'] = plan.get_plan_details()
    
    results['household_info']['members'].append(primary_result)

    # A for loop that loop within the dependent lists that check the eligibility of each of them
    for i, dependent in enumerate(dependents):
        dependent_eligibility = checker.check_eligibility(
            age=dependent.calculate_age(),
            annual_income=household.get_income(),
            family_size=household.household_size(),
            is_pregnant=dependent.pregnancy_status,
            is_parent=False      
        )
    # Return eligibility result for dependent
        dependent_result = {
            "type": "Dependent",
            "name": f"Dependent {i+1}",
            "relationship": dependent.relationship_to_the_applicant,
            "age": dependent.calculate_age(),
            "gender": dependent.gender,
            "citizenship": dependent.citizenship,
            "eligible": dependent_eligibility.get('eligible'),
            "program": dependent_eligibility.get('program'),
            "plan": None,
            "plan_details": None,
            "fpl_percentage": dependent_eligibility.get('fpl_percentage')
        }
    # Return plan results for dependent if eligible
        if dependent_result["eligible"]:
            plan = Plan(program=dependent_eligibility.get('program'))
            dependent_result['plan'] = plan.get_plan()
            dependent_result['plan_details'] = plan.get_plan_details()
        results['household_info']['members'].append(dependent_result)
             
    
    return results

def print_all(results):
     """
     Prints out eligibility and eligible plans for all household members seperately by primary applicants and dependents
     
     :param results: Returned results from previous function
     """
     if not results.get('household_info') or not results.get('eligible', True):
        print("\n" + "="*50)
        print("Eligibility Results:")
        print(f"\nHousehold Information:")
        print(f"Family Size:  {results['household_info']['family_size']}" )
        print(f"Total annual income: {results['household_info']['total_income']}" )
        print(f"\nStatus: NOT ELIGIBLE")
        print(f"Reason: {results.get('reason')}")
        print(f"Message: {results.get('message')}")
        print("\n" + "="*50)
        return
     
    
     # Print out resutls if household is eligible
     household = results['household_info']
     print("\n" + "="*70)
     print("Eligibility Results:")

     print(f"\nFamily Size: {household['family_size']}")
     print(f"Annual Income: ${household['total_income']:,.2f}\n")
    
    # Print each member
     for member in household['members']:
        
        # Member header
        # Print relationship with individual if member is a dependent
        print("-" * 50)
        print(f"{member['name']} | Age {member['age']} | {member['gender']}")
        if member['type'] == 'Dependent':
            print(f"Relationship: {member['relationship']}")
        print("-" * 50)
        
        # Eligibility status
        if member['eligible']:
            print(f"ELIGIBLE - {member['program']}")
            print(f"  Plan: {member['plan']}")
            print(f"  FPL: {member['fpl_percentage']}%")
            
            # Plan details
            if member['plan_details']:
                details = member['plan_details']
                print(f"  Coverage: {', '.join(details['coverage'])}")
                print(f"  Copay: {details['copay']}")
                print(f"  Premium: {details['premium']}")
                print(f"  Deductible: {details['deductible']}")
        else:
            print(f"NOT ELIGIBLE")
        
        print()
    
     print("="*70 + "\n")



     

#Test 1 

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

result_test1 = get_household_eligibility(individual_data, dependents_data, total_income)
print_all(result_test1)

# Test 2 - Non-US citizenship
individual_data = {
    "gender": "Female",
    "citizenship": "China",
    "birthdate": "2002-06-10",
    "state": "Massachusetts",
    "disability_status": False,
    "pregnancy_status": False,
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
total_income = 40000

result_test2 = get_household_eligibility(individual_data, dependents_data, total_income)
print_all(result_test2)

# Test 3 - Non-massachusetts resident, no dependent
individual_data = {
    "gender": "Female",
    "citizenship": "US Citizen",
    "birthdate": "2002-06-10",
    "state": "Calfornia",
    "disability_status": False,
    "pregnancy_status": False,
    "is_primary_caretaker": False
}
dependents_data = []

total_income = 40000

result_test3 = get_household_eligibility(individual_data, dependents_data, total_income)
print_all(result_test3)


# Returns value error

# Test 4, relatively high income family with two kids
individual_data = {
    "gender": "Female",
    "citizenship": "US Citizen",
    "birthdate": "1995-06-10",
    "state": "Massachusetts",
    "disability_status": False,
    "pregnancy_status": False,
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
    },
    {
         "gender": "Female",
        "citizenship": "US Citizen",
        "birthdate": "2025-05-20",
        "state": "Massachusetts",
        "relationship_to_the_applicant": "Child",
        "disability_status": False,
        "pregnancy_status": False
    }
]
total_income = 50000

result_test4 = get_household_eligibility(individual_data, dependents_data, total_income)
print_all(result_test4)

