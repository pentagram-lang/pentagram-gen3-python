def loop(func):
    try:
        while True:
            try:
                text = input("> ")
            except KeyboardInterrupt:
                print()
                continue
            print(func(text))
    except EOFError:
        print()
