def monkey_trouble(a_smile, b_smile):
    if a_smile and b_smile:
        return True
    return bool(not a_smile and not b_smile)
    ## The above can be shortened to:
    ##   return ((a_smile and b_smile) or (not a_smile and not b_smile))
    ## Or this very short version (think about how this is the same as the above)
    ##   return (a_smile == b_smile)
