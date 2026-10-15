def main():
    print("Hello from practice!")


if __name__ == "__main__":
    main()

num_one =45
blood_result = 10.4
is_active :bool =True
name = "asila"
a_char = 'a'


if is_active:
  print(f"Your boold mesure is {blood_result}") # f means formatted string.
else:
  print("not finished yet")
  

family_member: list = ["Asila", "Suad", "Hilal", "Mohammed"]
personal_info: dict = {"name": "asila", "ID_Card": "14236221", "active": True}
print(family_member)
family_member.append("Hammad")

#display all family member
for member in family_member:
    print(member)



sentence = "Never share your IDcard with anyone"
list_of_words = sentence.split()
new_sentence = "-".join(list_of_words)

print(new_sentence)


counter = 0
while counter < len(family_member):
    print(family_member[counter])
    counter += 1

print("-------------------")
    
# to do it reverse
counter = len(family_member) - 1

while counter >= 0:
    print(family_member[counter])
    counter -= 1
    


def get_branch_info(commit_id, name, owner_name, **kwargs):
    print("This is the commit id: " + str(commit_id))
    print("This is the name: " + name)
    print("This is the owner_name: " + owner_name)
    print(kwargs.get("duplicate_branch_name"))


get_branch_info(
    owner_name="CodelineAtyab",
    name="feature/something",
    commit_id=123,
    show_history=True,
    duplicate_branch_name="bugfix/anotherthing"
)