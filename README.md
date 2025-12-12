# MassMedicaidPy
## Description 
MassMedicaidPy is a Python package that calculates Medicaid eligibility and possible health insurance plans for residents of Massachusetts. It evaluates demographic information, family structure, income, pregnancy status, disability, and other factors to determine the user's eligibility for various MassHealth programs.

## Motivation
Determining eligibility for public health insurance is often confusing, time-consuming and complicated. This package simplifies the process for Massachusetts users by providing clean class structures and automatic eligibility calculations based on real Federal Poverty Level standards.

## Intended Users
Low-income individuals and families in Massachusetts seeking to understand their Medicaid eligibility.

## Installation 

#### 1. Clone the repository
```
git clone https://github.com/radiah23/MassMedicaidPy.git
```

#### 2. Navigate into the project directory
```
cd /path/to/repo
```

#### 3. Install the package locally
```
pip install .
```


## Dependencies of the Package 

This package requires:
- Python >= 3.9 version
- No external dependencies are needed (We use the standard library of python) 
All required modules (`datetime`, `typing`) are included in Python's standard library.


## Package Structure

### Assumptions of all the modules

- Primary applicant be a U.S. Citizen or Permanent Resident
- Primary applicant  be a Massachusetts resident
- Primary applicant  be 19 years or older (adults only) - otherwise the package will not process results
- Primary applicant is assumed to be the primary caretaker when dependents are present
- Dependents can be of any age
- Dependents live in the same household as the primary applicant (error in results otherwise)
- Dependents have the same citizenship and state as the primary applicant
- Total income must be calculated and provided as total annual household income in USD
- Users must calculate their household income themselves before using the package
- Birthdates must be provided in 'YYYY-MM-DD' format
- Birthdates cannot be in the future. Throws an error if input by the user.
- Age calculations are based on years only
- Gender must be one of: "Male", "Female", or "Prefer not to Disclose"
- Relationship types for dependents are limited to: "Spouse", "Child", or "Adult-Related-Dependent" (throws an error for other types)
- Disability and pregnancy status are boolean (True/False) values only
- Federal Poverty Level (FPL) data is based on 2024 guidelines (thresholds may change annually and require package updates)
- The package assumes standard MassHealth program categories and does not account for special circumstances or waiver programs
- Income eligibility is based solely on Federal Poverty Level percentages.



### 1. Household Information Module
Defines the main user-facing classes.

**Person**

Base class contains : `Gender`, `Citizenship`, `Birthdate` `State`

Methods contain :

`calculate_age` : Calculates the person object's age from their birthdate (the year
`is_child_acc_to_mass`, `is_adult `, `is_senior_acc_to_mass` : All of the methods check if the person object is a child, adult or senior

**Individual (Subclass of Person)**

Attributes: `Disability_status`, `pregnancy_status`, `is_primary_caretaker` : All of the attributes have `True/False` boolean values 
Always assumes they are primary caretaker. 

**Dependent (Subclass of Person)**

Attributes: `Disability_status`, `pregnancy_status`,`Relationship_to_applicant` 
Relationship to the primary applicant can be only one of these options `spouse, child, or other related adult`

**Household**

** Attributes:** 
`primary_applicant` - Individual object
`dependent_list` - List of Dependent objects living in the household
- `total_income` - Total annual household income in USD

** Functionality:**
- Connects primary applicant and dependents 
- Tracks household size, income, and all dependents
- Identifies number of children/adults/seniors in the household
- Checks for special conditions (pregnancy, disability) across all memberss

** Methods:**
- `get_income()` - Returns total household income
- `household_size()` - Returns total number of people in household
- `dependent_count()` - Returns number of dependents
- `get_children()` - Returns number of children (under 19)
- `get_adults()` - Returns number of adults (19-64)
- `get_seniors()` - Returns number of seniors (65+)
- `is_parent()` - Checks if primary applicant has children
- `has_pregnancy()` - Checks if any household member is pregnant
- `has_disabled_member()` - Checks if any household member has a disability
- `has_seniors()` - Checks if household includes seniors
- `add_dependent()` - Adds a new dependent to the household


### 2. Eligibility Module
Contains class:

**MassHealthEligibilityChecker**

This class:
- Stores FPL values
- Computes income thresholds using federal poverty percentages
- Checks:
  - Residency in Massachusetts
  - Citizenship/permanent residency
  - Child eligibility by age group
  - Pregnancy eligibility
  - Parent/caretaker eligibility
  - Adult expansion eligibility
- Returns a structured dictionary of eligibility results

### 3. Plan Module

**Plan**

Maps eligible programs to specific MassHealth plans:

Programs → Plans
- Children's Medicaid → MassHealth Standard
- CHIP → CHIP
- Adult expansion → MassHealth CarePlus

Provides:
- Plan descriptions
- Coverage details
- Copay, premium, and deductible information
- `get_summary()` method for a full plan overview


## Example Usage

After you are done installing it: 

```python
from MassMedicaidPy.Household_Information.code_household import Individual,Person,Household
from MassMedicaidPy.Plan_Information.code_plan import Plan
from MassMedicaidPy.Condition_Information.code_condition import MassHealthEligibilityChecker
from MassMedicaidPy.results_info.results import get_household_eligibility, print_all

# Define the user (Primary Applicant)
individual_data = {
    "gender": "Female",
    "citizenship": "US Citizen",
    "birthdate": "1995-06-10",
    "state": "Massachusetts",
    "disability_status": False,
    "pregnancy_status": True,
    "is_primary_caretaker": True 
}

# Define the dependents of the user
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

# Check eligibility
results = get_household_eligibility(individual_data, dependents_data, total_income=25000)
print_all(results)
```

For more detailed examples, see the `example.ipynb` notebook in the repository.


## Testing

To run the test suite:

```
cd /path/to/repo
```
```
pytest tests/
```

All tests should pass and the tests include unit tests for all the functions in the `Household`, `Individual`, `Person`, `Dependent`, `Condition`, `Plan`


## **Contributors:**
- Danyi Xu
- Xinxin Zhang
- Radiah Khan

## Acknowledgments

- Federal Poverty Level data from [HHS.gov](https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines)
- MassHealth program information from [Mass.gov](https://www.mass.gov/masshealth)
- Developed for SDS 271: Advanced Programming for Data Science at Smith College
- Special thanks to Professor Gillian Beltz-Mohrmann for all the support!
