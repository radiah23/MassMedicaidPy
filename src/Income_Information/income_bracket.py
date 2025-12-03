class Income:
    age_categories = [
        "child_0_1",
        "child_1_5",
        "child_6_18",
        "child_chip",
        "pregnant_woman_medicaid",
        "adult_parent_caretaker",
        "adult_expansion",
    ]
# Base level is one-person household yearly income
    federal_poverty_level = {
        "100%": {"base": 15660, "per_person": 5508},
        "133%": {"base": 20820, "per_person": 7320},
        "150%": {"base": 23484, "per_person": 8256},
        "200%": {"base": 31308, "per_person": 11004},
        "300%": {"base": 46956, "per_person": 16500},
    }

    category_eligibility = {
        "child_0_1": "200%",
        "child_1_5": "150%",
        "child_6_18": "150%",
        "child_chip": "300%",
        "pregnant_woman_medicaid": "200%",
        "adult_parent_caretaker": "133%",
        "adult_expansion": "133%",
    }

    def __init__(self, family_size, household_income):
        self.family_size = family_size
        self.household_income = household_income



        