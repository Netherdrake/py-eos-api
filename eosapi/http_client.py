# coding=utf-8
import json
import logging
import socket
import time
from http.client import RemoteDisconnected
from itertools import cycle
from json import JSONDecodeError
from urllib.parse import urlparse

import certifi
import urllib3
from eosapi.exceptions import (
    EosdNoResponse,
    HttpAPIError,
)
from urllib3.connection import HTTPConnection
from urllib3.exceptions import (
    MaxRetryError,
    ReadTimeoutError,
    ProtocolError,
)

logger = logging.getLogger(__name__)


class HttpClient(object):
    """ Http client for handling eosd connections.

    This class serves as an abstraction layer for underlying HTTP requests.

    Args:
      nodes (list): A list of Eos HTTP RPC nodes to connect to.

    .. code-block:: python

       from eosapi.http_client import HttpClient
       rpc = HttpClient(['https://eosnode.com'])

    any call available to that port can be issued using the instance
    via the syntax ``rpc.exec('command', *parameters)``.

    """

    def __init__(self, nodes, **kwargs):
        self.api_version = kwargs.get('api_version', 'v1')
        self.max_retries = kwargs.get('max_retries', 10),

        if kwargs.get('tcp_keepalive', True):
            socket_options = HTTPConnection.default_socket_options + \
                             [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1), ]
        else:
            socket_options = HTTPConnection.default_socket_options

        timeout = urllib3.Timeout(
            connect=kwargs.get('connect_timeout', 15),
            read=kwargs.get('timeout', 30))

        self.http = urllib3.poolmanager.PoolManager(
            num_pools=kwargs.get('num_pools', 50),
            maxsize=kwargs.get('maxsize', 10),
            block=kwargs.get('pool_block', False),
            retries=kwargs.get('http_retries', 10),
            timeout=timeout,
            socket_options=socket_options,
            headers={'Content-Type': 'application/json'},
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
        '''
            urlopen(method, url, body=None, headers=None, retries=None,
            redirect=True, assert_same_host=True, timeout=<object object>,
            pool_timeout=None, release_conn=None, chunked=False, body_pos=None,
            **response_kw)
        '''

        self.nodes = cycle(self._nodes(nodes))
        self.node_url = ''
        self.request = None
        self.next_node()

        log_level = kwargs.get('log_level', logging.INFO)
        logger.setLevel(log_level)

    def next_node(self):
        """ Switch to the next available node.

        This method will change base URL of our requests.
        Use it when the current node goes down to change to a fallback node. """
        self.set_node(next(self.nodes))

    def set_node(self, node_url):
        """ Change current node to provided node URL. """
        self.node_url = node_url

    @property
    def hostname(self):
        return urlparse(self.node_url).hostname

    def exec(self, api, endpoint, body=None, _ret_cnt=0):
        """ Execute a method against eosd RPC.

        Warnings:
            This command will auto-retry in case of node failure, as well as handle
            node fail-over, unless we are broadcasting a transaction.
            In latter case, the exception is **re-raised**.
        """

        url = f"{self.node_url}/{self.api_version}/{api}/{endpoint}"
        body = self._body(body)
        method = 'POST' if body else 'GET'
        try:
            response = self.http.urlopen(method, url, body=body)
        except (MaxRetryError,
                ConnectionResetError,
                ReadTimeoutError,
                RemoteDisconnected,
                ProtocolError) as e:

            if _ret_cnt >= self.max_retries:
                raise e

            # try switching nodes before giving up
            time.sleep(_ret_cnt)
            self.next_node()
            logging.debug('Switched node to %s due to exception: %s' %
                          (self.hostname, e.__class__.__name__))
            return self.exec(api, endpoint, body, _ret_cnt=_ret_cnt + 1)
        except Exception as e:
            extra = dict(err=e, request=self.request)
            logger.info('Request error', extra=extra)
            raise e

        else:
            return self._return(
                response=response,
                body=body)

    def _return(self, response=None, body=None):
        """ Process the response status code and body (json).

        Note:
            If re_raise flag is set, this method will raise an
            exception instead of returning None.

        Exceptions:
            EosdNoResponse on no response.
            HttpAPIError on non-200 response.

        Returns:
            Parsed response body.
        """

        if not response:
            raise EosdNoResponse(
                'eosd nodes have failed to respond, all retries exhausted.')

        result = response.data.decode('utf-8')
        if response.status != 200 or not result:
            extra = dict(result=result, response=response, request_body=body)
            logger.info('non ok response: %s',
                        response.status,
                        extra=extra)
            raise HttpAPIError(response.status, result)

        try:
            response_json = json.loads(result)
        except JSONDecodeError as e:
            extra = dict(response=response, request_body=body, err=e)
            logger.info('failed to parse response', extra=extra)
        else:
            result = response_json

        return result

    def _body(self, body):
        if type(body) not in [str, dict, type(None)]:
            raise ValueError(
                'Request body is of an invalid type %s' % type(body))
        if type(body) == dict:
            return json.dumps(body)
        return body

    def _nodes(self, nodes):
        if type(nodes) == str:
            nodes = nodes.split(',')
        return [x.rstrip('/') for x in nodes]


if __name__ == '__main__':
    h = HttpClient(["http://localhost:8888"])
    print(h.exec('chain', 'get_block', {"block_num_or_id": 5}))
    print(h.exec('chain', 'get_info'))
    # h.exec('get_block', '{"block_num_or_id":5}')
