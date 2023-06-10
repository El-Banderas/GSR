# GSR - 25 junho

## Tests
Start executing the `generate_security_info.py` to generate the keys to clients and servers.
Then, execute the server, and the following commands serve to execute the client.

Example request `python client_get.py -l  '2.4.0','23' -r SET -id Cli0`

### Testes para fazer

- Test change value of visibility to 5 \

- Test get value of key with new stuff of visibility\

### Dúvidas (abrir enunciado ao perguntar)


- É possível fazer um pedido que não termine em .0? Por exemplo, pedir get's de 3.2.1 , ou 3.2?    Estou a assumir que só se pedem valores terminados com 0, com "endereço completo", exceto chaves. 

> Na tabela não tem de acabar em 0. Mas config e system acaba em 0 (como tenho).

- Nós podemos estar a limpar chaves (quando passa muito tempo), alterando o identificador delas (que é a linha atual), e assim o cliente perde a referência para a sua chave. É ignorar esse caso? Ou mudar o identificador da linha (para, por exemplo, o pedido?)

> OOID tem de ser sempre válido, mesmo que se apague chaves

- É suposto os próximos ooids, nos pedidos, ser por linhas ou por colunas. No slide tem a procurar por colunas, quando é mais que um elemento.

> Por colunas

- Estrutura do relatório.

> Está no enunciado

- As chaves podem ser valores de bytes (0-255 carateres?)

> Sim, depois no cliente converter bytes para string e dar para ver.

- Fase 2, ver se está correto:

Neste momento, envio do cliente para o servidor: 
ID Cliente ; pedido encriptado com chave do servidor ; Checksum encriptado com chave do cliente

> Checksum é calculado a partir do conteúdo da mensagem.


Ao responder ao cliente, vai assim: ID Servidor ; pedido encriptado com chave do cliente; Checksum encriptado com chave do servidor

- Sets de dados tem de ser num dado intervalo? 

> Deve verificar o tipo, se é int, por exemplo. Podes definir intervalos de valores, mínimo e máximo. Tipo, máximo number of keys

### Coisas que faltam

- Mudar para bytes, as keys ;)
- Falta testar ir buscar vários valores à tabela dos dados
- Se calhar mudar a forma como as passes dos clientes estão feitas, para ser mais fácil alterar.
- Mudar nomes de ficheiros? Tipo common no cliente