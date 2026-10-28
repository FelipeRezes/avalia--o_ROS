import random

import rclpy
from rclpy.node import Node

from robo_interfaces.srv import ColetaMaterial


class RoboColetaServidor(Node):
    """Simula o robo: coleta bem sucedida com probabilidade de 70%."""

    def __init__(self):
        super().__init__('robo_coleta_servidor')
        self.srv = self.create_service(
            ColetaMaterial, 'coleta_material', self.callback)
        self.get_logger().info('Servico coleta_material pronto.')

    def callback(self, request, response):
        sorteio = random.random()  # numero aleatorio entre 0 e 1
        if sorteio <= 0.7:
            response.sucesso = True   # probabilidade de 70%
        else:
            response.sucesso = False
        self.get_logger().info(
            f'Requisicao: profundidade={request.profundidade:.3f} | '
            f'sorteio={sorteio:.3f} (<= 0.7?) -> sucesso={response.sucesso}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = RoboColetaServidor()
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