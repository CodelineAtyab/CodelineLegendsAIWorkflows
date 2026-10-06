def get_branch_info(*args, **kwargs):
    print("This is the commit id: " + str(args[0]))
    print("This is the name: " + args[1])
    print("This is the owner_name: " + args[2])
    print(kwargs.get("duplicate_branch_name"))


get_branch_info(
    123,
    "feature/something",
    "CodelineAtyab",
    "aef231",
    "fixed the rag workflow",
    123,
    "feature/something",
    "CodelineAtyab",
    "aef231",
    "fixed the rag workflow",
    show_history=True,
    duplicate_branch_name="bugfix/anotherthing",
    show_history_1=True,
    duplicate_branch_name_1="bugfix/anotherthing",
)


def get_branch_info_with_fixed_and_dynamic_params(
    commit_id, name, owner_name, *args, **kwargs
):
    print("This is the commit id: " + str(commit_id))
    print("This is the name: " + name)
    print("This is the owner_name: " + owner_name)
    print(kwargs)


get_branch_info_with_fixed_and_dynamic_params(
    123,
    "feature/something",
    "CodelineAtyab",
    "aef231",
    "fixed the rag workflow",
    show_history=True,
    duplicate_branch_name="bugfix/anotherthing",
)


def get_branch_info_with_keyword_args(commit_id, name, owner_name, **kwargs):
    print("This is the commit id: " + str(commit_id))
    print("This is the name: " + name)
    print("This is the owner_name: " + owner_name)
    print(kwargs)


get_branch_info_with_keyword_args(
    owner_name="CodelineAtyab",
    name="feature/something",
    commit_id=123,
    show_history=True,
    duplicate_branch_name="bugfix/anotherthing",
)

get_branch_info_with_keyword_args(123, "feature/func", "CodelineAtyab")


def my_sum(num_1, num_2, num_3, *args):
    result = num_1 + num_2 + num_3

    # Add the extra number in result
    result = result + sum(args)

    return result


print(my_sum(5, 6, 7, 15, 16, 11, 12))
