def collision(object_a, object_b):
    return object_a.get_x() < object_b.get_x() + object_b.get_size() and object_a.get_x() + object_b.get_size() > object_b.get_x() and object_a.get_y() < object_b.get_y() + object_b.get_size() and object_a.get_y() + object_a.get_size() > object_b.get_y()

def snake_collision(object_a, object_b):
    return object_a.get_x() < object_b.get_x() + object_b.get_size() - 10 and object_a.get_x() + object_b.get_size() - 10 > object_b.get_x() and object_a.get_y() < object_b.get_y() + object_b.get_size() -10 and object_a.get_y() + object_a.get_size() -10 > object_b.get_y()
