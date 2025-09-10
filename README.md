# Guia Passo a Passo: Docker Swarm + Stack

## 1. Iniciando o Swarm e a Rede Overlay

```bash
docker swarm init
docker network create --driver overlay app-net
```

## 2. Deploy da Stack

```bash
docker stack deploy -c stack.yml appdemo
```

## 3. Verificando os Serviços

```bash
docker service ls
```

## 4. Escalando os Serviços

```bash
docker service scale appdemo_frontend=5
docker service scale appdemo_backend=8
```

## 5. Acessando a Aplicação

```bash
curl http://localhost:8080
```

## 6. Finalizando/Derrubando a Stack

```bash
docker stack rm appdemo
```