def get_branch_info(commit_id,name,owner_name, **kwargs):
    print(f"Commit ID: {commit_id}")
    print(f"Branch Name: {name}")
    print(f"Owner Name: {owner_name}")
    for key, value in kwargs.items():
        print(f"{key}: {value}")