from Character import Character


class Enemy(Character):
    def __init__(self, x, y, start_image, images, group_all_sprite) -> None:
        super().__init__(x, y, start_image, images, group_all_sprite)
