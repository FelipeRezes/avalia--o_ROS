# Prova 1 - Topicos Especiais em Redes de Computadores (ROS 2)

Alunos: Alex Cristhian Lima de Medeiros e Felipe Rezes de Moura

Pacotes:
- `robo_interfaces` (ament_cmake / C++): msg `Monitoramento`, srv `ColetaMaterial`, action `Deslocamento`
- `robo_explorador` (ament_python): nos publisher, subscriber, servico e action

## Construir a imagem e subir o container

```bash
docker build -t robo_ros .
docker run -dit --name robo robo_ros
```

Para cada terminal, entrar no mesmo container (o ROS ja vem carregado):

```bash
docker exec -it robo bash
```

## Questoes 2, 5 e 8 (interfaces)

```bash
ros2 interface show robo_interfaces/msg/Monitoramento
ros2 interface show robo_interfaces/srv/ColetaMaterial
ros2 interface show robo_interfaces/action/Deslocamento
```

## Questoes 3 e 4 (topico) - um terminal para cada

```bash
ros2 run robo_explorador robo_topico_publish
ros2 run robo_explorador robo_topico_subscriber
```

## Questoes 6 e 7 (servico) - um terminal para cada

```bash
ros2 run robo_explorador robo_coleta_servidor
ros2 run robo_explorador robo_coleta_cliente
```

## Questoes 9, 10 e 11 (action)

```bash
ros2 run robo_explorador robo_deslocamento_servidor
ros2 run robo_explorador robo_deslocamento_cliente           # Q10: espera ate o fim
ros2 run robo_explorador robo_deslocamento_cliente_cancela   # Q11: cancela apos 5 s
```

## Depois de alterar o codigo

```bash
docker rm -f robo
docker build -t robo_ros .
docker run -dit --name robo robo_ros
```

Sem permissao de docker no computador? Troque `docker` por `podman`.
