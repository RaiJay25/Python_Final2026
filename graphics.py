# graphics.py

def world_to_screen_x(x, world_width, canvas_width):
    return (x / world_width) * canvas_width


def world_to_screen_y(y, world_height, canvas_height):
    return canvas_height - (y / world_height) * canvas_height


def draw(canvas, lander, platform_x, platform_width,
         world_width, world_height,
         canvas_width, canvas_height,
         thrust_on, game_over, message):

    canvas.delete("all")

    ground_y = world_to_screen_y(0, world_height, canvas_height)

    # ground
    canvas.create_rectangle(
        0, ground_y, canvas_width, canvas_height,
        fill="gray20", outline="gray20"
    )

    # platform
    platform_left = world_to_screen_x(platform_x - platform_width / 2, world_width, canvas_width)
    platform_right = world_to_screen_x(platform_x + platform_width / 2, world_width, canvas_width)

    canvas.create_rectangle(
        platform_left,
        ground_y - 12,
        platform_right,
        ground_y,
        fill="green",
        outline="white"
    )

    # lander
    lander_left = world_to_screen_x(lander.x - lander.width / 2, world_width, canvas_width)
    lander_right = world_to_screen_x(lander.x + lander.width / 2, world_width, canvas_width)
    lander_top = world_to_screen_y(lander.y + lander.height / 2, world_height, canvas_height)
    lander_bottom = world_to_screen_y(lander.y - lander.height / 2, world_height, canvas_height)

    canvas.create_rectangle(
        lander_left, lander_top, lander_right, lander_bottom,
        fill="white", outline="white"
    )

    # flame
    if thrust_on and not game_over:
        center_x = world_to_screen_x(lander.x, world_width, canvas_width)

        canvas.create_polygon(
            center_x - 8, lander_bottom,
            center_x + 8, lander_bottom,
            center_x, lander_bottom + 18,
            fill="orange",
            outline="yellow"
        )

    # text
    canvas.create_text(
        10, 20,
        text=f"x={lander.x:.2f}  y={lander.y:.2f}  vx={lander.vx:.2f}  vy={lander.vy:.2f}",
        fill="white",
        anchor="w"
    )

    if game_over:
        canvas.create_text(
            canvas_width / 2,
            80,
            text=message,
            fill="white"
        )