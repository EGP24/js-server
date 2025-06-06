from os import environ

from aiohttp import web
from dotenv import load_dotenv

from src.repositories.postgres.base import db_client
from src.web.urls import routes


def create_app() -> web.Application:
    load_dotenv()
    app = web.Application()

    app.add_routes(routes)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


async def on_startup(_):
    await db_client.connect()


async def on_shutdown(_):
    await db_client.close()


if __name__ == "__main__":
    app = create_app()
    web.run_app(
        app,
        host=environ.get('HOST', default='0.0.0.0'),
        port=int(environ.get('PORT', default=8080)),
    )