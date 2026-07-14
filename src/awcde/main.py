"""AWCDE FastAPI application entry point."""

from fastapi import FastAPI
from pydantic import ValidationError

from awcde.api.errors import (
    EntityNotFoundError,
    ProviderError,
    entity_not_found_handler,
    provider_error_handler,
    validation_error_handler,
)
from awcde.api.routes import classifications, health, ingest, recommendations, signatures

app = FastAPI(
    title="AWCDE — AI Workload Classification & Decision Engine",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(signatures.router, prefix="/api/v1")
app.include_router(classifications.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")

app.add_exception_handler(ProviderError, provider_error_handler)
app.add_exception_handler(EntityNotFoundError, entity_not_found_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
