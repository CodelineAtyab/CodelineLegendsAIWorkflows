# DYNAMICALLY TYPED LANGUAGE VS C# STATIC TYPED LANGUAGE

number_one: int = 25
div_result: float = 4.5
is_active: bool = True
name: str = "Hidaya"
a_char: str = "A"


if is_active:
    print(f"Hello {name}")
elif len(name) < 5:
    print("Name is too short")
else:
    print("Name is valid")


number_of_team_members: list = ["Hidaya", "Wijdan", "Rahaf", "Baraah", "Hafsa"]
team_number_info: dict = {
    "team_name": "Team A",
    "team_members": number_of_team_members,
    "team_leader": "Hidaya",
}

sentence = "This is a sample sentence that demonstrates the use of a string in Python. Strings can be defined using either single quotes or double quotes, and they can contain letters, numbers, and special characters."
print(sentence)
print(
    "----------------------------------------------------------------------------------------------------"
)
list_of_words = sentence.split()
new_sentence = " ".join(list_of_words)
print(new_sentence)

counter = 0
while counter < len(number_of_team_members):
    print(f"Team member {counter + 1}: {number_of_team_members[counter]}")
    counter += 1


for member in number_of_team_members:
    print(f"Team member: {member}")

print(list(filter(lambda curr_name: " i" in curr_name, number_of_team_members)))

for i in range(1, 6):
    print(f"Current number: {i}")


def my_sum(num1, num2, num3, *rest_of_numbers):
    total = num1 + num2 + num3 + sum(rest_of_numbers)
    return total


print(my_sum(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))


def my_sum1(num1, num2, num3, *rest_of_numbers):
    total = num1 + num2 + num3
    for number in rest_of_numbers:
        total += number
    return total


print(my_sum1(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))


def get_branch_info(commit_id, name, owner_name, *kwargs):
    print("This is the first id: " + str(commit_id))
    print("Branch Name: " + name)
    print("Owner Name: " + owner_name)
    print(kwargs)


get_branch_info(
    123456,
    "main",
    "Hidaya",
    "This is a sample branch",
    "This is a sample commit message",
    "This is a sample commit date",
)
