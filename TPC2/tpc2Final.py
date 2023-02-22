class Counter:
    def __init__(self):
        self.result = 0
        self.mode = 1
        
    def calculate(self, string):
        try:
            value = int(string)
            self.result += value * self.mode
        except ValueError:
            if string == "=":
                print(self.result)
            elif string == "on":
                self.mode = 1
            else:
                self.mode = 0


def process_string(string):
    # Initialize variables
    result = [] # DEBUG
    counter = Counter()
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
                counter.calculate(copy)
                result.append(copy)
        
        # Add buffer character to buffer string
        if char == "o":
            buffer = "o"
        elif char == "=":
            buffer = ""
            counter.calculate(char)
            result.append(char)
        elif curr_type == "number" or (char in "nf" and buffer == "o") or (char == "f" and buffer == "of"): 
            buffer += char
            if buffer == "on" or buffer == "off":
                counter.calculate(buffer)
                result.append(buffer)
                buffer = ""
        else:
            buffer = ""

        # Update previous type
        prev_type = curr_type
    
    # Add final buffer string to result list
    if buffer != "":
        result.append(buffer)
    
    return result # retorna as strings uteis utilizadas para o processo como forma de debug.


while True:
    text = input("Digite o texto:\n")
    debug_array = process_string(text)
    print(f"[DEBUG] -> {debug_array}")
