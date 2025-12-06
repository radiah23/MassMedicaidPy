from datetime import datetime,date
from pydantic import BaseModel, PositiveFloat, ValidationError, Field, computed_field, PositiveInt
from typing import List 

class Person(BaseModel): #it is the entire thing where the other classes are going to inherit 
    #Assuming citizenship is same
    # Plan : 
    # Household is the parent class 
    # Individual and dependent is going to inherit this household classs o it needs to have everything the parent class has 
    #Assuming it is medicaid always
    # disability_status, pregnant_member, gender,age, --> Individual
    #Seperate class for income_bracket
    
    gender : str
    citizenship : str
    birthdate : date 
    state: str
    
    @computed_field 
    @property
    
    def calculate_age(self) -> PositiveInt:
        '''
        this function is going to compute the proper age with the today's date. 
        '''

        today_date = date.today()
        age = (today_date.year - self.birthdate.year- ((today_date.month, today_date.day) < (self.birthdate.month, self.birthdate.day)))

        return age


    @computed_field
    @property
    def is_child_acc_to_mass(self) -> bool:
        return self.age < 19
    
    @computed_field
    @property
    def is_senior_acc_to_mass(self) -> bool:
        return self.age >= 65
    
    @computed_field
    @property
    def is_adult(self) -> bool:
        return 19 <= self.age < 65
    
    
class Individual(Person):
    disability_status : bool
    pregnancy_status : bool 
    is_working : bool 
    has_hiv = bool 

    @computed_field
    @property 
    def has_special_status(self):
     if self.disability_status == True or self.pregnancy_status or self.has_hiv :
        return "The person has a special status"
        
#How do we loop it to go there if they have dependent 
#Do we put user inputs there 
# Do not need a main
#for the error message : check inside the classes 
#Unit test : with the correct code it works 

class Dependent(Person): 
   relationship : str 

class Household(BaseModel):
    individual : Individual #[The primary person]
    dependents : list[Dependent] #lists dependent object 
    total_income : PositiveFloat
#Functions we need : counter on how many dependents?
    @computed_field
    @property

    def household_size(self) -> int:
        return 1 + len(self.dependents)

    @computed_field
    @property
    #checks if the individual is a kid
    def has_children(self) -> bool:
        if self.individual.is_child_acc_to_mass:
            return True
    
    @computed_field
    @property
    #checks if the individual is a senior
    def has_seniors(self) -> bool:
        if self.individual.is_senior_acc_to_mass:
            return True
    
    @computed_field
    @property
     #checks if the individual is disabled
    def has_disabled_member(self) -> bool:
        if self.individual.disability_status:
            return True

    @computed_field
    @property
     #checks if the individual is pregnant
    def has_pregnancy(self) -> bool:
        if self.has_pregnancy: 
            return True
    


    @computed_field
    @property
     #checks if the individual has hiv 
    def has_pregnancy(self) -> bool:
        if self.has_hiv: 
            return True


#Problem is idk how to count if the individual is under 18 
#If an indivual is under 18, they can not be subscriber as someone who will also have dependent 
    def add_dependent(self, newDependent: Dependent): 
        self.dependents.append(newDependent)
    def __len__(self): 
        return self.household_size
    #How many people under 18
    def get_children(self) -> int : 
        children = []
        for dep in self.dependents:
            if dep.is_child_acc_to_mass:
                children.append(dep)
        return len(children)

    
    def get_adults(self) -> int:
        adults = []
        if self.individual.is_adult:
            adults.append(self.individual)
        for dep in self.dependents:
            if dep.is_adult:
                adults.append(dep)
        return len(adults)


        
    def get_seniors(self) -> int:
        seniors = []
        if self.individual.is_senior_acc_to_mass:
            seniors.append(self.individual)
        for dep in self.dependents:
            if dep.is_senior_acc_to_mass:
                seniors.append(dep)

        return len(seniors)

    
    def get_special(self) -> int:
        special_status = []
        if self.individual.has_special_status:
            special_status.append(self.individual)
        for dep in self.dependents:
            if dep.has_special_status:
                special_status.append(dep)

        return len(special_status)

    def get_income(self) -> int : 
        return self.total_income

