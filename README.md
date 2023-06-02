# GSR

Como correr get (na pasta do cliente):
- Test add key
`python client_get.py  -l 1.2.3,2 3.2.6.0,1 -r SET`

- Test get value of key
`python client_get.py -l 3.2.6.0,2 -r SET ; python client_get.py -l 3.2.1.1.0,2 -r GET`
`python client_get.py -l 3.2.6.0,1 -r SET ; python client_get.py -l 3.2.6.0,1 -r SET ;  python client_get.py -l 2.2.0,2 3.2.2.1.0,2 3.2.2.1.0,2 -r GET`

- Test if set variable works
`python client_get.py -l 1.1.0,1 2.3.0,23 -r SET `
- Test invalid ooid
`python client_get.py -l 1.1.0,1 2.4.0,23 -r SET `

- Test set different value key
`python client_get.py  -l 3.2.6.0,1 3.2.6.1.0,5 -r SET`

- Test set key, first two valid, others wrong
### Coisas que faltam

- Ler da tabela e ver Read onlys, permissões. Também ver se intervalo de valores, e valores, fazem sentido. Criar classe que tem vários valores
- Proibir: "não é permitido que durante V segundos o gestor identifique outro pedido com o mesmo I-ID, sendo aconselhável que o gestor não utilize valores para os I-ID repetidos num intervalo temporal muito maior que V segundos" (última parte com dúvidas...)

- É possível fazer um pedido que não termine em .0? Por exemplo, pedir get's de 3.2.1 , ou 3.2?    Estou a assumir que só se pedem valores terminados com 1, com "endereço completo", exceto chaves

- Servidor responder pedidos ao clientem os dois darem parse
- Falta limparkeys que expiram validade, e alterar a linha da tabela. Também tirar 0 do ooid


- Mudar para bytes, as keys ;)
- MIB da config mal?