# physics.py
# Basic physics helpers for the lunar lander project

GRAVITY = -1.62  # m/s^2, moon gravity


def euler_step(position, velocity, acceleration, dt):
    """
    Update position and velocity using Euler's Method.
    Returns the new position and new velocity.
    """
    new_position = position + velocity * dt
    new_velocity = velocity + acceleration * dt
    return new_position, new_velocity


def vertical_acceleration(thrust_on, thrust_power):
    """
    Computes vertical acceleration from gravity and optional upward thrust.
    thrust_on: True if the player is firing the engine
    thrust_power: upward acceleration from engine in m/s^2
    """
    if thrust_on:
        return GRAVITY + thrust_power
    return GRAVITY


def horizontal_acceleration(move_left, move_right, move_power):
    """
    Computes horizontal acceleration from player input.
    """
    if move_left and not move_right:
        return -move_power
    if move_right and not move_left:
        return move_power
    return 0.0