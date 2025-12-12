import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Household_Information.code_household import Person, Individual, Household
from Condition_Information.code_condition import MassHealthEligibilityChecker

"""
Test basic functionality
"""

def test_checker_creation():
    # Test creating MassHealthEligibilityChecker
    checker = MassHealthEligibilityChecker()
    assert checker is not None
    assert hasattr(checker, 'annual_fpl')
    assert hasattr(checker, 'eligibility_standards')


def test_checker_has_fpl_data():
    # Test that FPL data is loaded correctly
    checker = MassHealthEligibilityChecker()
    assert len(checker.annual_fpl) == 8
    assert checker.annual_fpl[1] == 15660
    assert checker.annual_fpl[4] == 32160


def test_checker_has_eligibility_standards():
    # Test that eligibility standards are loaded correctly
    checker = MassHealthEligibilityChecker()
    assert 'children_0_1' in checker.eligibility_standards
    assert 'expansion_adults' in checker.eligibility_standards
    assert checker.eligibility_standards['children_0_1'] == 2.00


"""
Test regional_belonging
"""

def test_regional_belonging_massachusetts():
    # Test for Massachusetts resident
    checker = MassHealthEligibilityChecker()
    
    person = Person("Male", "US Citizen", "2000-01-01", "Massachusetts")
    
    result = checker.regional_belonging(person)
    assert result == "Massachusetts"


def test_regional_belonging_other_state():
    # Test for non-Massachusetts resident
    checker = MassHealthEligibilityChecker()
    
    person = Person("Female", "US Citizen", "1990-01-01", "California")
    
    result = checker.regional_belonging(person)
    assert result == "You might need to consider federal medicare options or your state options"


"""
Test citizenship_eligibility
"""

def test_citizenship_us_citizen():
    # Test for US Citizen
    checker = MassHealthEligibilityChecker()
    
    person = Person("Male", "US Citizen", "2000-01-01", "Massachusetts")
    
    result = checker.citizenship_eligibility(person)
    assert result == "US Citizen"


def test_citizenship_permanent_residency():
    # Test for Permanent Residency
    checker = MassHealthEligibilityChecker()
    
    person = Person("Female", "Permanent Residency", "1995-01-01", "Massachusetts")
    
    result = checker.citizenship_eligibility(person)
    assert result == "Permanent Residency"


def test_citizenship_other():
    # Test for other citizenship status
    checker = MassHealthEligibilityChecker()
    
    person = Person("Male", "Other", "2000-01-01", "Massachusetts")
    
    result = checker.citizenship_eligibility(person)
    assert result == "Sorry, there are other eligible international insurance options for you."


"""
Test calculate_annual_fpl
"""

def test_calculate_annual_fpl_small_families():
    # Test FPL calculation for family sizes 1-8
    checker = MassHealthEligibilityChecker()
    
    assert checker.calculate_annual_fpl(1) == 15660
    assert checker.calculate_annual_fpl(2) == 21156
    assert checker.calculate_annual_fpl(4) == 32160
    assert checker.calculate_annual_fpl(8) == 54156


def test_calculate_annual_fpl_large_families():
    # Test FPL calculation for family sizes > 8
    checker = MassHealthEligibilityChecker()
    
    # Family of 9: 54156 + 5508 = 59664
    assert checker.calculate_annual_fpl(9) == 59664
    
    # Family of 10: 54156 + (2 * 5508) = 65172
    assert checker.calculate_annual_fpl(10) == 65172
    
    # Family of 12: 54156 + (4 * 5508) = 76188
    assert checker.calculate_annual_fpl(12) == 76188


def test_calculate_annual_fpl_invalid():
    # Test FPL calculation with invalid family size
    checker = MassHealthEligibilityChecker()
    
    # Should return ValueError for family size <= 0
    result = checker.calculate_annual_fpl(0)
    assert result == ValueError


"""
Test get_annual_income_limit
"""

def test_get_annual_income_limit_valid():
    # Test income limit calculation for valid categories
    checker = MassHealthEligibilityChecker()
    
    # Test for children_0_1 (200% of FPL)
    limit = checker.get_annual_income_limit('children_0_1', 2)
    fpl = checker.calculate_annual_fpl(2)  # 21156
    expected = fpl * 2.00  # 42312
    assert limit == expected
    
    # Test for expansion_adults (133% of FPL)
    limit = checker.get_annual_income_limit('expansion_adults', 3)
    fpl = checker.calculate_annual_fpl(3)  # 26652
    expected = fpl * 1.33
    assert limit == expected


def test_get_annual_income_limit_invalid_category():
    # Test income limit calculation with invalid category
    checker = MassHealthEligibilityChecker()
    
    result = checker.get_annual_income_limit('invalid_category', 2)
    assert result == ValueError


"""
Test check_eligibility for children
"""

def test_check_eligibility_infant_eligible():
    # Test eligible infant (0-1 years)
    checker = MassHealthEligibilityChecker()
    
    results = checker.check_eligibility(
        age=0,
        annual_income=20000,
        family_size=2
    )
    
    assert results['eligible'] == True
    assert "Children's Medicaid" in results['program']
    assert results['is_chip'] == False
    assert results['family_size'] == 2


def test_check_eligibility_child_eligible_medicaid():
    # Test eligible child (1-5 years) for Medicaid
    checker = MassHealthEligibilityChecker()
    
    results = checker.check_eligibility(
        age=3,
        annual_income=25000,
        family_size=3
    )
    
    assert results['eligible'] == True
    assert "Children's Medicaid" in results['program']
    assert results['is_chip'] == False


def test_check_eligibility_child_chip_eligible():
    # Test child eligible for CHIP (higher income)
    checker = MassHealthEligibilityChecker()
    
    results = checker.check_eligibility(
        age=10,
        annual_income=70000,
        family_size=4
    )
    
    assert results['eligible'] == True
    assert "CHIP" in results['program']
    assert results['is_chip'] == True


def test_check_eligibility_child_not_eligible():
    # Test child not eligible (income too high)
    checker = MassHealthEligibilityChecker()
    
    results = checker.check_eligibility(
        age=15,
        annual_income=100000,
        family_size=3
    )
    
    assert results['eligible'] == False
    assert results['program'] is None
    assert results['is_chip'] == False


"""
Test check_eligibility for pregnant women
"""

def test_check_eligibility_pregnant_eligible():
    # Test eligible pregnant woman
    checker = MassHealthEligibilityChecker()
    
    results = checker.check_eligibility(
        age=25,
        annual_income=40000,
        family_size=2,
        is_pregnant=True
    )
    
    assert results['eligible'] == True
    assert "Pregnant Women" in results['program']
    assert results['family_size'] == 2


def test_check_eligibility_pregnant_not_eligible():
    # Test pregnant woman not eligible (income too high)
    checker = MassHealthEligibilityChecker()
    
    results = checker.check_eligibility(
        age=30,
        annual_income=80000,
        family_size=2,
        is_pregnant=True
    )
    
    assert results['eligible'] == False


"""
Test check_eligibility for adults
"""

def test_check_eligibility_parent_eligible():
    # Test eligible parent
    checker = MassHealthEligibilityChecker()
    
    results = checker.check_eligibility(
        age=35,
        annual_income=30000,
        family_size=4,
        is_parent=True
    )
    
    assert results['eligible'] == True