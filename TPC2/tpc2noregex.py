def transform_string(string):
    # Initialize variables
    result = []
    buffer = ""
    prev_type = None
    string = string.lower()
    
    for char in string:

        curr_type = "number" if char.isdigit() else "letter"
        
        # To verify if the letter changed to num or char
        if curr_type != prev_type and buffer != "":
            copy = buffer # exact copy of buffer
            buffer = ""
            if prev_type == "number" or copy == "on" or copy == "off":
                result.append(copy)
        
        # Add buffer character to buffer string
        if char == "o":
            buffer = "o"
        if char == "=":
            result.append(char)
            buffer = ""
        elif curr_type == "number" or (char in "nf" and buffer == "o") or (char == "f" and buffer == "of"): 
            buffer += char
            if buffer == "on" or buffer == "off":
                result.append(buffer)
                buffer = ""
        else:
            buffer = ""

        # Update previous type
        prev_type = curr_type
    
    # Add final buffer string to result list
    if buffer != "":
        result.append(buffer)
    
    return result


while True:
    text = input("Digite o texto:\n")
    # text = text.lower()
    buffer = [] # to store the sequences of consecutive numbers.
    word = "" # to be used when checking for on or off

    arr = transform_string(text)
    print(f"[DEBUG] -> {arr}")
    mode = 1
    result = 0
    for s in arr:
        try:
            value = int(s)
            result += value * mode
        except ValueError:
            if s == "=":
                print(result)
                # result = 0
            elif s == "on":
                mode = 1
            else:
                mode = 0
    print()
