import arcade
from src.entity.player import Player


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Mon Jeu ISP")
        self.player = Player(spawn_point=(100, 100), speed=10.0)
        self.scene_entities = arcade.SpriteList()
        self.scene_entities.append(self.player)
        self.direction = (0, 0)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.direction = (0, 1)
        elif key == arcade.key.DOWN:
            self.direction = (0, -1)
        elif key == arcade.key.RIGHT:
            self.direction = (1, 0)
        elif key == arcade.key.LEFT:
            self.direction = (-1, 0)

    def on_key_release(self, key, modifiers):
        if key in (
            arcade.key.UP,
            arcade.key.DOWN,
            arcade.key.LEFT,
            arcade.key.RIGHT,
        ):
            self.direction = (0, 0)

    def on_update(self, delta_time):
        self.player.move(self.direction)
        self.scene_entities.update()

    def on_draw(self):
        self.clear()
        self.scene_entities.draw()


app = MyGame()
arcade.run()
