import math

def reward_function(params):

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

    #TODO write rewards for the direction the car is heading
    # I think we will want a positive reinforcement if the car is heading
    # in the direction of the future waypoint. It will have negative reinforcement
    # if the car is heading too far away from the direction of the future waypoint.
    # It will have a large reward for going fast if the future waypoint is less than a X degree
    # turn (or something of the like) from the current position (or the current waypoint.)


    #----We can use the steering penalty threshold below if we desire, unsure if we should in this iteration ----

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 22

    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    return float(reward)
