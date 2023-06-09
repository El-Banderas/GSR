# GSR - 25 junho

## Tests
Start executing the `generate_security_info.py` to generate the keys to clients and servers.
Then, execute the server, and the following commands serve to execute the client.

Example request `python client_get.py -l  '2.4.0','23' -r SET -id Cli0`

### Testes para fazer

- Test change value of visibility to 5 \

- Test get value of key with new stuff of visibility\

### Dúvidas (abrir enunciado ao perguntar)


# Rápido
Falta corrigir este pedido:
`python client_get.py -l  '2.2.0','3' -r SET -id Cli0`
no table entry tem de ver se é int, e tudo mais, fácil, acho eu...


- Sets de dados tem de ser num dado intervalo? E garantir que são de um certo tipo? Estou a guardar tudo como string para generalizar. Se sim, escolho eu os critérios, e haverá mais uma mensagem de erro?

> Deve verificar o tipo, se é int, por exemplo. Podes definir intervalos de valores, mínimo e máximo. Tipo, máximo number of keys


- É possível fazer um pedido que não termine em .0? Por exemplo, pedir get's de 3.2.1 , ou 3.2?    Estou a assumir que só se pedem valores terminados com 0, com "endereço completo", exceto chaves. 

> Na tabela não tem de acabar em 0. Mas config e system acaba em 0 (como tenho).

- Nós podemos estar a limpar chaves (quando passa muito tempo), alterando o identificador delas (que é a linha atual), e assim o cliente perde a referência para a sua chave. É ignorar esse caso? Ou mudar o identificador da linha (para, por exemplo, o pedido?)

> OOID tem de ser sempre válido, mesmo que se apague chaves

- É suposto os próximos ooids, nos pedidos, ser por linhas ou por colunas. No slide tem a procurar por colunas, quando é mais que um elemento.

> Por colunas

- Mensagens de erro podem ser enviadas como string, ou tem de ir o id do erro? Eu tenho um dicionário comum aos dois com erros e ids.

> Enviar só o número, o cliente volta a converter para string.

- Estrutura do relatório.

> Está no enunciado

- Ver o que a visibilidade das chaves implica.

> 0 - Ninguém pode ver
1 - Quem a criou pode ver
2 - Toda a gente pode ver , pode ser só para o valor da chave, ou para a linha toda.
('3.2.6.0', '1'), cria chave com visibilidade 1.
Se criar com 0, ele pode ver uma primeira vez, e depois não pode ver, manda a mesma mensagem de erro que fosse um outro utilizador a ver.


- As chaves podem ser valores de bytes (0-255 carateres?)

> Sim, depois no cliente converter bytes para string e dar para ver.

- Fase 2, ver se está correto:

Neste momento, envio do cliente para o servidor: 
ID Cliente ; pedido encriptado com chave do servidor ; Checksum encriptado com chave do cliente

> Checksum é calculado a partir do conteúdo da mensagem.


Ao responder ao cliente, vai assim: ID Servidor ; pedido encriptado com chave do cliente; Checksum encriptado com chave do servidor

### Coisas que faltam

- Mudar para bytes, as keys ;)
- Falta testar ir buscar vários valores à tabela dos dados
- Se calhar mudar a forma como as passes dos clientes estão feitas, para ser mais fácil alterar.