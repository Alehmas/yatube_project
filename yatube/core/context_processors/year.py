import datetime as dt


def year(request):
    """Adds a variable with the current year."""
    return {'year': dt.datetime.now().year, }
