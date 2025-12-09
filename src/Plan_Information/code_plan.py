#Plan Class

class Plan:

    #When I am running the test file 
    
    program_to_category = {
    "Children's Medicaid (0-1)": "children_0_1",
    "Children's Medicaid (1-5)": "children_1_5",
    "Children's Medicaid (6-18)": "children_6_18",
    "Children's Separate CHIP": "children_chip",
    "Medicaid for Pregnant Women": "pregnant_medicaid",
    "Medicaid for Parents/Caretakers": "parents",
    "Medicaid Expansion for Adults": "expansion_adults"
}

# #Okay, this might be a problem on how we obtain the results
# Honestly on first glance the thing is we want to categorize plans
# We want to map the values to the plan labels
# But there is nothing connecting the keys to program criteria???
#The first eligible_category isnt dictionary either so there is a mismatch on the dictionary 

    category_to_plans = {
       'children_0_1': "MassHealth Standard",  
            'children_1_5': "MassHealth Standard",      
            'children_6_18': "MassHealth Standard",     
            'children_chip': "CHIP" ,    
            'pregnant_medicaid': "MassHealth Standard", 
            'parents': "MassHealth Standard" ,           
            'expansion_adults':  "MassHealth CarePlus"   
   }

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
    

    def __init__(self, program, family_size, age,
                annual_income, is_pregnant, is_parent,
                is_disabled, citizenship_eligibility):
            self.program=program #Added this here to make sure the class takes it 

            self.family_size = family_size
            self.annual_income = annual_income
            self.age = age
            self.is_pregnant = is_pregnant
            self.is_parent = is_parent
            self.is_disabled = is_disabled
            self.citizenship_eligibility = citizenship_eligibility

    def eligible_plans(self):
        eligible_plans = []
        category = self.program_to_category.get(self.program) #This is a realky crucial line because we want it to go to the Program_To_Category  --> get the value of the key which is the program name (not the plan yet)
        if category in self.category_to_plans: #(now if that category exists in the insurance plans it will give us the value of that from the category_to_plans which is again works like a key-value)
            #One confusion was to see why didnt we use.get() as well in the self.category_to_plans but used it in previous one
            #Okay so we usually whenever use .get() method --> it has a possibility that the category isnt in the pro_to_cat so we dont want it to crash, if it cannot match, its just going to return None
            eligible_plans.append(self.category_to_plans[category])

        if self.is_disabled:
            eligible_plans.append("MassHealth CommonHealth")

        
        if self.citizenship_eligibility not in ["US Citizen", "Permanent Residency"]:  # !!!!! Had to fix here to relate with MassHealthEligibilityChecker 
            if "MassHealth Family Assistance" not in eligible_plans:
                eligible_plans.append("MassHealth Family Assistance")
            # Removed the immigration status variable because we arent taking that into account
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
 
#Questions:
#Should we give them multiple plans(?)
