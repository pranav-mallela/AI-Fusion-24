class ObstacleDetector:
    def __init__(self):
        self.obstacles = []
        self.safety_radius = 0.7

    def detect_nearby_obstacles(self, robot_position):
        near_obstacles = []
        for obstacle in self.obstacles:
            obstacle_position = obstacle['position']
            obstacle_radius = obstacle['radius'] + self.safety_radius
            distance = self.calculate_distance(robot_position, obstacle_position)
            if distance <= obstacle_radius:
                near_obstacles.append(obstacle)
        return near_obstacles

    @staticmethod
    def calculate_distance(position1, position2):
        dx = position1[0] - position2[0]
        dy = position1[1] - position2[1]
        dz = position1[2] - position2[2]
        distance = (dx**2 + dy**2 + dz**2) ** 0.5
        return distance


def main():
    # Initialize obstacle detector
    obstacle_detector = ObstacleDetector()

    # Dummy drone trajectory
    drone_trajectory = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]  # Example trajectory

    # Detect nearby obstacles for each position in the trajectory
    for position in drone_trajectory:
        near_obstacles = obstacle_detector.detect_nearby_obstacles(position)
        if near_obstacles:
            print("Nearby obstacles:", near_obstacles)


if __name__ == "__main__":
    main()
