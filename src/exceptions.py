from aiohttp import web

ResourceNotFound = web.HTTPNotFound(text='This resource not found')
UserNotFound = web.HTTPNotFound(text='User not found')
CardNotFound = web.HTTPNotFound(text='Card not found')
TokenIsRequired = web.HTTPUnauthorized(text='Token is required')
CohortIsRequired = web.HTTPBadRequest(text='Cohort is required')
CardIdIsRequired = web.HTTPBadRequest(text='Card ID is required')