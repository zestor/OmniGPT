from io import StringIO

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from ruamel.yaml import YAML
from starlette.responses import Response


class UnicornAPI(FastAPI):
    def __init__(
        self,
        *,
        contact_name: str = "",
        contact_email: str = "",
        audience: str = "",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.contact = {
            'name': contact_name,
            'email': contact_email,
        }
        self.audience = audience
        self.openapi_yaml_str = ''

    def use_route_names_as_op_ids(self):  # pylint: disable=redefined-outer-name
        """Simplify operation IDs so that generated API clients have simpler function
        names.

        """
        for route in self.routes:
            if isinstance(route, APIRoute):
                route.operation_id = route.name  # in this case, 'read_items'

    def openapi(self) -> dict:
        # Change original method to include extra info fields and to generate YAML
        # from the openapi schema.
        if not self.openapi_schema:
            self.use_route_names_as_op_ids()
            self.openapi_schema = get_openapi(
                title=self.title,
                version=self.version,
                openapi_version=self.openapi_version,
                description=self.description,
                routes=self.routes,
                openapi_prefix=self.openapi_prefix,
            )
            self.openapi_schema['info']['contact'] = self.contact
            self.openapi_schema['info']['x-audience'] = self.audience

            yaml_str = StringIO()
            yaml = YAML()
            yaml.indent(mapping=2, sequence=4, offset=2)
            yaml.dump(self.openapi(), yaml_str)
            self.openapi_yaml_str = yaml_str.getvalue()

        return self.openapi_schema

    def openapi_yaml(self) -> str:
        # This is just a wrapper for the opanapi path operation
        self.openapi()
        return self.openapi_yaml_str

    def setup(self) -> None:
        # Override the openapi path operation to return YAML
        super().setup()
        if self.openapi_url:
            async def openapi() -> Response:
                return Response(self.openapi_yaml(), media_type='text/yaml')

            self.add_route(self.openapi_url, openapi, include_in_schema=False)