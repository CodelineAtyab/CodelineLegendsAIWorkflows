import re

# Read the file
list_of_prompts = []
with open("user_prompts.txt") as user_prompts_file:
  list_of_prompts = user_prompts_file.readlines()

# Transformed the file content (Data Cleaning)
cleaned_prompts = []
for prompt_line in list_of_prompts:
  cleaned_prompts.append(prompt_line.strip())

"""
Draft an appointment request for fictional resident 
Aisha Al-Harthy in Muscat, Oman; include the 
sample phone number +96892034543 something else.
"""
phone_number_re_pattern = re.compile(r"\+968[0-9]+")

# Masking the cleaned prompts
masked_prompts = []
for filtered_prompt in cleaned_prompts:
   curr_masked_prompt = phone_number_re_pattern.sub("[phone_number_here]", filtered_prompt)
   masked_prompts.append(curr_masked_prompt)
   
# Write the masked prompts (results) to the file
with open("masked_prompts.txt", 'w') as masked_prompts_file:
  for curr_masked_prompt in masked_prompts:
    masked_prompts_file.write(curr_masked_prompt + "\n")