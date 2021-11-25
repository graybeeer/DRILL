def collide(a_get_col, b_get_col):
    left_a, bottom_a, right_a, top_a = a_get_col
    left_b, bottom_b, right_b, top_b = b_get_col

    if left_a > right_b: return False
    elif right_a < left_b: return False
    elif top_a < bottom_b: return False
    elif bottom_a > top_b: return False

    return True