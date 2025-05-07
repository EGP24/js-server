from aiohttp import web


class ResourceNotFound(web.HTTPNotFound):
    def __init__(self, text: str = 'This resource not found'):
        super().__init__(text=text)
        self.text = text


class UserNotFound(web.HTTPNotFound):
    def __init__(self, text: str = 'User not found'):
        super().__init__(text=text)
        self.text = text


class CardNotFound(web.HTTPNotFound):
    def __init__(self, text: str = 'Card not found'):
        super().__init__(text=text)
        self.text = text


class TokenIsRequired(web.HTTPUnauthorized):
    def __init__(self, text: str = 'Token is required'):
        super().__init__(text=text)
        self.text = text


class CohortIsRequired(web.HTTPBadRequest):
    def __init__(self, text: str = 'Cohort is required'):
        super().__init__(text=text)
        self.text = text


class CardIdIsRequired(web.HTTPBadRequest):
    def __init__(self, text: str = 'Card ID is required'):
        super().__init__(text=text)
        self.text = text
