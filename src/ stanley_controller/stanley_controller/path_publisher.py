import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class PathPublisher(Node):
    def __init__(self):
        super().__init__('path_publisher')
        self.publisher_ = self.create_publisher(Path, '/path', 10)

      self.timer = self.create_timer(1.0, self.publish_path)
        

self.points = [
            (0.7187, 3.0803),
            (0.717, 2.9615),
            (0.7154, 2.8603),
            (0.7137, 2.744),
            (0.7125, 2.6652),
            (0.7112, 2.5802)
        ]

    def publish_path(self):
        path_msg = Path()
        path_msg.header.frame_id = "map" 
        path_msg.header.stamp = self.get_clock().now().to_msg()

        for x, y in self.points:
            pose = PoseStamped()
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0
            path_msg.poses.append(pose)

        self.publisher_.publish(path_msg)
        self.get_logger().info('Path Published!')

def main(args=None):
    rclpy.init(args=args)
    node = PathPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
