# Add required numbers and extra numbers
def my_sum(number_one, number_two, number_three, *args):
    result = number_one + number_two + number_three
    result = result + sum(args)
    return result


# Print branch information
def get_branch_info(commit_id, name, owner_name, *args, **kwargs):
    print("Commit ID:", commit_id)
    print("Branch name:", name)
    print("Owner name:", owner_name)
    print("Extra arguments:", args)
    print("Options:", kwargs)


# Call with extra numbers
total = my_sum(5, 6, 7, 15, 16, 11, 12)
print("Total:", total)


# Unpack a list
numbers = [5, 6, 7]
print("Total from list:", my_sum(*numbers))


# Call with extra arguments and keyword arguments
get_branch_info(
    123,
    "practice/wajdan-python-functions",
    "Wajdan",
    "fix",
    "success",
    show_history=True,
    duplicate_branch_name="practice/example",
)


# Unpack a dictionary
branch_details = {
    "commit_id": 123,
    "name": "practice/wajdan-python-functions",
    "owner_name": "Wajdan",
    "show_history": False,
}

get_branch_info(**branch_details)
