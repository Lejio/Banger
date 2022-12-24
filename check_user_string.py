def check_user_string(user_input, isnum):

  if (isnum):

    if (len(user_input) == 0):

      return False

    elif not (user_input[1].isdigit()):

      return False

    else:

      return True

  else:

    if (len(user_input) == 0):

      return False

    else:

      return True
