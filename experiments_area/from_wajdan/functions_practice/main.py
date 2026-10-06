# Variables and data types
number_one: int = 23
div_result: float = 4.5
is_active: bool = True
name: str = "Mr.A"
a_char: str = "a"


# Conditions
if is_active:
    print("Hello")
    print("Hello")
elif len(name) < 5:
    print("less than 5")
else:
    print("World")
    print("World")


# List
name_of_team_members: list = [
    "Hydaya",
    "Shaheen",
    "Ikhlas",
    "Mohammed",
]


# Dictionary
team_member_info: dict = {
    "status": "OK",
    "ip_address": "192.168.1.10",
    "active": True,
}


# Split a sentence into words
sentence = (
    "Why do Omanis never get lost in the desert? "
    "Because even the dunes know the way to Muscat!"
)

list_of_words = sentence.split()


# Join the words with a dash
new_sentence = "-".join(list_of_words)
print(new_sentence)


# While loop
counter = 0

while counter < len(name_of_team_members):
    print(name_of_team_members[counter])
    counter += 1


# For loop
for member_name in name_of_team_members:
    print(member_name)


# Filter names containing lowercase e
print(
    list(
        filter(
            lambda curr_name: "e" in curr_name,
            name_of_team_members,
        )
    )
)


# Print numbers from 0 to 4
for i in range(0, 5):
    print(i)