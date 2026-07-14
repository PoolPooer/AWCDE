"""Classification API routes — classify signatures and retrieve results."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from awcde.api.dependencies import get_classifier, get_repository
from awcde.api.errors import EntityNotFoundError
from awcde.classification.classifier import WorkloadClassifier
from awcde.models.classification import WorkloadClassification
from awcde.storage.repository import Repository

router = APIRouter(tags=["classifications"])


class ClassifyRequest(BaseModel):
    signature_id: str


@router.post("/classifications/classify", response_model=WorkloadClassification)
async def classify_signature(
    request: ClassifyRequest,
    classifier: WorkloadClassifier = Depends(get_classifier),
    repository: Repository = Depends(get_repository),
) -> WorkloadClassification:
    signature = await repository.get_signature(request.signature_id)
    if signature is None:
        raise EntityNotFoundError("WorkloadSignature", request.signature_id)

    classification = classifier.process(signature)
    await repository.save_classification(classification)
    return classification


@router.get(
    "/classifications/{classification_id}",
    response_model=WorkloadClassification,
)
async def get_classification(
    classification_id: str,
    repository: Repository = Depends(get_repository),
) -> WorkloadClassification:
    classification = await repository.get_classification(classification_id)
    if classification is None:
        raise EntityNotFoundError("WorkloadClassification", classification_id)
    return classification
