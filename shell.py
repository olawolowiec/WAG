import wag

while True:
    text = input('wag>')
    result, error = wag.run('<stdin>', text)

    if error: print(error.as_string())
    elif result: print(result)