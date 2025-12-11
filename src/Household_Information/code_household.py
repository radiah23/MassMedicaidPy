# Added for import issues
from __future__ import annotations
from typing import List
from datetime import datetime, date
#Citation : 
#Used Claude to plan the classes structures'
#The prompts that I used was :"Given this final project proposal, help us build a skeleton structure of methods that we planned to plan the structure better without explicitly giving the code"
class Person:
    def __init__(self, gender, citizenship, birthdate, state):
        gender_options = ["Male", "Female", "Prefer not to Disclose"]   
        #Error messages
        if not isinstance(gender, str):
            raise TypeError("gender must be a string")
        if gender not in gender_options:
            raise ValueError("Gender must be one of: Male, Female, Prefer not to Disclose")
        if not isinstance(citizenship, str):
            raise TypeError("citizenship must be a string")
        if isinstance(birthdate, str):
            try:
                datetime.strptime(birthdate, "%Y-%m-%d")
            except ValueError:
                raise ValueError("birthdate must be in valid 'YYYY-MM-DD' format")
        elif not isinstance(birthdate, date):
            raise TypeError("birthdate must be a string or datetime.date")
        if not isinstance(state, str):
            raise TypeError("state must be a string")     
        self.gender = gender
        self.citizenship = citizenship
        self.birthdate = birthdate
        self.state = state
    #Calculating the age of the Person class
    def calculate_age(self) -> int:
        date_today = date.today()
        if isinstance(self.birthdate, str):
            birthdate_input = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        else:
            birthdate_input = self.birthdate
        age = date_today.year - birthdate_input.year - (
            (date_today.month, date_today.day) < (birthdate_input.month, birthdate_input.day)
        )
        if not isinstance(age, int):
            raise TypeError("Age must be in integer")
        if age < 0: 
            raise ValueError("Age cannot be negetive")
        return age
    #Is the person under 18?
    #We want to see if they are up for a student package. There is one scope that they might be living out of state but for the time scope of the project we assumed they live with their parents state
    def is_child_acc_to_mass(self) -> bool:
        return self.calculate_age() < 19 
   #Is the person a senior?
    def is_senior_acc_to_mass(self) -> bool: #returns a yes or no 
        return self.calculate_age() >= 65
    #Is the person an adult?
    def is_adult(self) -> bool:
        return 19 <= self.calculate_age() < 65   
class Individual(Person):
    #Really complicated so we assume it is the primary takecarer
    def __init__(
        self,
        gender,
        citizenship,
        birthdate,
        state,
        disability_status: bool,
        pregnancy_status: bool,
#Include it in the documentation 
        is_primary_caretaker: bool = True
    ):
        super().__init__(gender, citizenship, birthdate, state)

        if not isinstance(disability_status, bool):
            raise TypeError("Disabiity Status must be true or false")
        if not isinstance(pregnancy_status, bool):
            raise TypeError("pregnancy_status must be true or false")
       
        if not isinstance(is_primary_caretaker, bool):
            raise TypeError("Primary Takecare Status must be true")
        
        self.disability_status = disability_status
        self.pregnancy_status = pregnancy_status
       
        self.is_primary_caretaker = is_primary_caretaker
        #Important step : It is not a constructor in the individual class because an Individual cannot contain the information about the Household its the otherway around. So initially it DOES NOT have a house. 
        #I want it to know that helloo you are going to have a household that I will refer you to later. This is solely because I want it to be connected to Household together once I build it
        self.household = None 


#ask how to work this in dependent class as well/Disability??
#Assuming that spouse is included in the package 
class Dependent(Person):
    def __init__(self,gender,citizenship,birthdate,state,relationship_to_the_applicant: str,disability_status: bool = False,pregnancy_status: bool = False
    ):
        super().__init__(gender, citizenship, birthdate, state)

        relationship_to_the_applicant_options = ["Spouse", "Child", "Adult-Related-Dependent"]
        if not isinstance(relationship_to_the_applicant, str):
            raise TypeError("relationship_to_the_applicant must be a string")

        if relationship_to_the_applicant not in relationship_to_the_applicant_options:
            raise ValueError("Invalid dependent relationship type")
        self.relationship_to_the_applicant = relationship_to_the_applicant
        self.disability_status = disability_status
        self.pregnancy_status = pregnancy_status
  #Again its the same logic as above      
        self.household = None
class Household:
    def __init__(self, primary_applicant: Individual, dependent_list: list[Dependent], total_income: float):
        if primary_applicant.is_child_acc_to_mass():
            raise ValueError("Primary applicant cannot be < 18")
        self.primary_applicant = primary_applicant
        self.dependent_list = dependent_list
        self.total_income = total_income
#Another SUPER important link I would say. I wanted it to refer it back to the primary_applicant(Which is our individual class)
        self.primary_applicant.household = self #
        for dependent in self.dependent_list: #
            dependent.household = self #
#Getters
    def get_income(self) -> float:
        return self.total_income
    def household_size(self) -> int:
        return 1 + len(self.dependent_list)
    def dependent_count(self) -> int:
        return len(self.dependent_list)
#Method : Adding Dependents
    def add_dependent(self, newDependent: Dependent):
        if self.primary_applicant.is_child_acc_to_mass():
            raise ValueError("An individual under 18 cannot be a primary applicant with dependents")
        self.dependent_list.append(newDependent)
#Len method for calculating the household size
    def __len__(self):
        return self.household_size()#Okay I made a mistake here before because I did not call it i just used normally without the ()
#Returns how many kids are there
    def get_children(self) -> int:
        children = []
        for dep in self.dependent_list:
            if dep.is_child_acc_to_mass():
                children.append(dep)
        return len(children)
#Checks if the applicant is a parent (Ask if I need to specify Indvidual)
    def is_parent(self) -> bool:
        return self.get_children() > 0
#Adults in the household
    def get_adults(self) -> int:
        adults = []
        if self.primary_applicant.is_adult():
            adults.append(self.primary_applicant)
        for dep in self.dependent_list:
            if dep.is_adult():
                adults.append(dep)
        return len(adults)
    def get_seniors(self) -> int:
        seniors = []
        if self.primary_applicant.is_senior_acc_to_mass():
            seniors.append(self.primary_applicant)
        for dep in self.dependent_list:
            if dep.is_senior_acc_to_mass():
                seniors.append(dep)
        return len(seniors)    
    def has_seniors(self) -> bool:
        if self.primary_applicant.is_senior_acc_to_mass():
            return True
        for dep in self.dependent_list:
            if dep.is_senior_acc_to_mass():
                return True
        return False
    
    def has_disabled_member(self) -> bool:
        if self.primary_applicant.disability_status:
            return True
        for dep in self.dependent_list:
            if dep.disability_status:
                return True
        return False
    def has_pregnancy(self) -> bool:
        if self.primary_applicant.pregnancy_status:
            return True
        for dep in self.dependent_list:
            if dep.pregnancy_status:
                return True
        return False
#Goal for the result is 
#It takes the household infos --> takes it to the other files --> checks eligibility --> plans
#Problems :
#The other files does not count for disability/special status --> should we remove it then for simplicity
#And if we do it anyways because we do have a method that checks pregnancy for example in all household using has_pregnancy
    def get_eligibility_and_plans(self):
        #If we want to put it outside then import all, then all of the self will be replaced , household_infos 
        from Condition_Information.code_condition import MassHealthEligibilityChecker
        from Plan_Information.code_plan import Plan

        checker = MassHealthEligibilityChecker()
        eligibility = checker.check_household_eligibility(self)


        plan_checker = Plan(
            program=eligibility.get("program"),
            family_size=self.household_size(),
            age=self.primary_applicant.calculate_age(),
            annual_income=self.get_income(),
            is_pregnant=self.has_pregnancy(),               
            is_parent=self.is_parent(),
            is_disabled=self.has_disabled_member(),        
            citizenship_eligibility=self.primary_applicant.citizenship
        )

        return {
            "eligible": eligibility.get("eligible"),
            "eligible_plans": plan_checker.eligible_plans()
        }

#Errors and how i handled it : 
# Citation of sources used : Stack OverFlow, Claude, ChatGPT
# 1. I initially used Pydantic for validation but had a difficult time handling it and understanding it. So I decided to go for the regular way
#of error handling which was pretty easy for me to understand. 
#It took a lot of time to understand the dependency. I used AI to help me refine my logic over and over again and also debug the nitty gritties of code. While 
#Asking for help from AI I mentioned to not give me the direct code so that I can build on the logics it gives me
#A big mistake that I was constantly doing was error in calling a method, everytime I called the age method i forgot to put () in it so it was never actually "calling" the function.
#For the age calculation, we were lowkey confused because theres that month factor : suppose someone might be 15 year 7 months so that calculation
#was pretty complex. So we just took the year from the age to keep it simple. 
#Something we really really struggled with is understanding how to connect the different classes together. Especially household, individual and dependent
#Bidirectional Association was a difficult concept so it took a lot of trial and error over stack overflow and ai tools mentioned above to understand https://stackoverflow.com/questions/63758893/implementing-a-bidirectional-association-relationship-in-python
#Article was helpful but still the question was on implemneting so I took help from the ai tools and asked "How to connect the three classes based on their inheritance with explanation"
#Approach 1: self.household = None to let it know that it is going to be in a household but now as of now it has no house
