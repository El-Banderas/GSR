# GSR - 25 junho

## Tests
Start executing the `generate_security_info.py` to generate the keys to clients and servers.
Then, execute the server, and the following commands serve to execute the client.

Example request `python manager.py -l  '2.4.0','23' -r SET -id manager0`

To try tests, you must run `python main.py` to execute the agent, and one of the following commands:
- `python gets_sets_tests.py`
- `python keys_test.py`
- `python ddos_tests.py`

Each time you run a test, you must reset the server (rerun the command).

### Testes para fazer

FALTA FAZER A SEGURANÇA PARA TRÁS, SERVIDOR CLIENTE

### Dúvidas 

### Coisas que faltam

- Se calhar mudar a forma como as passes dos clientes estão feitas, para ser mais fácil alterar.