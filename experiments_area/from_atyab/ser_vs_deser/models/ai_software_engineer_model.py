class Engineer():
  designation: str

  def __init__(self):
      self.name = "Anonymous"
      self.email = "anonymous@gmail.com"

  def get_name(self):
    return self.name

  def get_email(self):
    return self.email
  
  def activity_percent(self):
    return 50

class CivilEngineer(Engineer):
  def activity_percent(self):
    return 80

class SoftwareEngineer(Engineer):
  def activity_percent(self):
      return 10

if __name__ == "__main__":
  se = SoftwareEngineer()
  print(se.get_name())
  print(se.get_email())
  print(se.activity_percent())

  ce = CivilEngineer()
  print(ce.activity_percent())
