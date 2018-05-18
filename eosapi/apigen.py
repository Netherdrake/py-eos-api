import json
import sys
from functools import partial

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


def api_codegen(api_name, api_spec):
    """ Generates Python methods from steemd JSON API spec. Prints to stdout. """
    for endpoint_name, endpoint in api_spec.items():
        # method_arg_mapper = partial(map, lambda x: ', %s: %s' % (x[0], x[1]))
        call_arg_mapper = partial(map, lambda x: f', {x}')
        body_arg_mapper = partial(map, lambda x: f'\n\t{x}={x},')

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
            api=api_name,
            docstring=endpoint.get('brief', endpoint_name)
        )
        sys.stdout.write(fn)


def load_spec(api_name):
    with open(f"../_spec/{api_name}.json", 'r') as f:
        data = f.read()

    return api_name, json.loads(data)


if __name__ == '__main__':
    # api_codegen(*load_spec('chain'))
    api_codegen(*load_spec('history'))
    # inspect_api_coverage()
