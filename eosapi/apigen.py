import sys
from functools import partial

api_methods = {
    "get_info": {
        "brief": "Return general network information.",
        "params": None,
        "results": {
            "head_block_num": "UInt32",
            "head_block_id": "FixedBytes32",
            "head_block_time": "Time",
            "head_block_producer": {"_id": "UInt16"},
            "recent_slots": "String",
            "participation_rate": "Double"
        }
    },

    "get_block": {
        "brief": "Fetch a block from the blockchain.",
        "params": {
            "block_num_or_id": "String"
        },
        "results": {
            "previous": "UInt32",
            "timestamp": "Time",
            "transaction_merkle_root": "UInt32",
            "producer": "UInt16",
            "producer_signature": "Signature",
            "cycles": "Thread[]"
        },
        "errors": {
            "unknown block": None
        }
    },

    "get_account": {
        "brief": "Fetch a blockchain account",
        "params": {
            "name": "Name"
        },
        "results": {
            "name": "Name",
            "eos_balance": "UInt64",
            "staked_balance": "UInt64",
            "unstaking_balance": "UInt64",
            "last_unstaking_time": "Time",
            "producer": "optional<producer_info>",
            "abi": "optional<Abi>"
        }
    },

    "get_table_rows_i64": {
        "brief": "Fetch smart contract data from an account.",
        "params": {
            "scope": "Name",
            "code": "Name",
            "table": "Name",
            "json": {"type": "Bool", "default": False},
            "lower_bound": {"type": "UInt64", "default": "0"},
            "upper_bound": {"type": "UInt64", "default": "-1"},
            "limit": {"type": "UInt32", "default": "10"}
        },
        "results": {
            "rows": {
                "type": "Vector",
                "doc": "one row per item, either encoded as hex String or JSON object"
            },
            "more": {
                "type": "Bool",
                "doc": "true if last element"
            }
        }
    },

    "abi_json_to_bin": {
        "brief": "Manually serialize json into binary hex.  The binayargs is usually stored in Message.data.",
        "params": {
            "code": "Name",
            "action": "Name",
            "args": "Bytes"
        },
        "results": {
            "binargs": "Bytes",
            "required_scope": "Name[]",
            "required_auth": "Name[]"
        }
    },

    "abi_bin_to_json": {
        "brief": "Convert bin hex back into Abi json definition.",
        "params": {
            "code": "Name",
            "action": "Name",
            "binargs": "Bytes"
        },
        "results": {
            "args": "Bytes",
            "required_scope": "Name[]",
            "required_auth": "Name[]"
        }
    },

    "get_types": {
        "brief": "Fetch account registered types",
        "params": {
            "account_name": "String"
        },
        "results": "String[]"
    },

    "push_block": {
        "brief": "Append a block to the chain database.",
        "params": {
            "block": "Block"
        },
        "results": None
    },

    "push_transaction": {
        "brief": "Attempts to push the transaction into the pending queue.",
        "params": {
            "signed_transaction": "SignedTransaction"
        },
        "results": None
    },

    "get_required_keys": {
        "params": {
            "transaction": "Transaction",
            "available_keys": "Set[PublicKey]"
        },
        "results": "Set[PublicKey]"
    }

}

method_template = """
def {method_name}(self{method_arguments}){return_hints}:
    \"\"\" {docstring} \"\"\"
    
    body = dict({body_args}
    )
    
    return self.exec(
        api='{api}',
        endpoint='{method_name}',
        body=body
    )

"""


def api_codegen():
    """ Generates Python methods from steemd JSON API spec. Prints to stdout. """
    for endpoint_name, endpoint in api_methods.items():
        # method_arg_mapper = partial(map, lambda x: ', %s: %s' % (x[0], x[1]))
        call_arg_mapper = partial(map, lambda x: f', {x}')
        body_arg_mapper = partial(map, lambda x: f'\n\t\t{x}={x},')

        def parse_params(params, fn):
            if params is None:
                return ''

            return ''.join(fn(params.keys()))

        return_hints = ' -> dict'

        # generate method code
        fn = method_template.format(
            method_name=endpoint_name,
            method_arguments=parse_params(endpoint.get('params', {}), call_arg_mapper),
            call_arguments=parse_params(endpoint.get('params', {}), call_arg_mapper),
            body_args=parse_params(endpoint.get('params', {}), body_arg_mapper),
            return_hints=return_hints,
            api='chain',
            docstring=endpoint.get('brief', endpoint_name)
        )
        sys.stdout.write(fn)


# def find_api(method_name):
#     """ Given a method name, find its API. """
#     endpoint = first(where(api_methods, method=method_name))
#     if endpoint:
#         return endpoint.get('api')


# def inspect_api_coverage():
#     """ Compare implemented methods with current live deployment of eosd. """
#     _apis = distinct(pluck('api', api_methods))
#     _methods = set(pluck('method', api_methods))
#
#     avail_methods = []
#     s = Steem(re_raise=False)
#     for api in _apis:
#         err = s.exec('nonexistentmethodcall', api=api)
#         [avail_methods.append(x) for x in err['data']['stack'][0]['data']['api'].keys()]
#
#     avail_methods = set(avail_methods)
#
#     print("\nMissing Methods:")
#     pprint(avail_methods - _methods)
#
#     print("\nLikely Deprecated Methods:")
#     pprint(_methods - avail_methods)


if __name__ == '__main__':
    api_codegen()
    # inspect_api_coverage()
