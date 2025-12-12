from __future__ import annotations
from typing import List

class Plan:
   
    """
    
    ------------------------------------------------------------------------------------------------------------------------------------------
        Attributes:

        program                    String
                                   The program people are assigned in the previous condition class
   ----------------------------------------------------------------------------------------------------------------------------------------------
    Methods : 
        get_plan(self)             Dictionary
                                   Returns plan based on the person's program
                                   
        get_plan_details(self)     Dictionary
                                   Returns Dictionary containing details
        
        get_description(self)      String
                                   Returns string that describes who the plan is for                          
        
        get_coverage(self)         List 
                                   Returns a list of coverages of the plan

        get_copay(self)            String
                                   Returns copay informaton of the plan
        
        has_premium(self)          Boolean
                                   Returns whether the plan has premium

        has_deductible(self)       Boolean
                                   Returns whether the plan has deductible 

        get_summary(self)          Dictionary
                                   Returns a summary dictionary containing all the information above 
    --------------------------------------------------------------------------------------------------------------------------------------------------
 """    
   
    # First match programs defined in condition class to plans through a dictionary
    program_to_plans = {
        "Children's Medicaid (0-1)": "MassHealth Standard",
        "Children's Medicaid (1-5)": "MassHealth Standard",
        "Children's Medicaid (6-18)": "MassHealth Standard",
        "Children's Separate CHIP": "CHIP",
        "Medicaid for Pregnant Women": "MassHealth Standard",
        "Medicaid for Parents/Caretakers": "MassHealth Standard",
        "Medicaid Expansion for Adults": "MassHealth CarePlus",
    }
    # Plan details including description, coverage, copay, premium, and deductibles
    plans = {
        "MassHealth Standard": {
            "description": "For children, pregnant women, and parents/caretakers",
            "coverage": ["Full medical", "Dental", "Mental health", "Long-term care"],
            "copay": "Low or none",
            "premium": "No premium",
            "deductible": "No deductible",
        },
        "MassHealth CarePlus": {
            "description": "For working adults without children",
            "coverage": ["Doctor visits", "Hospital care", "Limited long-term care"],
            "copay": "Variable",
            "premium": "Based on income",
            "deductible": "Yes",
        },
        "CHIP": {
            "description": "Children's Health Insurance Program for higher-income families",
            "coverage": ["Similar to Standard for children", "Dental", "Vision"],
            "copay": "Low copay",
            "premium": "Low monthly premium",
            "deductible": "Low or none",
        },
    }

    def __init__(self, program):
        self.program = program
    
    """
        Get plans'names
        Returns string from the program_to_sting dic
    """
    def get_plan(self):
       
        if self.program is None:
            return None
        
        return self.program_to_plans.get(self.program)
    """
        Get plans' details
        Returns dictionary from the plans dictionary
    """
    def get_plan_details(self):
        plan_name = self.get_plan()
        if plan_name is None:
            return None
        
        return self.plans.get(plan_name)
    """
        Get plan's description
        Return string
    """
    
    def get_description(self):
        details = self.get_plan_details()
        return details.get("description") if details else None
    
    """
        Get covered services
        Returns a list including all the services covered
    """
    def get_coverage(self):
        details = self.get_plan_details()
        return details.get("coverage") if details else None
    
    """
        Get copays
        Returns string
    """

    def get_copay(self):
        details = self.get_plan_details()
        return details.get("copay") if details else None
    
    """
        Has premiums
        Returns boolean
    """
    def has_premium(self):
        details = self.get_plan_details()
        if details is None:
            return False
        return "no premium" not in details["premium"].lower()

    """
        Has deductibles
        Returns boolean
    """
   
    def has_deductible(self):
        details = self.get_plan_details()
        if details is None:
            return False
        return details.get("deductible") == "Yes"
    """
    Return a summary that contains all the inforamtion above
    """
    def get_summary(self):
        plan = self.get_plan()
        details = self.get_plan_details()
        
        if plan is None:
            return {
                "program": self.program,
                "eligible": False,
                "plan": None,
            }
        
        return {
            "program": self.program,
            "eligible": True,
            "plan": plan,
            "description": details["description"],
            "coverage": details["coverage"],
            "copay": details["copay"],
            "premium": details["premium"],
            "deductible": details["deductible"],
        }