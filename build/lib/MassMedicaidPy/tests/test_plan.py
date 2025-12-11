import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import plan from plan class
from Plan_Information.code_plan import Plan

"""
Test basic functionality
"""
def test_plan_creation_valid_program():
    # Test creating plan with valid program
    plan = Plan("Medicaid for Pregnant Women")
    assert plan is not None


def test_plan_creation_none():
    # Test creating plan with None 
    plan = Plan(None)
    assert plan is not None
    assert plan.get_plan() is None


"""
Test get_plan
"""

def test_get_plan_pregnant():
   # Test get_plan for pregnant women
    plan = Plan("Medicaid for Pregnant Women")
    assert plan.get_plan() == "MassHealth Standard"


def test_get_plan_chip():
    # Test get_plan for CHIP
    plan = Plan("Children's Separate CHIP")
    assert plan.get_plan() == "CHIP"


def test_get_plan_careplus():
    # Test get_plan for expansion adults
    plan = Plan("Medicaid Expansion for Adults")
    assert plan.get_plan() == "MassHealth CarePlus"


def test_get_plan_none():
    # Test get_plan returns None when not eligible
    plan = Plan(None)
    assert plan.get_plan() is None


"""
Test get_plan_details
"""

def test_plan_details_has_required_keys():
    # Test plan details has all required keys
    plan = Plan("Medicaid for Pregnant Women")
    details = plan.get_plan_details()
    
    assert "description" in details
    assert "coverage" in details
    assert "premium" in details
    assert "copay" in details
    assert "deductible" in details


def test_get_coverage():
    # Test get_coverage returns list
    plan = Plan("Medicaid for Pregnant Women")
    coverage = plan.get_coverage()
    assert isinstance(coverage, list)
    assert len(coverage) > 0

def test_has_premium():
    # Test has_premium
    plan = Plan("Medicaid for Preganant Women")
    assert plan.has_premium() == False
    plan2 = Plan("Medicaid Expansion for Adults")
    assert plan2.has_premium() == True

def test_has_deductible():
    # Test has_deductible
    plan = Plan("Medicaid for Pregnant Women")
    assert plan.has_deductible() == False

def test_get_summary():
    # Test get_summary returns complete plan info
    plan = Plan("Medicaid for Pregnant Women")
    summary = plan.get_summary()
    assert summary["eligible"] == True
    assert summary["plan"] == "MassHealth Standard"
    assert "coverage" in summary
    assert "premium" in summary
    assert "copay" in summary


def test_get_summary_not_eligible():
    plan = Plan(None)
    summary = plan.get_summary()
    
    assert summary["eligible"] == False
    assert summary["plan"] is None
"""
Test all work
"""

def test_all_programs_works():
    # Test all valid programs work
    programs = [
        "Children's Medicaid (0-1)",
        "Children's Medicaid (1-5)",
        "Children's Medicaid (6-18)",
        "Children's Separate CHIP",
        "Medicaid for Pregnant Women",
        "Medicaid for Parents/Caretakers",
        "Medicaid Expansion for Adults"
    ]
    
    for program in programs:
        plan = Plan(program)
        assert plan.get_plan() is not None
        assert plan.get_plan_details() is not None
        assert plan.get_coverage() is not None


