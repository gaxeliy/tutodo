from typing import Any

from pydantic import ConfigDict
from starlette.responses import Response

from app.config import templates


class ModelConfig:
    model_config = ConfigDict(from_attributes=True)


def get_response_class(template_name: str) -> type[Response]:
    """
    Generates the response class for the given template name.
    Args:
        template_name (str): The name of the template.
    Returns:
        type[Response]: The generated response class.
    """

    class HTMXResponse(Response):
        media_type = 'text/html'

        def render(self, content: Any) -> bytes:
            return templates.TemplateResponse(template_name, {'request': None, 'content': content}).body

    return HTMXResponse
