
class Plan:
    eligible_categories = [
        'children_0_1',  
        'children_1_5',      
        'children_6_18',     
        'children_chip',    
        'pregnant_medicaid', 
        'parents' ,           
        'expansion_adults'   
    ]

    plans = {
        "MassHealth Standard": {
            "description": "Generally for individuals who are pregnant, children, disabled, seniors, or medically frail",
            "coverage": "Full medical, dental, mental health, long-term care",
        },
        "MassHealth CommonHealth": {
            "description": "For disabled working adults",
            "coverage": "Similar to Standard, includes long-term care",
        },
        "MassHealth CarePlus": {
            "description": "For working adults without children",
            "coverage": "Doctor visits, hospital, but limited long-term care",
        },
        "CHIP": {
            "description": "Children's Health Insurance Program for households with income > 300% poverty level",
            "coverage": "Similar to Standard for children",
        },
        "MassHealth Family Assistance": {
            "description": "For people with immigration restrictions",
            "coverage": "Medical services, no long-term care",
        },
        "MassHealth Limited": {
            "description": "Emergency services only",
            "coverage": "Emergency medical services only",
            "copay": "Varies",
        },

    }
    category_to_plans = {
       'children_0_1': "MassHealth Standard",  
            'children_1_5': "MassHealth Standard",      
            'children_6_18': "MassHealth Standard",     
            'children_chip': "CHIP" ,    
            'pregnant_medicaid': "MassHealth Standard", 
            'parents': "MassHealth Standard" ,           
            'expansion_adults':  "MassHealth CarePlus"   
   }

    def __init__(self,eligible_categories, family_size, age, annual_income, is_pregnant, is_parent, is_disabled, citizenship_eligibility):
        self.eligible_categories = eligible_categories
        self.family_size = family_size
        self.annual_income = annual_income
        self.age = age
        self.is_pregnant = is_pregnant
        self.is_parent = is_parent
        self.is_disabled = is_disabled
        self.citizenship_eligibility = citizenship_eligibility

    def eligible_plans(self):
        eligible_plans = []
        for category in self.eligible_categories:
            if category in self.category_to_plans:
                plan = self.category_to_plans[category]
                if plan not in eligible_plans:
                    eligible_plans.append(plan)

        if self.is_disabled and "MassHealth CommonHealth" not in eligible_plans:
            eligible_plans.append("MassHealth CommonHealth")
        
        if self.citizenship not in ["US Citizen", "Permanent Residency"]:#Had to fix here to relate with MassHealthEligibility checker
            if "MassHealth Family Assistance" not in eligible_plans:
                eligible_plans.append("MassHealth Family Assistance")
    #Removed the immigration status variable because we arent taking that into account

            if "MassHealth Limited" not in eligible_plans:
                    eligible_plans.append("MassHealth Limited")
        return eligible_plans
    
    def plan_summary(self):
    
        # Get all eligible plans
        all_plans = self.eligible_plans()

        return {
            "family_size": self.family_size,
            "annual_income": self.annual_income,
            "eligible_categories": self.eligible_categories,
            "age": self.age,
            "is_disabled": self.is_disabled,
            "is_pregnant": self.is_pregnant,
            "is_parent": self.is_parent,
            "citizenship_eligibility": self.citizenship_eligibility,
            "eligible_plans": all_plans,
            "number_of_plans": len(all_plans),
        }
 
