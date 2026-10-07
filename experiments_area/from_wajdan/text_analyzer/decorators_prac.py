def add_text_stats(given_fun):
    def decorated_func(*args, **kwargs):
        text = given_fun(*args, **kwargs)
        return text

    return decorated_func


@add_text_stats
def get_message(message):
    return message


print(get_message("Hello Wajdan"))