def decorator_with_starts_repeat(repeat):

    def decorate_with_stars(given_fun):
        def decorated_func(*args, **kwargs):
            final_msg = ""
            final_msg = final_msg + "**********************\n"

            for _ in range(repeat):
                final_msg = final_msg + given_fun(*args, **kwargs) + "\n"

            final_msg = final_msg + "**********************\n"
            return final_msg

        return decorated_func

    return decorate_with_stars


@decorator_with_starts_repeat(repeat=5)
def greet_opal_2(pre_message, message, post_message):
    return pre_message + message + post_message


print(greet_opal_2("START! ", "OPAL-2 Is doing great!!!", " DONE!!!"))

# @decorate_with_stars
# def get_lab_theme_info():
#     return "The Lab is White & Blue"

# @decorate_with_stars
# def get_team_feedback_of_python():
#     return "Python seems funny!"


# new_func = decorate_with_stars(greet_opal_2)
# new_func2 = decorate_with_stars(get_lab_theme_info)
# new_func3 = decorate_with_stars(get_team_feedback_of_python)

# print(new_func())
# print(new_func2())
# print(new_func3())
