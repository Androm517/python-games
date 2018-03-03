 

def str_repr(pos):
    return chr(ord('a') + pos[1]) + chr(ord('1') + pos[0])


def nbr_repr(pos):
    return ( ord(pos[1]) - ord('1'), ord(pos[0]) - ord('a'))
