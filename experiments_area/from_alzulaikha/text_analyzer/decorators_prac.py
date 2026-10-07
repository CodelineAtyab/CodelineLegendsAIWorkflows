from decorators import add_text_stats


@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


print(get_news())