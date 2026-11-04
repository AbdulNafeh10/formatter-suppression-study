def compute():
    try:
        1 / 0
    except Exception as error:  # note: F841
        pass
    leftover=1
