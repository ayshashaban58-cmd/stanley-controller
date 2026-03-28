import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path, Odometry
from ackermann_msgs.msg import AckermannDriveStamped
import numpy as np

class StanleyController(Node):
    def __init__(self):
        super().__init__('stanley_controller')

        # Params
        self.k = 0.6           # tuning parameter
        self.wheelbase = 2.5   # meters
        self.desired_speed = 3.0  
      
        # Subscribers
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.create_subscription(Path, '/path', self.path_callback, 10)

        # Publisher
        self.drive_pub = self.create_publisher(AckermannDriveStamped, '/drive', 10)

        self.path_x = []
        self.path_y = []

    def path_callback(self, msg):
        self.path_x = [pose.pose.position.x for pose in msg.poses]
        self.path_y = [pose.pose.position.y for pose in msg.poses]

    def odom_callback(self, msg):
        if not self.path_x:
            return

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # heading من quaternion
        q = msg.pose.pose.orientation
        yaw = self.quaternion_to_yaw(q)


        dx = np.array(self.path_x) - x
        dy = np.array(self.path_y) - y
        dists = np.hypot(dx, dy)
        target_idx = np.argmin(dists)

        target_x = self.path_x[target_idx]
        target_y = self.path_y[target_idx]

        path_heading = np.arctan2(
            self.path_y[min(target_idx+1, len(self.path_y)-1)] - target_y,
            self.path_x[min(target_idx+1, len(self.path_x)-1)] - target_x
        )

        # cross-track error
        error = np.sin(path_heading - yaw) * dists[target_idx]

        # Stanley control law
        heading_error = self.normalize_angle(path_heading - yaw)
        steering_angle = heading_error + np.arctan2(self.k * error, self.desired_speed)

        # Publish command
        drive_msg = AckermannDriveStamped()
        drive_msg.drive.steering_angle = float(steering_angle)
        drive_msg.drive.speed = float(self.desired_speed)
        self.drive_pub.publish(drive_msg)

    @staticmethod
    def quaternion_to_yaw(q):
        import math
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
        return math.atan2(siny_cosp, cosy_cosp)

    @staticmethod
    def normalize_angle(angle):
        while angle > np.pi:
            angle -= 2.0 * np.pi
        while angle < -np.pi:
            angle += 2.0 * np.pi
        return angle

def main(args=None):
    rclpy.init(args=args)
    node = StanleyController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
