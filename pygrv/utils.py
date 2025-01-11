def get_arg(arg, default):
    return default if arg is None else arg

def to_ordinal(n):
    s = str(n)
    if 10 <= n % 100 <= 20:
        return s + "th"
    last = n % 10
    if last == 1:
        return s + "st"
    if last == 2:
        return s + "nd"
    if last == 3:
        return s + "rd"
    return s + "th"

