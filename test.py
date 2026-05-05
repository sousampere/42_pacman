import random

import arcade
from src.entity.entity import Collectible
from src.entity.ghost import Ghost
from src.entity.pacgum import Pacgum
from src.entity.player import Player
from src.entity.super_pacgum import SuperPacgum


class MyGame(arcade.Window):
    def __init__(self) -> None:
        super().__init__(800, 600, "Mon Jeu ISP")
        self.entity_list: arcade.SpriteList = arcade.SpriteList()
        self.scene_entities: arcade.SpriteList = arcade.SpriteList()
        self.player = Player(spawn_point=(100, 100), speed=10.0)
        self.ghost = Ghost(spawn_point=(500, 300), speed=10.0)
        self.scene_entities.append(self.player)
        self.scene_entities.append(self.ghost)

        for _ in range(random.randint(5, 40)):
            pacgum = Pacgum((random.randint(10, 780), random.randint(10, 580)))
            self.entity_list.append(pacgum)
            self.scene_entities.append(pacgum)
        self.super_pacgum = SuperPacgum((200, 200))
        self.scene_entities.append(self.super_pacgum)
        self.entity_list.append(self.super_pacgum)
        self.entity_list.append(self.ghost)
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

    def on_update(self, delta_time) -> None:
        self.player.move(self.direction)
        self.scene_entities.update()
        hit_list: list[Collectible | Ghost] = arcade.check_for_collision_with_list(
            self.player, self.entity_list
        )

        for entities in hit_list:
            if isinstance(entities, Collectible):
                if entities.collect():
                    print(entities.score)
                    entities.activate_power()
                    entities.remove_from_sprite_lists()
            elif isinstance(entities, Ghost):
                if not entities.is_edible:
                    self.player.die()
                    entities.is_edible = True
                else:
                    print("meurt")
                    entities.die()

    def on_draw(self):
        self.clear()
        self.scene_entities.draw()


app = MyGame()
arcade.run()
