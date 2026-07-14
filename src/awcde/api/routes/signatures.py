"""Signature API routes — derivation and retrieval."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from awcde.api.dependencies import get_repository, get_signature_service
from awcde.api.errors import EntityNotFoundError
from awcde.models.signature import WorkloadSignature
from awcde.signatures.service import SignatureService
from awcde.storage.repository import Repository

router = APIRouter(tags=["signatures"])


class DeriveRequest(BaseModel):
    telemetry_id: str


@router.post("/signatures/derive", response_model=WorkloadSignature)
async def derive_signature(
    request: DeriveRequest,
    signature_service: SignatureService = Depends(get_signature_service),
    repository: Repository = Depends(get_repository),
) -> WorkloadSignature:
    telemetry = await repository.get_telemetry(request.telemetry_id)
    if telemetry is None:
        raise EntityNotFoundError("BenchmarkTelemetry", request.telemetry_id)

    signature = signature_service.process(telemetry)
    await repository.save_signature(signature)
    return signature


@router.get("/signatures/{signature_id}", response_model=WorkloadSignature)
async def get_signature(
    signature_id: str,
    repository: Repository = Depends(get_repository),
) -> WorkloadSignature:
    signature = await repository.get_signature(signature_id)
    if signature is None:
        raise EntityNotFoundError("WorkloadSignature", signature_id)
    return signature
