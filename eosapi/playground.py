import requests

base_url = 'http://localhost:8898/v1'
api = 'chain'

info = requests.get(f"{base_url}/{api}/get_info").text
block = requests.post(f"{base_url}/{api}/get_block", data='{"block_num_or_id":5}').text

print(info)
print()
print(block)

schema = {
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
      "previous":"UInt32",
      "timestamp":"Time",
      "transaction_merkle_root":"UInt32",
      "producer": "UInt16",
      "producer_signature":"Signature",
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
      "json": { "type": "Bool", "default": False},
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
    "brief": "Manually serilize json into binary.  The binayargs is usually stored in Message.data.",
    "params": {
      "code": "Name",
      "action": "Name",
      "args": "Vector"
    },
    "results": {
      "binargs": "Bytes",
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
  }

}
