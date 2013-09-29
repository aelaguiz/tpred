def load_words(path):
    f = open(path, "r")
    res = f.readlines()
    f.close()
    for w in res:
        w = w.lower().strip()
        yield w
