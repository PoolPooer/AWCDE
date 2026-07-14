from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


class ProviderError(Exception):
    def __init__(self, provider_id: str, message: str, field: str | None = None):
        self.provider_id = provider_id
        self.message = message
        self.field = field
        super().__init__(message)


class EntityNotFoundError(Exception):
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} '{entity_id}' not found")


class PipelineError(Exception):
    def __init__(self, stage: str, message: str):
        self.stage = stage
        self.message = message
        super().__init__(f"Pipeline error in {stage}: {message}")


async def provider_error_handler(request: Request, exc: ProviderError) -> JSONResponse:
    detail = {"provider_id": exc.provider_id, "message": exc.message}
    if exc.field:
        detail["field"] = exc.field
    return JSONResponse(status_code=422, content={"detail": [detail]})


async def entity_not_found_handler(request: Request, exc: EntityNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.entity_type} '{exc.entity_id}' not found"},
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(status_code=422, content={"detail": errors})
