import click
import os
from typing import Dict
import json
from clients.factory import ClientsFactory
from servers.factory import ServersFactory
from writers.factory import WritersFactory
from ping_client import PingClient


# @PROD: of course in real scenario this won't stored locally.
CONFIG_FILE = os.environ.get('CONFIG_FILE', 'config_file.txt')


@click.group()
def cli():
    pass


@click.command()
@click.option('--destination',
              type=str,
              help='the destination server')
@click.option('--port',
              type=int,
              help='the port in the destination server')
def perform_ping(destination: str, port: int):
    current_config = _read_config_from_file(CONFIG_FILE)

    clients_factory = ClientsFactory()
    client = clients_factory.create_client(current_config['client_type'])

    server_factory = ServersFactory()
    server = server_factory.create_server(current_config['client_type'])

    writer_factory = WritersFactory()
    writer = writer_factory.create_writer(current_config['writer_type'])

    # @PROD- I would also generate log class with some flexibility
    # (log levels, output, format and such) and use it to log the different steps.

    executor = PingClient(client=client,
                          writer=writer,
                          server=server)

    executor.execute(destination=destination,
                     server_port=port,
                     local_port=current_config['local_port'],
                     delay_in_secs=current_config['delay_in_secs'],
                     number_of_packets_to_send=current_config['number_of_packets_to_send'],
                     timeout_in_secs=current_config['timeout_in_secs'],
                     packet_size_in_bytes=current_config['packet_size_in_bytes'])


def _read_config_from_file(input_file: str) -> Dict:
    with open(input_file, "r") as input_file:
        # @PROD- I would validate the input here so for example we
        # won't try to ping illegal address, message size too big/negative and such
        return json.load(input_file)


# @PROD- we should add a similar command to invoke the ping server


cli.add_command(perform_ping)


if __name__ == "__main__":
    cli()
