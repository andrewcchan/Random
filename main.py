from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.label import Label
import random

class Enemy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.8, 0.2, 0.2, 1)  # Red color for enemies
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Bullet(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 0, 1)  # Yellow color for bullets
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Barricade(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.health = 100.0
        with self.canvas:
            # The barricade structure
            Color(0.6, 0.3, 0.1, 1)  # Brown color
            self.rect = Rectangle(pos=self.pos, size=self.size)

            # The health bar
            Color(0.8, 0, 0, 1)  # Red for health background
            self.health_bg = Rectangle()
            Color(0, 0.8, 0, 1)  # Green for health
            self.health_bar = Rectangle()
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        health_bar_pos = (self.x + 5, self.y + 5)
        health_bar_size = (self.width - 10, self.height - 10)
        self.health_bg.pos = health_bar_pos
        self.health_bg.size = health_bar_size
        health_width = health_bar_size[0] * (self.health / 100.0)
        self.health_bar.pos = health_bar_pos
        self.health_bar.size = (health_width, health_bar_size[1])

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        self.update_rect()  # Update the health bar


class Player(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0, 0.8, 0.4, 1)  # A bright green color for the player
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class GameWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_over = False
        self.enemies = []
        self.bullets = []

        self.barricade = Barricade(size_hint=(None, None), size=(self.width, 40))
        self.add_widget(self.barricade)

        self.player = Player(size_hint=(None, None), size=(50, 80))
        self.add_widget(self.player)
        self.current_lane = 'left'
        Window.bind(on_resize=self.on_window_resize)
        self.update_canvas()
        Clock.schedule_interval(self.spawn_enemy, 2.0)
        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Background
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Lanes
            Color(0.3, 0.3, 0.3, 1) # Slightly lighter grey
            lane_width = self.width * 0.4
            # Left Lane
            Rectangle(pos=(0, 0), size=(lane_width, self.height))
            # Right Lane
            Rectangle(pos=(self.width - lane_width, 0), size=(lane_width, self.height))

        self.barricade.size = (self.width, 40)
        self.barricade.update_rect()
        self.update_player_pos()

    def update_player_pos(self):
        lane_width = self.width * 0.4
        if self.current_lane == 'left':
            self.player.x = lane_width / 2 - self.player.width / 2
        else: # right lane
            self.player.x = self.width - lane_width + (lane_width / 2 - self.player.width / 2)
        self.player.y = self.barricade.height # A small margin from the bottom

    def on_window_resize(self, window, width, height):
        self.update_canvas()

    def on_touch_down(self, touch):
        self.touch_start_x = touch.x
        # Allow touch to be handled by children if any
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.game_over:
            return super().on_touch_up(touch)
        dx = touch.x - self.touch_start_x
        if abs(dx) > 50:  # Swipe threshold
            if dx > 0 and self.current_lane == 'left':  # Swipe right
                self.current_lane = 'right'
                self.update_player_pos()
            elif dx < 0 and self.current_lane == 'right':  # Swipe left
                self.current_lane = 'left'
                self.update_player_pos()
        else:  # It's a tap
            self.shoot_bullet()
        return super().on_touch_up(touch)

    def shoot_bullet(self):
        if self.game_over:
            return
        bullet = Bullet(size_hint=(None, None), size=(10, 30))
        bullet.x = self.player.center_x - bullet.width / 2
        bullet.y = self.player.top

        self.add_widget(bullet)
        self.bullets.append(bullet)

        # Animate the bullet
        anim = Animation(y=self.height, duration=1.5)
        anim.bind(on_complete=self.on_bullet_complete)
        anim.start(bullet)

    def on_bullet_complete(self, animation, bullet):
        if bullet.parent:
            self.remove_widget(bullet)
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def spawn_enemy(self, dt):
        if self.game_over:
            return
        enemy = Enemy(size_hint=(None, None), size=(50, 50))
        lane = random.choice(['left', 'right'])
        lane_width = self.width * 0.4

        if lane == 'left':
            enemy.x = lane_width / 2 - enemy.width / 2
        else:
            enemy.x = self.width - lane_width + (lane_width / 2 - enemy.width / 2)
        enemy.y = self.height

        self.add_widget(enemy)
        self.enemies.append(enemy)

        anim = Animation(y=self.barricade.height, duration=5.0)
        anim.bind(on_complete=self.on_enemy_complete)
        anim.start(enemy)

    def on_enemy_complete(self, animation, enemy):
        if not self.game_over:
            self.barricade.take_damage(10)
            if self.barricade.health <= 0:
                self.end_game()

        if enemy.parent:
            self.remove_widget(enemy)
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def update(self, dt):
        if self.game_over:
            return

        bullets_to_remove = []
        enemies_to_remove = []

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.collide_widget(enemy):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)

        for bullet in bullets_to_remove:
            self.remove_widget(bullet)
            self.bullets.remove(bullet)

        for enemy in enemies_to_remove:
            self.remove_widget(enemy)
            self.enemies.remove(enemy)

    def end_game(self):
        self.game_over = True
        Clock.unschedule(self.spawn_enemy)
        game_over_label = Label(text="Game Over", font_size='40sp',
                                center_x=self.width / 2, center_y=self.height / 2)
        self.add_widget(game_over_label)

class LaneZeroApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    LaneZeroApp().run()
