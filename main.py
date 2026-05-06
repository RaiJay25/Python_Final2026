# main.py
import random
import tkinter as tk

from lander import Lander


class LunarLanderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Lunar Lander")

        # window / canvas size
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # world size in meters
        self.world_width = 100.0
        self.world_height = 120.0

        # platform settings
        self.platform_width = 4.0
        self.platform_height_px = 12

        # simulation settings
        self.dt = 0.05
        self.running = True
        self.game_over = False
        self.message = ""

        # key states
        self.thrust_on = False
        self.move_left = False
        self.move_right = False

        # bind keys
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)

        self.reset_game()
        self.update_game()

    def reset_game(self):
        self.lander = Lander()

        # starting position
        self.lander.x = self.world_width / 2
        self.lander.y = 100.0
        self.lander.vx = 0.0
        self.lander.vy = 0.0

        # random platform position
        margin = 10.0
        self.platform_x = random.uniform(
            margin + self.platform_width / 2,
            self.world_width - margin - self.platform_width / 2
        )

        self.running = True
        self.game_over = False
        self.message = ""

        self.thrust_on = False
        self.move_left = False
        self.move_right = False

    def world_to_screen_x(self, x):
        return (x / self.world_width) * self.canvas_width

    def world_to_screen_y(self, y):
        return self.canvas_height - (y / self.world_height) * self.canvas_height

    def key_press(self, event):
        key = event.keysym.lower()

        if key == "space":
            self.thrust_on = True
        elif key in ["a", "left"]:
            self.move_left = True
        elif key in ["d", "right"]:
            self.move_right = True
        elif key == "r" and self.game_over:
            self.reset_game()
        elif key == "escape":
            self.root.destroy()

    def key_release(self, event):
        key = event.keysym.lower()

        if key == "space":
            self.thrust_on = False
        elif key in ["a", "left"]:
            self.move_left = False
        elif key in ["d", "right"]:
            self.move_right = False

    def get_horizontal_overlap(self):
        lander_left = self.lander.x - self.lander.width / 2
        lander_right = self.lander.x + self.lander.width / 2

        platform_left = self.platform_x - self.platform_width / 2
        platform_right = self.platform_x + self.platform_width / 2

        overlap_left = max(lander_left, platform_left)
        overlap_right = min(lander_right, platform_right)

        overlap = max(0.0, overlap_right - overlap_left)
        return overlap

    def check_touchdown(self):
        # bottom of lander touching ground
        return self.lander.y - self.lander.height / 2 <= 0

    def classify_landing(self):
        overlap = self.get_horizontal_overlap()
        touchdown_speed = abs(self.lander.vy)

        # clamp lander to ground
        self.lander.y = self.lander.height / 2
        self.lander.vx = 0.0
        self.lander.vy = 0.0

        # at least 75% of 2 m width must be over the platform
        required_overlap = 0.75 * self.lander.width

        if touchdown_speed > 5.0:
            return "Crash: landing speed was too high."
        elif overlap < required_overlap:
            return "Miss: not enough of the lander was over the platform."
        elif touchdown_speed <= 3.0:
            return "Successful landing!"
        else:
            return "Hard landing: too fast for a safe landing."

    def keep_lander_in_bounds(self):
        half_width = self.lander.width / 2

        if self.lander.x < half_width:
            self.lander.x = half_width
            self.lander.vx = 0.0
        elif self.lander.x > self.world_width - half_width:
            self.lander.x = self.world_width - half_width
            self.lander.vx = 0.0

    def draw(self):
        self.canvas.delete("all")

        # ground
        ground_y = self.world_to_screen_y(0)
        self.canvas.create_rectangle(
            0, ground_y, self.canvas_width, self.canvas_height,
            fill="gray20", outline="gray20"
        )

        # platform
        platform_left = self.world_to_screen_x(self.platform_x - self.platform_width / 2)
        platform_right = self.world_to_screen_x(self.platform_x + self.platform_width / 2)

        self.canvas.create_rectangle(
            platform_left,
            ground_y - self.platform_height_px,
            platform_right,
            ground_y,
            fill="green",
            outline="white"
        )

        # lander
        lander_left = self.world_to_screen_x(self.lander.x - self.lander.width / 2)
        lander_right = self.world_to_screen_x(self.lander.x + self.lander.width / 2)
        lander_top = self.world_to_screen_y(self.lander.y + self.lander.height / 2)
        lander_bottom = self.world_to_screen_y(self.lander.y - self.lander.height / 2)

        self.canvas.create_rectangle(
            lander_left, lander_top, lander_right, lander_bottom,
            fill="white", outline="white"
        )

        # flame when thrusting
        if self.thrust_on and not self.game_over:
            center_x = self.world_to_screen_x(self.lander.x)
            flame_top = lander_bottom
            flame_bottom = lander_bottom + 18

            self.canvas.create_polygon(
                center_x - 8, flame_top,
                center_x + 8, flame_top,
                center_x, flame_bottom,
                fill="orange",
                outline="yellow"
            )

        # info text
        info_text = (
            f"x = {self.lander.x:.2f} m    "
            f"y = {self.lander.y:.2f} m    "
            f"vx = {self.lander.vx:.2f} m/s    "
            f"vy = {self.lander.vy:.2f} m/s"
        )

        self.canvas.create_text(
            10, 20,
            text=info_text,
            fill="white",
            anchor="w",
            font=("Arial", 12)
        )

        self.canvas.create_text(
            10, 45,
            text="Controls: Space = thrust, A/D or arrows = move, R = restart",
            fill="white",
            anchor="w",
            font=("Arial", 12)
        )

        if self.game_over:
            self.canvas.create_text(
                self.canvas_width / 2,
                80,
                text=self.message,
                fill="white",
                font=("Arial", 18, "bold")
            )

    def update_game(self):
        if self.running and not self.game_over:
            self.lander.update(self.dt, self.thrust_on, self.move_left, self.move_right)
            self.keep_lander_in_bounds()

            if self.check_touchdown():
                self.message = self.classify_landing()
                self.game_over = True

        self.draw()
        self.root.after(int(self.dt * 1000), self.update_game)


def main():
    root = tk.Tk()
    game = LunarLanderGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()