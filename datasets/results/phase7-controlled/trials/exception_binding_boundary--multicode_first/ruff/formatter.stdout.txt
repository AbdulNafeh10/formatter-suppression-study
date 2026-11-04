def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F401, F821, F841
        pass
    leftover = 1
