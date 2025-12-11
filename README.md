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

### Assumptions

- The user using this is a U.S. Citizen/ Permenant Resident and a Massachussetts resident
- The user using this is an adult according to Massachussetts otherwise it does not process the results
- The dependents can be of any age 
- The age of the user and their dependents have is the year (not calculating for months and days)
- The dependents of the user needs to live in the same household as the user using this package, error in results otherwise.
- The dependents of the user have the same citizenship, state as the user
- Total income must be calculated and provided as total annual household income (users must calculate this themselves)
- Total yearly income must be in USD 
- The user is assumed to be the primary caretaker when dependents are present
- Federal Poverty Level (FPL) data is based on the 2024 guidelines so the threshold might change annually
- Relationship types for dependents are limited to "Spouse", "Child", or "Adult-Related-Dependent" and it does not account for any other relationship. Throws an error if you try to input any other types.
- The package assumes standard MassHealth program categories and does not account for special circumstances or waiver programs
- Does not provide enrollment assistance or next steps after determining eligibility
- Gender must be one of the options :  [Male, Female, Prefer not to Disclose] for the sake of the project scope. 

### 1. Household Information Module
Defines the main user-facing classes.

**Person**

Base class contains : `Gender`, `Citizenship`, `Birthdate` `State`

**Individual (Subclass of Person)**

Attributes:
- Disability status
- Pregnancy status
- Primary caretaker flag
- Back-reference to the household

**Dependent (Subclass of Person)**

Dependents (spouse, child, or other related adult).

Attributes:
- Relationship to applicant
- Optional disability/pregnancy indicators
- Back-reference to household

**Household**

Represents a family unit applying for coverage.

Key functionality:
- Tracks household size, income, dependents
- Identifies number of children/adults/seniors
- Checks special conditions (pregnancy, disability)
- Connects to eligibility and plan modules
- Provides `get_eligibility_and_plans()` to return unified results

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
