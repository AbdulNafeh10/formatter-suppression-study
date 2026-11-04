def compute():
    try:
        1 / 0
    # noqa: F841
    except Exception as error:
        pass
    leftover=1
