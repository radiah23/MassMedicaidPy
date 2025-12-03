from datetime import datetime,date


class Person: #it is the entire thing where the other classes are going to inherit 
    #Assuming citizenship is same
    # Plan : 
    # Household is the parent class 
    # Individual and dependent is going to inherit this household classs o it needs to have everything the parent class has 
    #Assuming it is medicaid always
    # disability_status, pregnant_member, gender,age, --> Individual
    #Seperate class for income_bracket
    

    def __init__(self,gender, citizenship,birthdate): 
        self.citizenship = citizenship
        self.gender = gender
        self.birthdate = birthdate
    
    def calculate_age(self):
        '''
        this function is going to compute the proper age with the today's date. 
        '''

        today_date = date.today()
        age = (today_date.year - self.birthdate.year- ((today_date.month, today_date.day) < (self.birthdate.month, self.birthdate.day)))

        return age
    
    
class Individual(Person):
    def __init__(self,citizenship,gender,birthdate: datetime,disability_status: bool,pregnant_status: bool):
        super().__init__(citizenship, gender, birthdate)
        self.disability_status = disability_status
        self.pregnant_status = pregnant_status
        
#How do we loop it to go there if they have dependent 
#Do we put user inputs there 
# Do not need a main
#for the error message : check inside the classes 
#Unit test : with the correct code it works 

class Dependent(Person): 
    def __init(self, citizenship,gender,birthdate:datetime, relationship_to_individual):
        super().__init__(citizenship, gender, birthdate)
        self.relationship_to_individual = relationship_to_individual



    






  