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

app = create_app()
if __name__ == '__main__':
    from uvicorn import run
    run(app, host=environ.get('HOST', '127.0.0.1'), port=int(environ.get('PORT', 8080)))