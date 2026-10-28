import random

import rclpy
from rclpy.node import Node

from robo_interfaces.msg import Monitoramento


class RoboTopicoPublish(Node):

    def __init__(self):
        super().__init__('robo_topico_publish')
        self.publisher_ = self.create_publisher(Monitoramento, 'monitoramento', 10)
        self.timer = self.create_timer(1.0, self.publicar)

    def publicar(self):
        msg = Monitoramento()
        msg.nivel_oxigenio = random.uniform(1.0, 100.0)
        msg.temperatura = random.uniform(1.0, 100.0)
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Publicando: oxigenio={msg.nivel_oxigenio:.2f} temperatura={msg.temperatura:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = RoboTopicoPublish()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
