def get_branch_info(commit_id, name, owner_name, **kwargs):
    print("This is the commit id: " + str(commit_id))
    print("This is the name: " + name)
    print("This is the owner_name: " + owner_name)
    print(kwargs)

get_branch_info(owner_name="CodelineAtyab",
                name="feature/something",
                commit_id=123,
                show_history=True,
                duplicate_branch_name="bugfix/anotherthing")