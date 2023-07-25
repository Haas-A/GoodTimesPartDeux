import math

def reward_function(params):

    # Read input parameters
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering_angle = params['steering_angle']
    speed = params['speed']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']

    speed_weight = 2
    heading_weight = 4
    steering_weight = 5
    off_track_weight = 8

    future_waypoint = 5
    target_waypoint_index = closest_waypoints[0] + future_waypoint
    target_waypoint_index = target_waypoint_index % len(waypoints)
    target_waypoint = waypoints[target_waypoint_index]
    prev_waypoint = waypoints[closest_waypoints[0]]
    reward = 1.0

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(target_waypoint[1] - prev_waypoint[1], target_waypoint[0] - prev_waypoint[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    if distance_from_center > track_width / 2:
        return float(-2)
    
    reward = speed_bonus(speed_weight, speed) + heading_bonus(heading_weight, direction_diff)
    reward = reward + steering_bonus(steering_weight, direction_diff, steering_angle) + off_track_bonus(off_track_weight, distance_from_center, track_width)
    
    return float(reward)

def speed_bonus(speed_weight, speed):
    max = 6
    delta = max - speed
    delta_sq = delta * delta
    max_sq = max * max
    bonus = max_sq / delta_sq
    return speed_weight * bonus

def heading_bonus(heading_weight, direction_diff):
    sqrt = math.sqrt(1 + (direction_diff * direction_diff))
    bonus = 5 / sqrt
    return heading_weight * bonus

def steering_bonus(steering_weight, direction_diff, steering_angle):
    delta = abs(steering_angle - direction_diff) / 180
    return delta * steering_weight

def off_track_bonus(off_track_weight, distance_from_center, track_width):
    leeway = track_width * 0.4
    bonus = 0
    if distance_from_center > leeway:
        temp = 1 / distance_from_center
        bonus = temp - 3
    return bonus * off_track_weight