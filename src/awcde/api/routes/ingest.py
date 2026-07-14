"""Ingest API routes — file upload and provider management."""

from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile

from awcde.api.dependencies import get_provider_registry, get_repository
from awcde.api.errors import ProviderError
from awcde.models.telemetry import BenchmarkTelemetry
from awcde.providers.base import ProviderInfo, ProviderSource
from awcde.providers.registry import ProviderRegistry
from awcde.storage.repository import Repository

router = APIRouter(tags=["ingest"])


@router.post("/ingest", response_model=BenchmarkTelemetry)
async def ingest_benchmark(
    file: UploadFile,
    provider_id: str | None = None,
    provider_registry: ProviderRegistry = Depends(get_provider_registry),
    repository: Repository = Depends(get_repository),
) -> BenchmarkTelemetry:
    content = await file.read()
    source = ProviderSource(
        filename=file.filename or "upload",
        content_type=file.content_type or "",
        content=content,
    )

    try:
        if provider_id:
            provider = provider_registry.get(provider_id)
        else:
            provider = provider_registry.resolve(source)
    except (KeyError, ValueError) as e:
        raise ProviderError(
            provider_id=provider_id or "auto",
            message=str(e),
        ) from e

    telemetry = provider.ingest(source)
    await repository.save_telemetry(telemetry)
    return telemetry


@router.get("/providers", response_model=list[ProviderInfo])
async def list_providers(
    provider_registry: ProviderRegistry = Depends(get_provider_registry),
) -> list[ProviderInfo]:
    return provider_registry.list_providers()
