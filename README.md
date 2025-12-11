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

## Package Structure

### Assumptions

- The user using this is a U.S. Citizen/ Permenant Resident and a Massachussetts resident
- The user using this is an adult according to Massachussetts otherwise it does not process the results
- The dependents can be of any age 
- The age of the user and their dependents have is the year (not calculating for months and days)
- The dependents of the user live in the same household as the user using this package
- The dependents of the user have the same citizenship, state as the user
- Total income must be calculated and provided as total annual household income (users must calculate this themselves)
- The user is assumed to be the primary caretaker when dependents are present
- Federal Poverty Level (FPL) data is based on the 2024 guidelines so the threshold might change annually 

### 1. Household Information Module
Defines the main user-facing classes.

**Person**

Base class containing:
- Gender
- Citizenship
- Birthdate
- State
- Age-calculation and demographic helper methods

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
