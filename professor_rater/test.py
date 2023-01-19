import math

def round(x):
    if isinstance(x, int):
        return x
    ceiling = math.ceil(x)
    if ceiling - x > .5:
        return math.floor(x)
    elif ceiling - x <= .5:
        return ceiling

if __name__ == "__main__":
    print(round(3.5))
    print(round(3))
    print(round(3.49999))
    print(round(3.95))
    print(round(3.0))