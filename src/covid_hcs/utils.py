def yes_no_to_bool(yes_no: str) -> bool:
    if yes_no == "Y":
        return True
    elif yes_no == "N":
        return False
    else:
        raise ValueError(yes_no)
