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

# Docker Swarm Demo: Frontend + Backend com Balanceamento e Scaling

## Visão Geral

Este projeto demonstra a implantação de uma aplicação web composta por **frontend** e **backend** em um cluster Docker Swarm, evidenciando:
- **Escala horizontal** (múltiplas réplicas de cada serviço)
- **Balanceamento de carga automático** do Swarm
- **Comunicação via rede overlay**
- **Parâmetros de configuração simulando configs/secrets**
- **Disponibilidade durante updates e scaling**
- **Documentação detalhada para fácil reprodução**

---

## Topologia da Solução

- **Serviço frontend:**  
  - Python Flask  
  - Responde na porta **8080** (exposta)  
  - Identifica a instância pela chave `"frontend_host"`  
  - Chama o backend, retorna também o hostname da réplica do backend
  - Mensagem customizável e chave fake via variáveis de ambiente

- **Serviço backend:**  
  - Python Flask  
  - NÃO expõe portas externas  
  - Retorna hostname/container-id no endpoint `/` (campo `"backend_host"`)

- **Rede overlay:**  
  - Ambos os serviços estão na rede `app-net` (Docker Swarm Overlay Network)

- **Configs/Secrets (opcional):**  
  - Mensagem (`MESSAGE`) e chave fake (`FAKE_KEY`) passadas como variáveis de ambiente para o frontend

---

## Pré-requisitos

- Docker e Docker Compose instalados
- Docker Hub para envio das imagens (altere `seu-usuario` para seu usuário Docker Hub)

---

## Estrutura dos Arquivos

```
.
├── backend.py
├── frontend.py
├── Dockerfile.backend
├── Dockerfile.frontend
├── stack.yml
└── README.md
```

---

## Passo a Passo

### 1. Inicializar o Docker Swarm e a rede overlay

```bash
docker swarm init
docker network create --driver overlay app-net
```

### 2. Build e Push das Imagens para o Docker Hub

**Backend:**
```bash
docker build -f Dockerfile.backend -t seu-usuario/backend-app:latest .
docker push seu-usuario/backend-app:latest
```

**Frontend:**
```bash
docker build -f Dockerfile.frontend -t seu-usuario/frontend-app:latest .
docker push seu-usuario/frontend-app:latest
```

### 3. Deploy da Stack

```bash
docker stack deploy -c stack.yml appdemo
```

### 4. Verificando os Serviços

```bash
docker service ls
docker service ps appdemo_frontend
docker service ps appdemo_backend
```

### 5. Acessando a Aplicação

Acesse várias vezes em seu navegador ou use cURL:

```bash
curl http://localhost:8080
```

**Exemplo de resposta:**
```json
{
  "frontend_host": "frontend-xyz123",
  "mensagem": "Olá do frontend!",
  "fake_key": "chave-fake-demo",
  "backend_response": {
    "backend_host": "backend-abc456"
  }
}
```
- O valor de `frontend_host` mudará conforme a réplica do frontend que responder.
- O valor de `backend_host` mudará conforme a réplica do backend que for chamada internamente.
- Isso evidencia o **balanceamento de carga** do Swarm.

### 6. Escalonamento Dinâmico (Scaling)

Aumente ou diminua as réplicas dos serviços em tempo real:

```bash
docker service scale appdemo_frontend=5
docker service scale appdemo_backend=8
```
- O serviço permanece acessível durante o scaling.
- O balanceamento se ajusta automaticamente ao novo número de réplicas.

### 7. Atualizações (Updates)

Você pode atualizar a stack (por exemplo, reconstruindo a imagem e redeployando) e a aplicação continuará acessível graças ao **rolling update** do Swarm:

```bash
docker stack deploy -c stack.yml appdemo
```

### 8. Visualização via Portainer (opcional)

Para visualizar os serviços, containers e rede do Swarm em interface gráfica:

```bash
docker service create \
  --name portainer \
  --publish 9000:9000 \
  --constraint 'node.role == manager' \
  --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  portainer/portainer-ce
```
Acesse: [http://localhost:9000](http://localhost:9000)

### 9. Finalizando (Remover tudo)

```bash
docker stack rm appdemo
docker service rm portainer
```

---

## Como Reproduzir os Testes de Balanceamento

1. **Acesse** o frontend repetidas vezes (navegador ou cURL).
2. Observe a alternância do campo `"frontend_host"` na resposta: cada acesso pode ser atendido por uma réplica diferente.
3. O campo `"backend_host"` dentro de `"backend_response"` também alterna, mostrando que o frontend está chamando diferentes réplicas do backend internamente.
4. Durante e após o scaling (`docker service scale ...`), continue acessando e veja o balanceamento se adaptar ao novo número de réplicas.

---

## Arquivo Compose para Swarm (stack.yml)

```yaml
version: "3.8"
services:
  backend:
    image: seu-usuario/backend-app:latest
    networks:
      - app-net
    deploy:
      replicas: 5

  frontend:
    image: seu-usuario/frontend-app:latest
    networks:
      - app-net
    ports:
      - "8080:8080"
    environment:
      - BACKEND_HOST=backend:5000
      - MESSAGE=Olá do frontend!
      - FAKE_KEY=chave-fake-demo
    deploy:
      replicas: 3

networks:
  app-net:
    driver: overlay
```

---

## Referência dos Códigos

**backend.py**
```python
from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def index():
    return {
        "backend_host": socket.gethostname()
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**frontend.py**
```python
from flask import Flask
import requests
import socket
import os

BACKEND_HOST = os.environ.get("BACKEND_HOST", "backend:5000")
MESSAGE = os.environ.get("MESSAGE", "Olá do frontend!")
FAKE_KEY = os.environ.get("FAKE_KEY", "chave-fake-demo")

app = Flask(__name__)

@app.route("/")
def index():
    try:
        backend_response = requests.get(f"http://{BACKEND_HOST}").json()
    except Exception as e:
        backend_response = {"error": str(e)}
    return {
        "frontend_host": socket.gethostname(),
        "mensagem": MESSAGE,
        "fake_key": FAKE_KEY,
        "backend_response": backend_response
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

**Dockerfile.backend**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY backend.py /app/
RUN pip install flask
CMD ["python", "backend.py"]
```

**Dockerfile.frontend**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY frontend.py /app/
RUN pip install flask requests
CMD ["python", "frontend.py"]
```

---

## Dúvidas?  
Abra uma issue ou entre em contato!


## 🛠️ Soluções para Problemas Comuns (Docker + WSL)

Se você encontrar problemas ao rodar este projeto com Docker no WSL (Ubuntu), siga este checklist e dicas de troubleshooting:

### 1. **Docker Desktop está rodando?**
- Certifique-se que o Docker Desktop está aberto no Windows e o ícone da baleia aparece na bandeja do sistema.
- Caso não esteja, abra o Docker Desktop antes de rodar qualquer comando Docker no Ubuntu.

---

### 2. **Ubuntu está integrado ao Docker Desktop?**
- Abra o Docker Desktop → Settings (⚙️) → **Resources** → **WSL Integration**
- Certifique-se que a sua distribuição (`Ubuntu`) está ativada (switch azul).  
- Se não aparecer, talvez precise reinstalar o Ubuntu pelo WSL.

---

### 3. **Verifique se está no diretório certo**
- No Ubuntu, acesse a pasta do projeto:
  ```bash
  cd /mnt/c/Users/SEU_USUARIO/SEU_CAMINHO/Projeto
  ```

---

### 4. **Erro: “This node is already part of a swarm”**
- Se rodar `docker swarm init` e aparecer esse erro, significa que o swarm já está iniciado.
- **Solução:** Pule este passo e siga para o deploy do stack.

---

### 5. **Erro: “port 'XXXX' is already in use by service...”**
- Significa que já existe um serviço Docker usando essa porta.
- **Soluções:**
  - Remova o serviço antigo:
    ```bash
    docker service ls           # Veja o nome do serviço
    docker service rm NOME_DO_SERVICO
    ```
  - Ou, altere a porta no seu `stack.yml` para uma porta livre (ex: 8081:8080).

---

### 6. **Nada aparece ao acessar o navegador**
- Confirme que o serviço frontend está rodando:
  ```bash
  docker stack services NOME_DO_STACK
  ```
- Veja os logs para mensagens de erro:
  ```bash
  docker service logs NOME_DO_STACK_frontend
  ```
- Certifique-se que está acessando a porta correta (ex: http://localhost:8080).

---

### 7. **Reiniciar tudo (limpar e subir do zero)**
```bash
docker stack rm NOME_DO_STACK
docker swarm leave --force
docker swarm init
docker stack deploy -c stack.yml NOME_DO_STACK
```

---

### 8. **Docker não reconhecido no Ubuntu**
- Certifique-se de usar o terminal do Ubuntu (não PowerShell/CMD).
- O comando `docker --version` deve funcionar no Ubuntu.
- Se der erro, reabra o Docker Desktop e o Ubuntu.

---

### 9. **Atenção com as pastas**
- Não coloque seus arquivos em `\\wsl.localhost\docker-desktop\...`
- Use sempre `/mnt/c/...` no Ubuntu ou pastas normais do Windows.

---

### 10. **Comandos úteis**

- Subir o stack:
  ```bash
  docker stack deploy -c stack.yml NOME_DO_STACK
  ```
- Ver serviços:
  ```bash
  docker stack services NOME_DO_STACK
  ```
- Ver containers:
  ```bash
  docker ps
  ```
- Ver logs do frontend:
  ```bash
  docker service logs NOME_DO_STACK_frontend
  ```
- Remover stack:
  ```bash
  docker stack rm NOME_DO_STACK
  ```

---

Se ainda tiver problemas, envie o erro exato para quem está ajudando ou consulte a [documentação oficial do Docker](https://docs.docker.com/).
