from fastapi import FastAPI

from controllers import scraping_controller


def create_app():
    app = FastAPI()
    app.include_router(scraping_controller.router)

    return app
