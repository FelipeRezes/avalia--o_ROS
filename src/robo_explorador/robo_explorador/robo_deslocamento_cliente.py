import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from robo_interfaces.action import Deslocamento


class RoboDeslocamentoCliente(Node):
    def __init__(self):
        super().__init__('robo_deslocamento_cliente')
        self._client = ActionClient(self, Deslocamento, 'deslocamento')

    def feedback_cb(self, fb_msg):
        fb = fb_msg.feedback
        self.get_logger().info(
            f'Feedback: posicao atual ({fb.latitude_atual:.3f}, {fb.longitude_atual:.3f})')

    def enviar(self, lat, lon, vlat, vlon):
        self._client.wait_for_server()
        goal = Deslocamento.Goal()
        goal.latitude = lat
        goal.longitude = lon
        goal.velocidade_latitude = vlat
        goal.velocidade_longitude = vlon
        self.get_logger().info(f'Enviando meta: ({lat}, {lon}) vel=({vlat}, {vlon})')
        return self._client.send_goal_async(goal, feedback_callback=self.feedback_cb)


def main(args=None):
    rclpy.init(args=args)
    node = RoboDeslocamentoCliente()

    send_future = node.enviar(10.0, 5.0, 2.0, 1.0)
    rclpy.spin_until_future_complete(node, send_future)
    goal_handle = send_future.result()

    if not goal_handle.accepted:
        node.get_logger().info('Meta rejeitada.')
    else:
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(node, result_future)
        resultado = result_future.result().result
        node.get_logger().info(
            f'Distancia percorrida: {resultado.distancia_percorrida:.3f}')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
