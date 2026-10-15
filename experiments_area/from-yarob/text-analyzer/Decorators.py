def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):
    def add_text_stats(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            word_count = len(text.split())
            space_count = text.count(" ")
            uppercase_count = sum(1 for char in text if char.isupper())

            if count_words == True and count_spaces ==True and count_uppercase_chars ==True:
                return f"[No. of Words: {word_count}, No. of Spaces: {space_count}, No. of Uppercase Chars: {uppercase_count}]{text}"

            elif count_words ==True and count_spaces ==False and count_uppercase_chars ==True:
             return f"[No. of Words: {word_count}, No. of Uppercase Chars: {uppercase_count}]{text}"

            elif count_words ==False and count_spaces ==False and count_uppercase_chars ==True:
                return f"[No. of Uppercase Chars: {uppercase_count}]{text}"


            elif count_words ==False and count_spaces ==False and count_uppercase_chars ==False:
                 return f"{text}"
        return wrapper
    return add_text_stats



def get_news_full_stats():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True)
def get_news_with_analysis():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=True, count_spaces=False, count_uppercase_chars=True)
def get_news_with_partial_analysis():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=True)
def get_news_with_spaces_only():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False)
def get_news_without_analysis():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=False)
def get_news_without_word_count():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


print(get_news_with_analysis())
print(get_news_with_partial_analysis())
print(get_news_with_spaces_only())
print(get_news_without_analysis())
print(get_news_without_word_count())


