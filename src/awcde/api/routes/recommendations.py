"""Recommendation API routes — generate and retrieve recommendations."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from awcde.api.dependencies import get_recommendation_engine, get_repository
from awcde.api.errors import EntityNotFoundError
from awcde.models.recommendation import InfrastructureRecommendation
from awcde.recommendations.engine import RecommendationEngine
from awcde.storage.repository import Repository

router = APIRouter(tags=["recommendations"])


class RecommendRequest(BaseModel):
    classification_id: str
    signature_id: str


@router.post(
    "/recommendations/generate",
    response_model=InfrastructureRecommendation,
)
async def generate_recommendation(
    request: RecommendRequest,
    engine: RecommendationEngine = Depends(get_recommendation_engine),
    repository: Repository = Depends(get_repository),
) -> InfrastructureRecommendation:
    classification = await repository.get_classification(request.classification_id)
    if classification is None:
        raise EntityNotFoundError("WorkloadClassification", request.classification_id)

    signature = await repository.get_signature(request.signature_id)
    if signature is None:
        raise EntityNotFoundError("WorkloadSignature", request.signature_id)

    recommendation = engine.process(classification, signature)
    await repository.save_recommendation(recommendation)
    return recommendation


@router.get(
    "/recommendations/{recommendation_id}",
    response_model=InfrastructureRecommendation,
)
async def get_recommendation(
    recommendation_id: str,
    repository: Repository = Depends(get_repository),
) -> InfrastructureRecommendation:
    recommendation = await repository.get_recommendation(recommendation_id)
    if recommendation is None:
        raise EntityNotFoundError(
            "InfrastructureRecommendation", recommendation_id
        )
    return recommendation
