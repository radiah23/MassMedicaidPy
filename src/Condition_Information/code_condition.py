from Household_Information.code_household import Person, Individual, Household
class MassHealthEligibilityChecker:
   def __init__(self):
       #yearly federal poverty level  - yearly income
       self.annual_fpl = {
           1: 15660,  
           2: 21156,
           3: 26652,
           4: 32160,
           5: 37656,
           6: 43152,
           7: 48660,
           8: 54156
       }
      
       self.additional_person_annual = 5508
      
       # Different income percentage standards
       #the categories
       self.eligibility_standards = {
           'children_0_1': 2.00,      # 200%
           'children_1_5': 1.50,     
           'children_6_18': 1.50,    
           'children_chip': 3.00 ,   
           'pregnant_medicaid': 2.00,
           'parents': 1.33,          
           'expansion_adults': 1.33  
       }
#Here it was saying self but it should access person. bevause it is accessing the person objects 
   def regional_belonging(self, person:Person):#Person object
       if person.state == "Massachusetts":
           return person.state
       else:
           return "You might need to consider federal medicare options or your state options"


   def citizenship_eligibility(self,person):
        if person.citizenship == "US Citizen":
            return person.citizenship
        elif person.citizenship == "Permanent Residency":
            return person.citizenship
        else:
            return "Sorry, there are other eligible international insurance options for you."

  
   def calculate_annual_fpl(self, family_size):
       """Calculate the Federal Poverty Level (annual income) for a given family size
           and return the annual FPL amount."""
       if family_size <= 0:
           return ValueError #Fixed here because I think it should be atleast 1 person who is applying - Radiah
      
       if family_size <= 8:
           return self.annual_fpl[family_size]
       else:
           return self.annual_fpl[8] + (family_size - 8) * self.additional_person_annual
  
   def get_annual_income_limit(self, category, family_size):
       """Get the annual income limit for a specific category
           and return the limit amount."""
       percentage = self.eligibility_standards.get(category)
       if percentage is None:
           return ValueError #invalid ???? or return as error ??????? #But ask again
      
       fpl = self.calculate_annual_fpl(family_size)
       return fpl * percentage
  
   def check_eligibility(self, age, annual_income, family_size,
                        is_pregnant=False, is_parent=False):
       """
       evaluate eligibility for MassHealth programs based on provided criteria.
      
       Parameters:
           age: Age in years
           annual_income: Annual income in USD
           family_size: Number of family members
           is_pregnant: Whether pregnant
           is_parent: Whether a parent/caretaker


       Returns:
           A dictionary with eligibility results and details.
       """
       # Calculate the current income as a percentage of the FPL
       fpl = self.calculate_annual_fpl(family_size)
       fpl_percentage = (annual_income / fpl) if fpl > 0 else 0
      
       results = {
           'eligible': False,
           'program': None,
           'is_chip': False,
           'annual_income_limit': 0,
           'current_annual_income': annual_income,
           'fpl_percentage': round(fpl_percentage * 100, 1),
           'annual_fpl': fpl,
           'family_size': family_size
       }
      
       # pregnancy check
       if is_pregnant:
           limit = self.get_annual_income_limit('pregnant_medicaid', family_size)
           if annual_income <= limit:
               results['eligible'] = True
               results['program'] = "Medicaid for Pregnant Women"
               results['annual_income_limit'] = limit
           return results
      
       # 2. Children check (0-18 years)
       if age <= 18:
           # First check Medicaid eligibility
           if age < 1:  # 0-1 years
               limit = self.get_annual_income_limit('children_0_1', family_size)
               program_name = "Children's Medicaid (0-1)"
           elif age <= 5:  # 1-5 years
               limit = self.get_annual_income_limit('children_1_5', family_size)
               program_name = "Children's Medicaid (1-5)"
           else:  # 6-18 years
               limit = self.get_annual_income_limit('children_6_18', family_size)
               program_name = "Children's Medicaid (6-18)"
          
           if annual_income <= limit:
               results['eligible'] = True
               results['program'] = program_name
               results['annual_income_limit'] = limit
           else:
               # extra check for CHIP eligibility
               chip_limit = self.get_annual_income_limit('children_chip', family_size)
               if annual_income <= chip_limit:
                   results['eligible'] = True
                   results['program'] = "Children's Separate CHIP"
                   results['annual_income_limit'] = chip_limit
                   results['is_chip'] = True
      
       # 3. Adult check (19 years and older)
       elif age >= 19:
           if is_parent:  # Parents/Caretakers
               limit = self.get_annual_income_limit('parents', family_size)
               program_name = "Medicaid for Parents/Caretakers"
           else:  # Expansion adults
               limit = self.get_annual_income_limit('expansion_adults', family_size)
               program_name = "Medicaid Expansion for Adults"
          
           if annual_income <= limit:
               results['eligible'] = True
               results['program'] = program_name
               results['annual_income_limit'] = limit
      
       return results
    
   def check_household_eligibility(self, household: Household) -> dict:
        """:
        Check eligibility for all members in a household using household data.
        return a dictionary with eligibility results for each member.
        """
        regional_check = self.regional_belonging(household.primary_applicant)
        if regional_check != "Massachusetts":
            return {"eligible": False,
                    "reason":"Household not in Massachusetts",
                    "message": regional_check}
        
        citizenship_check = self.citizenship_eligibility(household.primary_applicant)
        if citizenship_check not in ["US Citizen", "Permanent Residency"]:
            return {"eligible": False,
                    "reason":"Household members do not meet citizenship requirements",
                    "message": citizenship_check}
        return self.check_eligibility(
            age=household.individual.calculate_age(),
            annual_income=household.get_income(),
            family_size=household.household_size(),
            is_pregnant=household.individual.pregnancy_status,
            is_parent= household.is_parent()
        )
   
#Fixes: connected th classes in a way that it doesnt duplicated
#specifically in the return function 
#Fixed the is_parent with() by calling the method DIRECTLYYYY