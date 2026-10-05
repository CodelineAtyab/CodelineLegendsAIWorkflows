number_one = 23
div_result = 4.5
is_active = True
name = 'Mr. Mohammed'
a_char = 'a'

if is_active:
  print("Hello")
  print("Hello")
elif len(name) < 5:
  print("less than 5")
elif len(name) < 5:
  print("less than 5")
elif len(name) < 5:
  print("less than 5")
else:
  print("World")
  print("World")


name_of_team_members: list = ["Hidaya", "Shaheen", "Ikhlas", "Mohammed"]
team_member_info: dict = {"status": "OK", "ip_address": "192.168.1.10", "active": True}


sentence = "Why do Omanis never get lost in the desert? Because even the dunes know the way to Muscat!"
list_of_words = sentence.split()
new_sentence = "-".join(list_of_words)

print(new_sentence)

counter = 0
while counter < len(name_of_team_members):
  print(name_of_team_members[counter])
  counter += 1

for name in name_of_team_members:
  print(name)

print(list(filter(lambda curr_name: "e" in curr_name, name_of_team_members)))

for i in range(0, 5):
  print(i)