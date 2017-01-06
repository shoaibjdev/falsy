import pprint

import falcon
import json
import logging

from falsy.dynamic_import import get_function_from_name

from falcon.routing import compile_uri_template

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class SpecLoader:
    def __init__(self):
        self.specs = {}

    def load_specs(self, swagger_spec):
        log.info("Loading swagger spec into routing table")
        try:
            swagger_spec = json.loads(swagger_spec) if type(swagger_spec) == str else swagger_spec
        except:
            raise Exception("Unable to parse the Swagger spec JSON document.")
        try:
            self.specs['basePath'] = swagger_spec.get('basePath')
            self.specs['beforeId'] = swagger_spec.get('beforeId')
            self.specs['afterId'] = swagger_spec.get('afterId')
            for path, path_content in swagger_spec['paths'].items():
                self.load_paths(path, path_content, swagger_spec)
        except:
            raise Exception("Unable to build routing table from provided Swagger spec.")
        return self.specs

    def load_paths(self, path, path_content, swagger_spec):
        for method, method_content in path_content.items():
            self.load_methods(method, method_content, path, swagger_spec)

    def load_methods(self, method, method_content, path, swagger_spec):
        uri_fields, uri_regex = compile_uri_template(
            '/' + method.lower() + swagger_spec['basePath'] + path)
        self.specs[uri_regex] = {'uri_fields': uri_fields}
        for attribute, attribute_content in method_content.items():
            self.load_attributes(attribute, attribute_content, swagger_spec, uri_regex)

    def load_attributes(self, attribute, attribute_content, swagger_spec, uri_regex):
        self.specs[uri_regex][attribute] = attribute_content
        if attribute == 'parameters':
            for param in attribute_content:
                if param.get('in') == 'body':
                    schema = param.get('schema')
                    ref = schema.get('$ref')
                    if ref:
                        self.specs[uri_regex]['schema'] = swagger_spec['definitions'][
                            ref[ref.rfind('/') + 1:]]
                    else:
                        self.specs[uri_regex]['schema'] = schema