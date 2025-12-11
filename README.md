# MassMedicaidPy

## Description 
MassMedicaidPy is a Python package that calculates Medicaid eligibility and possible health insurance plans for residents of Massachusetts. It evaluates demographic information, family structure, income, pregnancy status, disability, and other factors to determine the user's eligibility for various MassHealth programs.

## Motivation
Determining eligibility for public health insurance is often confusing, time-consuming and complicated. This package simplifies the process for Massachusetts users by providing clean class structures and automatic eligibility calculations based on real Federal Poverty Level standards.

## Intended Users
Low-income individuals and families in Massachusetts seeking to understand their Medicaid eligibility.

## Installation 
#### 1. Clone the repository
git clone https://github.com/radiah23/MassMedicaidPy.git

#### 2. Navigate into the project directory
cd /path/to/repo

#### 3. Install the package locally
pip install .




## Package structure
1. Household Information Module

Defines the main user-facing classes.
Person
Base class containing:Gender, Citizenship, Birthdate, State, Age-calculation and demographic helper methods

Individual (Subclass of Person)
Attributes: Disability status, Pregnancy status, Primary caretaker flag, Back-reference to the household, Dependent (Subclass of Person)

Dependents (spouse, child, or other related adult).
Attributes:Relationship to applicant, Optional disability/pregnancy indicators, Back-reference to household

Household
Represents a family unit applying for coverage.
Key functionality: Tracks household size, income, dependents
Identifies number of children/adults/seniors, Checks special conditions (pregnancy, disability), Connects to eligibility and plan modules, Provides get_eligibility_and_plans() to return unified results

2. Eligibility Module

Contains class:
MassHealthEligibilityChecker

This class:
Stores FPL values
Computes income thresholds using federal poverty percentages

Checks:
Residency in Massachusetts
Citizenship/permanent residency
Child eligibility by age group
Pregnancy eligibility
Parent/caretaker eligibility
Adult expansion eligibility

Returns a structured dictionary of eligibility results

3. Plan Module
Plan
Maps eligible programs to specific MassHealth plans:
Programs → Plans
Children’s Medicaid → MassHealth Standard
CHIP → CHIP
Adult expansion → MassHealth CarePlus

Provides:
Plan descriptions, Coverage details, Copay, premium, and deductible information
get_summary() method for a full plan overview
