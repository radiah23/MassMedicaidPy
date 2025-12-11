from __future__ import annotations
from typing import List
from datetime import datetime, date
class Person:
    """
    Instantiates a Person object that will be the the parent class for the Individual and Dependent classes.
    ------------------------------------------------------------------------------------------------------------------------------------------
        Attributes:

        gender                  String 
                                The gender identity of a person 
                                Must be one of the options in this list [Male, Female, Prefer not to Disclose]

        citizenship             String
                                The citizenship of a person 
                                Must be one of the options in this list [US Citizen, Permanent Resident]

        birthdate               datetime.date
                                Person's date of birth. Accepts a string in 'YYYY-MM-DD' format.
                                Strings in "YYYY-MM-DD" format are converted to datetime.date.
                               
        state                   String 
                                The state the person is from
                                Accepts only Massachussetts residents. Inputs must be one of the options in the list [Massachussetts, MA]

                        
   ----------------------------------------------------------------------------------------------------------------------------------------------
    Methods : 
        calculate_age(self)             Integer
                                        Returns the age in years after the user inputs their birthdate 

        is_child_acc_to_mass(self)      Boolean 
                                        Checks if the person is under 18 and returns true if the person is and false otherwise

        
        is_senior_acc_to_mass(self)     Boolean 
                                        Checks if the person is over or equal to 65 and returns true if the person is and false otherwise
        
        
        is_adult(self)                  Boolean 
                                        Checks if the person is over 18 and under 65 and returns true if the person is and false otherwise
    --------------------------------------------------------------------------------------------------------------------------------------------------
 """    

    def __init__(self, gender, citizenship, birthdate, state):
        gender_options = ["Male", "Female", "Prefer not to Disclose"]   
        
        #Error messages to validate the type
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

    #Assigning the values passed into the constructor   
        self.gender = gender
        self.citizenship = citizenship
        self.birthdate = birthdate
        self.state = state


    #Calculating the age of the Person class
    def calculate_age(self) -> int:
        """ 
        This function calculates the age of the person from their birthdate. 
        :return : (int) Returns the calculated age

        >>> person1 = Person("Female", "US Citizen", "2000-01-01", "MA")
        >>> person1.calculate_age()
        25
        """
        date_today = date.today()
        if isinstance(self.birthdate, str):
            birthdate_input = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        else:
            birthdate_input = self.birthdate
        age = date_today.year - birthdate_input.year - (
            (date_today.month, date_today.day) < (birthdate_input.month, birthdate_input.day)
        )
     
        
       
    #Is the person under 18?
    def is_child_acc_to_mass(self) -> bool:
         """ 
        This function checks if the person is a child according to MassMedicaid's rules
        :return : (bool) returns True if the person is under 19, false if otherwise

        >>> person1 = Person("Female", "US Citizen", "2000-01-01", "MA")
        >>> person1.is_child_acc_to_mass()
        False
        """
         return self.calculate_age() < 19 
    
   #Is the person a senior?
    def is_senior_acc_to_mass(self) -> bool: 
        """ 
        This function checks if the person is a senior according to MassMedicaid's rules
        :return : (bool) returns True if the person is over or equal to 65 , false if otherwise
        >>> person1 = Person("Female", "US Citizen", "2000-01-01", "MA")
        >>> person1.is_senior_acc_to_mass()
        False
        """
        return self.calculate_age() >= 65
    
    #Is the person an adult?
    def is_adult(self) -> bool:
        """ 
        This function checks if the person is an adult according to MassMedicaid's rules
        :return : (bool) returns True if the person is under 65 and over 19 , false if otherwise
        >>> person1 = Person("Female", "US Citizen", "2000-01-01", "MA")
        >>> person1.is_adult()
        True
        """
        return 19 <= self.calculate_age() < 65 


class Individual(Person):
     """
    Inherits the person class and instantiates an Individual object which will be referred to as a primary applicant later on in the code.
    -------------------------------------------------------------------------------------------------------------------------------------------
    Attributes:
        disability_status       Boolean 
                                Checks if the Individual identifies as Disabled. True if yes, false otherwise
                                
        pregnancy_status        Boolean 
                                Checks if the Individual is pregnant. True if yes, false otherwise

        is_primary_caretaker    Boolean
                                Checks if the Individual is primary caretaker. True if yes, false otherwise.
                                For the scope of this package, we have assumed that the individual is always the primary caretaker
                                               
    ----------------------------------------------------------------------------------------------------------------------------------------------
    """    

     def __init__(self,gender,citizenship,birthdate, state,disability_status: bool,pregnancy_status: bool,is_primary_caretaker: bool = True):    
    
    #Accesses the parent class Person and its' attributes 
        super().__init__(gender, citizenship, birthdate, state)
    
    #Validates the type of the attributes
        if not isinstance(disability_status, bool):
            raise TypeError("Disabiity Status must be true or false")
        if not isinstance(pregnancy_status, bool):
            raise TypeError("pregnancy_status must be true or false")
       
        if not isinstance(is_primary_caretaker, bool):
            raise TypeError("Primary Takecare Status must be true")
    
        self.disability_status = disability_status
        self.pregnancy_status = pregnancy_status    
        self.is_primary_caretaker = is_primary_caretaker
        self.household = None 


class Dependent(Person):
     """
    Inherits the person class and instantiates an Dependent object which will be referred to as a primary applicant later on in the code.
    -------------------------------------------------------------------------------------------------------------------------------------------
    Attributes:

        disability_status       Boolean 
                                Checks if the Dependent identifies as Disabled. True if yes, false otherwise
                                
        pregnancy_status        Boolean 
                                Checks if the Dependent is pregnant. True if yes, false otherwise
        
        relationship_to_the_    String
        applicant               Dependent's relationship to the primary applicant
                                Must be one of the options ["Spouse", "Child", "Adult-Related-Dependent"]
                                                 
    ----------------------------------------------------------------------------------------------------------------------------------------------
    """    

     def __init__(self,gender,citizenship,birthdate,state,relationship_to_the_applicant: str,disability_status: bool = False,pregnancy_status: bool = False
    ):
    #Accesses the parent class Person and its' attributes 
        super().__init__(gender, citizenship, birthdate, state)

        relationship_to_the_applicant_options = ["Spouse", "Child", "Adult-Related-Dependent"]

    #Checks the types of the attributes 
        if not isinstance(relationship_to_the_applicant, str):
            raise TypeError("relationship_to_the_applicant must be a string")

        if relationship_to_the_applicant not in relationship_to_the_applicant_options:
        
            raise ValueError("Invalid dependent relationship type")        
        self.relationship_to_the_applicant = relationship_to_the_applicant
        self.disability_status = disability_status
        self.pregnancy_status = pregnancy_status
        self.household = None


class Household:
    """
    Instantiates a Household object that contains the primary applicant and the dependents with their total income. This is the class that connects Individual and 
    Dependents and store them in one household. The package does not let someone who is not an adult yet to be a primary applicant, so it will throw a ValueError. 
    The class stores the primary applicant in the household and runs with the assumption that the dependents live in the same household as well. It does
    not take into account if the dependents live out of the household. 

    ------------------------------------------------------------------------------------------------------------------------------------------
        Attributes:

        primary_applicant       Dictionary 
                                A dictionary containing the primary applicant’s information. This dictionary 
                                is built from an Individual object (Individual class) and includes informations such as 
                                gender, citizenship, birthdate, state, disability status, pregnancy status, caretaker status

        dependent_list          List 
                                A list of dictionaries built from Dependent objects, each representing a dependent’s 
                                information: gender, citizenship, birthdate, relationship to the applicant, disability status, pregnancy status

        total_income            float
                                Household object's total income. 
                                Users need to input their yearly total income. For the scope of this package the users need to compute
                                their own household income and use that as total income
   ----------------------------------------------------------------------------------------------------------------------------------------------
    Methods : 
        get_income(self)        Float
                                Returns the household object's total income and returns it 

        household_size(self)    Integer
                                Returns the total number of people living in the household
                            
        dependent_count(self)   Integer
                                Returns the number of dependents in the household. 
        
        add_dependent
        (self, 
        newDependent: Dependent) None 
                                 Lets the primary applicant add a new dependent to the household
        
        
        get_children(self)      Integer
                                Returns the number of children in house. 
               
        is_parent(self)         Boolean
                                Checks if the primary applicant is a parent. Returns true if yes, false if otherwise
                                
        get_adults(self)        Integer
                                Returns the number of adults in house. 

        get_seniors(self)       Integer
                                Returns the number of seniors in house. 
        
        has_seniors (self)      Boolean
                                Checks if the household has seniors. Returns true if yes, false if otherwise
                        
        has_disabled_
        member(self)            Boolean
                                Checks if the household has disabled members. Returns true if yes, false if otherwise

        has_pregnancy(self)     Boolean
                                Checks if the household has pregnant members. Returns true if yes, false if otherwise
                        
                                                                                                                                    Checks if the person is over 18 and under 65 and returns true if the person is and false otherwise
    --------------------------------------------------------------------------------------------------------------------------------------------------
    """    



    def __init__(self, primary_applicant: Individual, dependent_list: list[Dependent], total_income: float):  
        if primary_applicant.is_child_acc_to_mass():
            raise ValueError("Primary applicant cannot be < 19")
        self.primary_applicant = primary_applicant
        self.dependent_list = dependent_list
        self.total_income = total_income
        self.primary_applicant.household = self 
        for dependent in self.dependent_list: 
            dependent.household = self 


    def get_income(self) -> float:
        """
        This function returns the household income (yearly)
        :return(float) Returns the household object's total income 

        >>> primary_applicant = Individual("Female", "US Citizen", "1990-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = Dependent("Male", "US Citizen", "2010-08-15", "MA",
                 disability_status=False, pregnancy_status=False)
        >>> house1 = Household(primary, [dependent], total_income=55000.0)
        >>> house1.get_income()
        55000.0
        """
    
        return self.total_income
    
    def household_size(self) -> int:

        """
            This function calculates the total number of people living in the household
            :return(float) returns the total number of people living in the household

            >>> primary_applicant = Individual("Female", "US Citizen", "1990-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
            >>> dependent = Dependent("Male", "US Citizen", "2010-08-15", "MA",
                    disability_status=False, pregnancy_status=False)
            >>> house1 = Household(primary, [dependent], total_income=55000.0)
            >>> house1.household_size()
            2
        """
        return 1 + len(self.dependent_list)
    
    def dependent_count(self) -> int:
        """
        This function calculates the number of dependent in the household
        :return(float) Returns the number of dependent in the household

        >>> primary_applicant = Individual("Female", "US Citizen", "1990-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = Dependent("Male", "US Citizen", "2010-08-15", "MA",
                 disability_status=False, pregnancy_status=False)
        >>> house1 = Household(primary, [dependent], total_income=55000.0)
        >>> house1.dependent_count()
        1
        """
        return len(self.dependent_list)
    
#Adds Dependents
    def add_dependent(self, newDependent: Dependent):
        """
        This function will let the user to add dependents of the household. It also checks if the primary applicant is a child. If yes, it doesnt let 
        the user use this package because it limits the primary applicants to be an adult. 

        :param newDependent: (Dependent) The dependent object the user adds
        >>> primary_applicant = Individual("Female", "US Citizen", "1990-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = Dependent("Male", "US Citizen", "2010-08-15", "MA",
                 disability_status=False, pregnancy_status=False)
        >>> dependent2 = Dependent("Female", "US Citizen", "2012-08-15", "MA",
                 disability_status=False, pregnancy_status=False)
        >>> house1 = Household(primary, [dependent], total_income=55000.0)
        >>> house1.add_dependent(dependent2)
        None
     """
        if self.primary_applicant.is_child_acc_to_mass():
            raise ValueError("An individual under 18 cannot be a primary applicant with dependents")
        self.dependent_list.append(newDependent)

#Returns how many kids are there
    def get_children(self) -> int:
        """
        This function calculates the number of dependents who are children in the household. It first creates an empty list and then loops through the dependent list to check
        how many people are children there. 
        :return: (int) Returns number of child dependents.

        >>> primary_applicant = Individual("Female", "US Citizen", "1990-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = Dependent("Male", "US Citizen", "2010-08-15", "MA",
                 disability_status=False, pregnancy_status=False)
        >>> dependent2 = Dependent("Female", "US Citizen", "2015-08-15", "MA",
                 disability_status=False, pregnancy_status=False)
        >>> house1 = Household(primary, [dependent, dependent2], total_income=55000.0)
        >>> house1.get_children()
        2
        """
        children = []
        for dep in self.dependent_list:
            if dep.is_child_acc_to_mass():
                children.append(dep)
        return len(children)
    
#Checks if the applicant is a parent 
    def is_parent(self) -> bool:

        """
        This function checks whether the primary applicant is a parent. 

        :return: (bool) Returns true if the primary applicant has children, false if otherwise. 

        >>> primary_applicant = Individual("Female", "US Citizen", "1990-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = [] 
        >>> house2 = Household(primary, dependent, total_income=55000.0)
        >>> house2.is_parent()
        False
        """
        return self.get_children() > 0
    
#Checks the number of adults in the household
    def get_adults(self) -> int:
        """
        This function calculates the number of adults in the household.
        :return: (int) Returns the number of adults in the household.

        >>> primary_applicant = Individual("Female", "US Citizen", "1990-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = [] 
        >>> house2 = Household(primary, dependent, total_income=55000.0)
        >>> house2.get_adults()
        1
        """
        adults = []
        if self.primary_applicant.is_adult():
            adults.append(self.primary_applicant)
        for dep in self.dependent_list:
            if dep.is_adult():
                adults.append(dep)
        return len(adults)

#Checks the number of seniors in the household
    def get_seniors(self) -> int:
        """
        This function returns the number of seniors in the household.
        :return: (int) The number of sen in the household.

        >>> primary_applicant = Individual("Female", "US Citizen", "1960-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = [] 
        >>> house2 = Household(primary, dependent, total_income=55000.0)
        >>> house2.get_seniors()
        1
        """
        seniors = []
        if self.primary_applicant.is_senior_acc_to_mass():
            seniors.append(self.primary_applicant)
        for dep in self.dependent_list:
            if dep.is_senior_acc_to_mass():
                seniors.append(dep)
        return len(seniors) 

#Checks if the household has seniors      
    def has_seniors(self) -> bool:
        """
        This function checks if the household has any seniors. 
        :return: (bool) Returns true if the household has any seniors and false if otherwise

        >>> primary_applicant = Individual("Female", "US Citizen", "1960-05-10", "MA", disability_status=False, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = [] 
        >>> house2 = Household(primary, dependent, total_income=55000.0)
        >>> house2.has_seniors()
        True
        """
        if self.primary_applicant.is_senior_acc_to_mass():
            return True
        for dep in self.dependent_list:
            if dep.is_senior_acc_to_mass():
                return True
        return False

#Checks if the household has disabled members 

    def has_disabled_member(self) -> bool:
        """
        This function checks if the household has any disabled members. 
        :return: (bool) Returns true if the household has any disabled members and false if otherwise

        >>> primary_applicant = Individual("Female", "US Citizen", "1960-05-10", "MA", disability_status=True, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = [] 
        >>> house2 = Household(primary, dependent, total_income=55000.0)
        >>> house2.has_disabled_member()
        True
        """
        if self.primary_applicant.disability_status:
            return True
        for dep in self.dependent_list:
            if dep.disability_status:
                return True
        return False
    
#Checks if the household has pregnant members 
    
    def has_pregnancy(self) -> bool:
        """
        This function checks if the household has any pregnant members. 
        :return: (bool) Returns true if the household has any pregnant members and false if otherwise

        >>> primary_applicant = Individual("Female", "US Citizen", "1960-05-10", "MA", disability_status=True, pregnancy_status=False,is_primary_caretaker=True)
        >>> dependent = [] 
        >>> house2 = Household(primary, dependent, total_income=55000.0)
        >>> house2.has_pregnancy()
        False
        """
        if self.primary_applicant.pregnancy_status:
            return True
        for dep in self.dependent_list:
            if dep.pregnancy_status:
                return True
        return False


    
