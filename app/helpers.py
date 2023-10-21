import json
from functools import wraps
from typing import Any, TypeVar, Generic, Mapping

from pydantic import ConfigDict, BaseModel
from starlette.requests import Request
from starlette.responses import Response

from app.config import templates


T = TypeVar('T')


class ResponseWithHeaders(BaseModel, Generic[T]):
    data: T
    headers: Mapping[str, str]


class ModelConfig:
    model_config = ConfigDict(from_attributes=True)


def pass_headers(func):
    """
    Добавляет заголовки в Response для использования в renderer-ах
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        data = await func(*args, **kwargs)
        headers = kwargs['request'].headers
        return ResponseWithHeaders(data=data, headers=headers)

    return wrapper


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
                htmx_body = templates.TemplateResponse(template_name, {'request': None, 'content': content}).body
                return htmx_body
            elif 'application/json' in headers.get('accept'):
                self.media_type = 'application/json'
                json_body = json.dumps(
                    content,
                    ensure_ascii=False,
                    allow_nan=False,
                    indent=None,
                    separators=(",", ":"),
                ).encode("utf-8")
                return json_body
            else:
                self.media_type = 'text/html'
                html_body = templates.TemplateResponse(template_name,
                                                       {'request': None, 'content': content, 'full_page': True}).body
                return html_body
            pass

    return HTMXOrJSONResponse
