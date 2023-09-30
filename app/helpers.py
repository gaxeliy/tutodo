import json
from typing import Any

from pydantic import ConfigDict
from starlette.responses import Response

from app.config import templates


class ModelConfig:
    model_config = ConfigDict(from_attributes=True)


class HasHeader:
    headers: dict[str, str]


def get_response_class(template_name: str) -> type[Response]:
    """
    Создает объект response_class в зависимости от заголовков
    """
    class HTMXOrJSONResponse(Response):
        media_type = 'application/json'

        def render(self, content: Any) -> bytes:
            headers = content.get('headers', {})
            if 'headers' in content:
                del content['headers']
            if 'hx-request' in headers:
                self.media_type = 'text/html'
                return templates.TemplateResponse(template_name, {'request': None, 'content': content}).body
            else:
                self.media_type = 'application/json'
                return json.dumps(
                    content,
                    ensure_ascii=False,
                    allow_nan=False,
                    indent=None,
                    separators=(",", ":"),
                ).encode("utf-8")

    return HTMXOrJSONResponse
