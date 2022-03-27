def yesNoToBool(yesNo: str) -> bool:
  if yesNo == "Y":
    return True
  elif yesNo == "N":
    return False
  else:
    raise ValueError(yesNo)
