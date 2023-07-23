import math

def reward_function(params):

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    abs_steering = abs(params['steering_angle']) # Only need the absolute steering angle
    speed = params['speed']

    #Threshold the car should aim for the target waypoint
    direction_threshold = 10
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15
    future_waypoint = 5
    num_waypoints = len(waypoints)
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

    #reward for going fast when heading towards future waypoint
    if direction_diff < direction_threshold and speed > 3.75:
        reward *= 2.2
    elif direction_diff < direction_threshold * 2 and speed > 2.75:
        reward *= 1.3
    elif direction_diff > 70 and speed > 2.75:
        reward *= 0.1

    #Punish if car is too far from center and likely off track
    if distance_from_center > track_width / 2:
        reward *= 0.1
    elif distance_from_center > track_width / 1.8:
        reward *= 0.0001

    reward = speed_bonus + steering_bonus + heading_bonus
    
    return float(reward)

def speed_bonus(param):
        #reward just for going fast
    if speed > 3.5:
        reward *= 1.2
    return 0

def steering_bonus(param):
    return 0

def heading_bonus(param):
    return 0

