def compute():
    try:
        1 / 0
    # note: F841
    except Exception as error:
        pass
    leftover = 1
