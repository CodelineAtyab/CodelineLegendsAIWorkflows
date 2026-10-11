import utils
# from utils import multiply as mul

def main():
    user_chat_history = ["Hi", "Want to know about Python"]
    utils.add_msg_to_chat_history(msg="I am done!", chat_history=user_chat_history)
    print(user_chat_history)

    user_chat_history = user_chat_history + ["One More Sentence", "Another Sentence"]
    print(user_chat_history)

    numbers = ("One", "Two", "Three")
    numbers = tuple(list(numbers) + ["Four"])
    print(numbers)
    
    # Lists are mutable
    # user_chat_history = ["Hi", "Want to know about Python", "why is it called a scripting language"]
    # user_chat_history[1] = "Want to know about C#"
    # user_chat_history.append("interpreter vs comp diff ?")

    # print(user_chat_history)

    # # Tuple
    # bot_chat_history = ("Hello I am GPT-5", "Its a programming language", "Because its interpreted")
  
    
    # print(mul(1,2))
    # print(utils.x)
    # print("This is the main module.")

if __name__ == "__main__":
    main()