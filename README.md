# GSR - 25 junho

## Tests
Start executing the `generate_security_info.py` to generate the keys to clients and servers.
Then, execute the server, and the following commands serve to execute the client.

Example request `python client_get.py -l  '2.4.0','23' -r SET -id Cli0`

### Testes para fazer

- Test change value of visibility to 5 \
- Testar cliente que não está registado no servidor
FALTA FAZER A SEGURANÇA PARA TRÁS, SERVIDOR CLIENTE

### Dúvidas 


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