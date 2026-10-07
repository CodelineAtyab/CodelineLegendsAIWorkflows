def add_text_stats(given_fun):
    def decorated_func(*args, **kwargs):
        text = given_fun(*args, **kwargs)
        
        # Count words
        words = len(text.split())
        # Count spaces
        spaces = text.count(" ")
        
        # Count uppercase letters A-Z
        uppercase = 0
        for char in text:
            if "A" <= char <= "Z":
                uppercase += 1

        final_msg = (
            f"[No. of Words: {words}, "
            f"No. of Spaces: {spaces}, "
            f"No. of Uppercase Chars: {uppercase}] "
        )
        final_msg = final_msg + text
        return final_msg

    return decorated_func


@add_text_stats
def get_message(message):
    return message


print(get_message(message="Hello Wajdan"))