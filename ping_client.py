import os
import time
from typing import List
from clients.base import BaseClient
from servers.base import BaseServer
from writers.base import BaseWriter


class PingClient:

    _HOST_TO_LISTEN = '127.0.0.1'

    def __init__(self,
                 client: BaseClient,
                 server: BaseServer,
                 writer: BaseWriter):
        self._client = client
        self._server = server
        self._writer = writer

    def execute(self,
                destination: str,
                server_port: int,
                local_port: int,
                delay_in_secs: int,
                number_of_packets_to_send: int,
                timeout_in_secs: int,
                packet_size_in_bytes: int) -> None:

        # @PROD - we should verify that we were able to connect successfully
        self._client.connect(destination, server_port)

        self._print_initial_results(total_number_of_packets=number_of_packets_to_send,
                                    number_of_bytes=packet_size_in_bytes,
                                    destination=destination,
                                    port=server_port)
        rtts = []

        for i in range(number_of_packets_to_send):
            time.sleep(delay_in_secs)
            bytes_to_send = os.urandom(packet_size_in_bytes)

            # @PROD- we should send in the headers the local port to which we should send the response.

            sent_time = time.time()

            self._client.send(bytes_to_send)

            # and we'll start to wait for the reply message
            # @PROD - assuming we can use the local address as the server host
            self._server.prepare_for_msg(self._HOST_TO_LISTEN, local_port)

            # @PROD- in general it would have been better to wait on a different thread
            # and perform some other things while waiting. However, in this case there isn't
            # anything else we can do so we'll just wait here

            time_to_wait = timeout_in_secs
            while True:
                data = self._server.wait_for_new_data(time_to_wait)
                if data and data != bytes_to_send:
                    # it's possible we get old message/irrelevant one
                    time_to_wait = timeout_in_secs - int(time.time() - sent_time)
                else:
                    break

            if data:
                rtts.append(time.time() - sent_time)

            # we'll print the results (whether we got a ping or not)
            self._print_temp_results(data=data,
                                     index=i+1,
                                     start_time=sent_time)

        # we'll print the final results
        self._print_final_results(durations=rtts,
                                  total_number_of_packets=number_of_packets_to_send)

    def _print_initial_results(self,
                               total_number_of_packets: int,
                               number_of_bytes: int,
                               destination: str,
                               port: int) -> None:
        self._writer.write(f'Sending {total_number_of_packets} (packet_size = {number_of_bytes}) to host: {destination} and port {port}.')

    def _print_temp_results(self, data: bytes, index: int, start_time: float) -> None:
        if not data:
            self._writer.write(f'Request timeout. Request number: {index}')
        else:
            self._writer.write(f'Got reply in {time.time()- start_time} seconds')

    def _print_final_results(self, durations: List[float], total_number_of_packets: int) -> None:
        self._writer.write(f'{total_number_of_packets} were sent. {len(durations)} were received')
        self._writer.write(f'From the received one- Max- {max(durations)} (sec), Min- {min(durations)} (sec), Avg- {sum(durations)/len(durations)} (sec)')
