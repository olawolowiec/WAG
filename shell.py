import wag

while True:
    text = input('wag>')
    result, error = wag. run(text)

    if error: print(error.as_string())
    else: print(result)