import math

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    off_track = params['is_offtrack']
    abs_steering = abs(params['steering_angle']) # Only need the absolute steering angle
    speed = params['speed']

    num_waypoints = len(waypoints)
    target_waypoint_index = closest_waypoints[0] + 5
    target_waypoint_index = target_waypoint_index % len(waypoints)
    target_waypoint = waypoints[target_waypoint_index]
    prev_waypoint = waypoints[closest_waypoints[0]]
    direction_threshold = 10
    reward = 1.0

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(target_waypoint[1] - prev_waypoint[1], target_waypoint[0] - prev_waypoint[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    if off_track:
        if direction_diff > direction_threshold * 0.5:
            reward *= 0.2
    else:
        if direction_diff > direction_threshold:
            reward *= 0.4
        elif direction_diff > direction_threshold * .75:
            reward *= 0.6
        elif direction_diff > direction_threshold * 0.5:
            reward *= 0.8


    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1 and direction_diff < direction_threshold * 7 and speed > 3:
        reward *= 4
    elif distance_from_center <= marker_2:
        reward = reward - reward - 0.025
    elif distance_from_center <= marker_3:
        reward = reward - 0.1
    else:
        reward = reward - 0.25  # likely crashed/ close to off track

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 22

    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)
