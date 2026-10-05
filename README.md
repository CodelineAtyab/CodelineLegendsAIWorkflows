# CodelineLegendsAIWorkflows

Under Development By Team Codeline Legends

## About This Project
To be defined ...
---

## Contribution Guidelines

### Step 1
Copy the issue ID (ticket-id) from GitHub issues

### Step 2
Goto the repo and git status (Make sure you are on main branch)

### Step 3
git pull (Make sure you are up to date)

### Step 4
Create a new branch (replica of main) from the main branch and check it out (switch to the new branch)
Example: `git branch feature/<ticket-id>-ticket-title`

### Step 5
Checkout the new branch using git checkout 
Example: `git checkout feature/<ticket-id>-ticket-title`

### Step 6
Now do your task

### Step 7
Push your changes (branch) to github by doing:
```
git add *
git commit -m "some-message"
git push 
```
NOTE: (if upstream bracnh is not there then run the --set-upstream command given by git only once)

### Step 8
Got GitHub and click on "Compare & pull request"

### Step 9
Add Reviewers and Click on "Create pull request"

### Step 10
Move the ticket to "Ready for Review"

### Step 11
Wait for atleast 2 approvals from the team

### Step 12
After approvals, Please "SQUASH MERGE"

### Step 13
Go back to the main branch
```
git checkout main
```

### Step 14
Pull the latest chages by doing
```
git pull
```

### Step 15
Repeat the same steps from Step 1 for a new task

