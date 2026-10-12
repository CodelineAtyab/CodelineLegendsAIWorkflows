import utils
from uuid import uuid4
# from utils import multiply as mul

def main():
    a, b = (1, 2)
    
    # dummy_student = {"name": "Anoymous", "id": -1, "email": "unknown"}
    dummy_data = [("name", "Anoymous"), ("id", -1), ("email", "unknown")]
    dummy_data = {k: v for k, v in dummy_data}
    print(dummy_data)

if __name__ == "__main__":
    main()