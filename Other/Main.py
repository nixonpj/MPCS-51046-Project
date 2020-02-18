class Member:
    def __init__(self, name, gender, spouse_father, age,
                 religion, soc_category, disability, apl_bpl):
        self.name = name
        self.gender = gender
        self.spouse_father = spouse_father
        self.age = age
        self.religion = religion
        self.soc_category = soc_category
        self.disability = disability
        self.apl_bpl = apl_bpl


    def __str__(self):
        return str([self.name, self.gender, self.spouse_father, self.age,
                 self.religion, self.soc_category, self.disability, self.apl_bpl])


    def
a = Member('pooja devi', 'female', 'rajaram', 29, 'Hindu', 'OBC', 'No', 'APL')

print(a)