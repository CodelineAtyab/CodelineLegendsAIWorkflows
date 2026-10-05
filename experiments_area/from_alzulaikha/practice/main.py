def main():
    print("Hello from practice!")

    number = 30
    div_result = 9.8
    is_active = True
    name = "alzulaikha"
    a_char = "m"

    age = 33

    if age >= 18:
        print("Adult")
    elif age >= 13:
        print("Teenager")
    else:
        print("Child")
name_of_team_members: list = ["Alzulaikha", "Bader", "Saif", "Ali"]
print(name_of_team_members)
print(name_of_team_members[1])
print(len(name_of_team_members))
team_member_info: dict = {
        "status": "OK",
        "ip_address": "192.168.1.1",
        "active": True
}
message = "Learning Python programming can help us build useful applications and solve many interesting problems"

words = message.split()

new_message = "|".join(words)

print(new_message)

def my_sum(num_1, num_2, num_3, *args):
    result = num_1 + num_2 + num_3

    # Add the extra numbers in result
    for curr_num in args:
        result = result + curr_num

    return result


print(my_sum(5, 6, 7, 15, 16, 11, 12))

def get_branch_info(commit_id, name, owner_name, **kwargs):
    print("This is the commit id: " + str(commit_id))
    print("This is the name: " + name)
    print("This is the owner_name: " + owner_name)
    print(kwargs)


get_branch_info(
    owner_name="CodelineAtyab",
    name="feature/something",
    commit_id=123,
    show_history=True,
    duplicate_branch_name="bugfix/anotherthing"
)

if __name__ == "__main__":
    main()