def get_branch_info(commit_id, name, owner_name):
  print("This is the commit id: " + str(commit_id))
  print("This is the name: " + name)
  print("This is the owner_name: " + owner_name)


# received_data = [123, "release/0.0.1", "Mr.A"]

# get_branch_info(*received_data)

received_data = {"owner_name": "Mr.A", "commit_id": 123, "name": "release/0.0.1"}
get_branch_info(**received_data)