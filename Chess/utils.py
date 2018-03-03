 

def str_repr(pos):
    return chr(ord('a') + pos[0]) + chr(ord('1') + pos[1])


def nbr_repr(pos):
    return (ord(pos[0]) - ord('a'), ord(pos[1]) - ord('1'))
