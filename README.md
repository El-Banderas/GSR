# GSR - 25 junho

## Tests
Start executing the `generate_security_info.py`, in the folder of security, to generate the keys to clients and servers.
Then, execute the server, `python main.py` in the agent folder,and the following commands serve to execute the client.

Example request `python manager.py -l  '2.4.0','23' -r SET -id manager0`

To try tests, you must run `python main.py` to execute the agent, and one of the following commands:
- `python gets_sets_tests.py`
- `python keys_test.py`
- `python ddos_tests.py`

Each time you run a test, you must reset the server (rerun the command).
