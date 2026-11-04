def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F841
        pass
    leftover = 1
