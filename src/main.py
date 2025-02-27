import logging
import os
from contextlib import asynccontextmanager
import argparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import environment_loader
from src.api.routes import calculator_api
import uvicorn

logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting Zap-HR net salary calculator...")
    yield
    logging.info("Shutting down Zap-HR net salary calculator...")


# Initialize FastAPI app
zap_hr_calculator = FastAPI(title="Zap-HR net salary calculator", version="0.0.1", description="API for Your Project",
                            lifespan=lifespan)

# Configure CORS (adjust origins as needed)
zap_hr_calculator.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
zap_hr_calculator.include_router(calculator_api.router, prefix=calculator_api.prefix, tags=calculator_api.tags)


def main():
    environment_loader.load_environment()
    uvicorn.run(zap_hr_calculator, host=os.getenv("HOST"), port=int(os.getenv("PORT")))


if __name__ == "__main__":
    main()
