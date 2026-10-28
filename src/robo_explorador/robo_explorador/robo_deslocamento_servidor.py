import math
import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node

from robo_interfaces.action import Deslocamento


class RoboDeslocamentoServidor(Node):

    def __init__(self):
        super().__init__('robo_deslocamento_servidor')
        self.lat = 0.0
        self.lon = 0.0
        self._server = ActionServer(
            self, Deslocamento, 'deslocamento',
            execute_callback=self.execute,
            goal_callback=self.on_goal,
            cancel_callback=self.on_cancel)
        self.get_logger().info('Action server deslocamento pronto em (0.0, 0.0).')

    def on_goal(self, goal_request):
        return GoalResponse.ACCEPT

    def on_cancel(self, goal_handle):
        self.get_logger().info('Cancelamento solicitado.')
        return CancelResponse.ACCEPT

    def execute(self, goal_handle):
        goal = goal_handle.request
        result = Deslocamento.Result()
        result.distancia_percorrida = 0.0

        # sucesso apenas se a localizacao for diferente da atual
        if goal.latitude == self.lat and goal.longitude == self.lon:
            self.get_logger().info('Localizacao igual a atual: meta abortada.')
            goal_handle.abort()
            return result

        vlat = abs(goal.velocidade_latitude)
        vlon = abs(goal.velocidade_longitude)
        if (goal.latitude != self.lat and vlat == 0.0) or \
                (goal.longitude != self.lon and vlon == 0.0):
            self.get_logger().info('Velocidade nula em eixo que precisa se mover: abortada.')
            goal_handle.abort()
            return result

        distancia = 0.0
        feedback = Deslocamento.Feedback()

        while (self.lat, self.lon) != (goal.latitude, goal.longitude):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.distancia_percorrida = distancia
                self.get_logger().info(f'Cancelado. Distancia percorrida: {distancia:.3f}')
                return result

            time.sleep(1.0)

            dlat = self._passo(self.lat, goal.latitude, vlat)
            dlon = self._passo(self.lon, goal.longitude, vlon)
            self.lat += dlat
            self.lon += dlon
            distancia += math.hypot(dlat, dlon)

            feedback.latitude_atual = self.lat
            feedback.longitude_atual = self.lon
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'Posicao atual: ({self.lat:.3f}, {self.lon:.3f})')

        goal_handle.succeed()
        result.distancia_percorrida = distancia
        self.get_logger().info(f'Chegou ao destino. Distancia: {distancia:.3f}')
        return result

    @staticmethod
    def _passo(atual, alvo, velocidade):
        falta = alvo - atual
        if abs(falta) <= velocidade:
            return falta
        return math.copysign(velocidade, falta)


def main(args=None):
    rclpy.init(args=args)
    node = RoboDeslocamentoServidor()
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
