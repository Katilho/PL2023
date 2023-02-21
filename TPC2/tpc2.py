import re

while True:
    text = input("\nDigite o texto:\n")
    text = text.lower()
    regex = r"(\d+|on|off|=)" # Se for para somar os números individualmente, retira-se o "+" da regex.
    arr = re.findall(regex, text)
    # print(f"[DEBUG]Lista separada: {arr}")
    result = 0
    mode = 1 # 1 -> on; 0 -> off
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





