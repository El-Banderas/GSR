# GSR

## Tests
Start executing the `generate_security_info.py` to generate the keys to clients and servers.
Then, execute the server, and the following commands serve to execute the client.

### Gets

- Simple add key (could be used to test max key number) \
`python client_get.py  -l 3.2.6.0,1 -r SET -id Cli0`

- Test add key and change value of visibility to 5 \
`python client_get.py  -l 3.2.6.0,1 3.2.6.1.0,5 -r SET -id Cli0`


- Test get value of key  \
`python client_get.py -l 3.2.6.0,1 -r SET -id Cli0 ; python client_get.py -l 3.2.1.1.0,2 -r GET -id Cli0`
`python client_get.py -l 3.2.6.0,1 -r SET -id Cli0; python client_get.py -l 3.2.6.0,1 -r SET -id Cli0;  python client_get.py -l 2.2.0,2 3.2.2.1.0,2 3.2.2.2.0,2 -r GET -id Cli0`

- Test if set variable works (1º error, second valid) \
`python client_get.py -l 1.1.0,1 2.3.0,23 -r SET  -id Cli0`

- Test invalid ooid (1º read-only value, 2º 2.4.0 ooid doesn't exist) \
`python client_get.py -l 1.1.0,1 2.4.0,23 -r set  -id Cli0`

- Test set key, first two valid, others wrong \
`python client_get.py  -l 3.2.6.0,1 3.2.6.0,1 3.2.2.1.0,5 -r SET -id Cli0`

- User B tries to see user A key \
`python client_get.py  -l 3.2.6.0,1 -r SET -id Cli0 ; python client_get.py  -l 3.2.1.2.0,1 -r GET -id Cli1`

`python client_get.py  -l 3.2.6.0,1 -r SET -id Cli0 ; python client_get.py  -l 3.2.6.1.0,4 -r SET -id Cli1`
### Coisas que faltam

- Proibir: "não é permitido que durante V segundos o gestor identifique outro pedido com o mesmo I-ID, sendo aconselhável que o gestor não utilize valores para os I-ID repetidos num intervalo temporal muito maior que V segundos" (última parte com dúvidas...)
- Adicionar número do pedido, pode ser número random ou a porta

- É possível fazer um pedido que não termine em .0? Por exemplo, pedir get's de 3.2.1 , ou 3.2?    Estou a assumir que só se pedem valores terminados com 0, com "endereço completo", exceto chaves
- Nós podemos estar a limpar chaves, alterando o identificador delas (que é a linha atual), e assim o cliente perde a referência para a sua chave

- Sets de dados tem de ser num dado intervalo? E garantir que são de um certo tipo? Estou a guardar tudo como string para generalizar. 

- É suposto os próximos ooids, nos pedidos, ser por linhas ou por colunas. No slide tem a procurar por colunas, quando é mais que um elemento

- Mudar para bytes, as keys ;)
- Mensagens de erro podem ser como as que tenho?
- Estrutura do relatório?
- Ver discord, o meu servidor