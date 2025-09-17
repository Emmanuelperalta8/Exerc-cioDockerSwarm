## Slide: Demonstração - Docker rodando ao vivo

---

### Terminal: Serviços do Docker Stack

Mostre o terminal com o seguinte comando e explique:

```bash
docker stack services atividade2
```

**Exemplo do que vai aparecer:**

```
ID             NAME                  MODE         REPLICAS   IMAGE                             PORTS
w98kvuexzbc3   atividade2_backend    replicated   5/5        seu-usuario/backend-app:latest
hrqggb4ghzmv   atividade2_frontend   replicated   3/3        seu-usuario/frontend-app:latest   *:8080->8080/tcp
```

**Fale:**
- Aqui temos os dois serviços ativos: backend e frontend.
- Cada um está rodando a quantidade de réplicas configuradas (`5/5` para backend, `3/3` para frontend).
- O frontend está publicado na porta 8080 (veja a coluna PORTS).

---

### Navegador: Aplicação em funcionamento

Abra o navegador e acesse:

```
http://localhost:8080
```

Mostre a aplicação carregando corretamente (pode ser a tela inicial, login, dashboard, qualquer tela que mostre o frontend ativo).

**Fale:**
- A aplicação está acessível localmente graças ao Docker, que faz todo o gerenciamento dos containers e da rede.
- Qualquer pessoa no grupo pode rodar esses mesmos comandos e acessar a aplicação igual, sem depender de configurações específicas de máquina.

---

### Slide: Conclusão da Demonstração

- O Docker permite que todo o ambiente seja replicado facilmente.
- Facilita o deploy, o desenvolvimento em grupo e a escalabilidade da aplicação.
- Testes e deploys ficam mais rápidos, confiáveis e padronizados.

---

## Dica para a apresentação

- Deixe o terminal aberto ao lado do navegador.
- Faça uma alteração no código (se quiser impressionar), redeploy e mostre como o serviço reinicia sem grandes dificuldades.
- Se possível, mostre rapidamente um `docker service logs atividade2_frontend` para exibir logs em tempo real.

---

## Slide (visual sugerida)

| Terminal: Serviços Docker         | Navegador: Aplicação Rodando      |
| --------------------------------- | --------------------------------- |
| ![print_terminal](print_terminal) | ![print_navegador](print_navegador)|

(Substitua pelas suas prints reais!)
