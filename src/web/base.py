from typing import get_type_hints

from aiohttp import web
from serpyco_rs import SchemaValidationError

from src.exceptions import CardIdIsRequired, CohortIsRequired, TokenIsRequired
from src.mappers.base import EntityMapper


def with_typehinted_request(func):
    type_hints = get_type_hints(func)

    async def wrapper(request: web.Request, **kwargs):
        parsed_request = None
        if (request_type := type_hints.get('request')) and request_type is not type(None):
            request_mapper = EntityMapper(request_type)
            try:
                parsed_request = request_mapper.map_from(await request.json())
            except SchemaValidationError as e:
                raise web.HTTPBadRequest(text=f"Invalid request data: {e}") from e

        for name, hint in type_hints.items():
            if name == 'request':
                continue
            if hint is XAuthorizationRequired:
                if not (token := request.headers.get('Authorization')):
                    raise TokenIsRequired
                kwargs[name] = token
            if hint is XCohortRequired:
                if not (cohort := request.match_info.get('cohort_id')):
                    raise CohortIsRequired
                kwargs[name] = cohort
            if hint is XCardIdRequired:
                if not (card_id := request.match_info.get('card_id')) or not card_id.isdigit():
                    raise CardIdIsRequired
                kwargs[name] = int(card_id)

        kwargs['app'] = request.app
        kwargs |= {'request': parsed_request} if parsed_request else {}
        result = await func(**kwargs)
        if (return_type := type_hints.get('return')) and return_type is not type(None):
            print(return_type, type(None), return_type is not type(None))
            response_mapper = EntityMapper(return_type)
            response_data = {}
            if result:
                try:
                    response_data = response_mapper.map_to(result)
                except SchemaValidationError as e:
                    raise web.HTTPInternalServerError(text=f"Invalid response data: {e}") from e
            return web.json_response(data=response_data)
        return web.Response()

    return wrapper


class XAuthorizationRequired(str): ...


class XCohortRequired(str): ...


class XCardIdRequired(int): ...