from eosapi import HttpClient


class Client(HttpClient):
    def __init__(self, nodes=None, **kwargs):
        nodes = nodes or ['http://localhost:8888']
        super().__init__(nodes=nodes, **kwargs)

    #############################
    # apigen.py generated methods
    #############################

    def get_info(self) -> dict:
        """ Return general network information. """

        body = dict(
        )

        return self.exec(
            api='chain',
            endpoint='get_info',
            body=body
        )

    def get_block(self, block_num_or_id) -> dict:
        """ Fetch a block from the blockchain. """

        body = dict(
            block_num_or_id=block_num_or_id,
        )

        return self.exec(
            api='chain',
            endpoint='get_block',
            body=body
        )

    def get_account(self, name) -> dict:
        """ Fetch a blockchain account """

        body = dict(
            name=name,
        )

        return self.exec(
            api='chain',
            endpoint='get_account',
            body=body
        )

    def get_table_rows_i64(self, scope, code, table, json, lower_bound, upper_bound, limit) -> dict:
        """ Fetch smart contract data from an account. """

        body = dict(
            scope=scope,
            code=code,
            table=table,
            json=json,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            limit=limit,
        )

        return self.exec(
            api='chain',
            endpoint='get_table_rows_i64',
            body=body
        )

    def abi_json_to_bin(self, code, action, args) -> dict:
        """ Manually serialize json into binary hex.  The binayargs is usually stored in Message.data. """

        body = dict(
            code=code,
            action=action,
            args=args,
        )

        return self.exec(
            api='chain',
            endpoint='abi_json_to_bin',
            body=body
        )

    def abi_bin_to_json(self, code, action, binargs) -> dict:
        """ Convert bin hex back into Abi json definition. """

        body = dict(
            code=code,
            action=action,
            binargs=binargs,
        )

        return self.exec(
            api='chain',
            endpoint='abi_bin_to_json',
            body=body
        )

    def get_types(self, account_name) -> dict:
        """ Fetch account registered types """

        body = dict(
            account_name=account_name,
        )

        return self.exec(
            api='chain',
            endpoint='get_types',
            body=body
        )

    def push_block(self, block) -> dict:
        """ Append a block to the chain database. """

        body = dict(
            block=block,
        )

        return self.exec(
            api='chain',
            endpoint='push_block',
            body=body
        )

    def push_transaction(self, signed_transaction) -> dict:
        """ Attempts to push the transaction into the pending queue. """

        body = dict(
            signed_transaction=signed_transaction,
        )

        return self.exec(
            api='chain',
            endpoint='push_transaction',
            body=body
        )

    def get_required_keys(self, transaction, available_keys) -> dict:
        """ get_required_keys """

        body = dict(
            transaction=transaction,
            available_keys=available_keys,
        )

        return self.exec(
            api='chain',
            endpoint='get_required_keys',
            body=body
        )


if __name__ == '__main__':
    client = Client(['http://localhost:8888'])
