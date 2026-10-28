import random

import rclpy
from rclpy.node import Node

from robo_interfaces.srv import ColetaMaterial


class RoboColetaCliente(Node):
    def __init__(self):
        super().__init__('robo_coleta_cliente')
        self.cli = self.create_client(ColetaMaterial, 'coleta_material')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando o servico coleta_material...')

    def enviar(self):
        req = ColetaMaterial.Request()
        req.profundidade = random.uniform(0.1, 0.5)
        self.get_logger().info(f'Solicitando coleta a profundidade {req.profundidade:.3f}')
        return self.cli.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    node = RoboColetaCliente()
    future = node.enviar()
    rclpy.spin_until_future_complete(node, future)
    resposta = future.result()
    if resposta.sucesso:
        node.get_logger().info('Coleta bem sucedida!')
    else:
        node.get_logger().info('Coleta NAO foi bem sucedida.')
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()