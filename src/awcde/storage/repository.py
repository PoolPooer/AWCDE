"""SQLite-backed repository for persisting pipeline entities."""

from __future__ import annotations

import aiosqlite

from awcde.models.classification import WorkloadClassification
from awcde.models.recommendation import InfrastructureRecommendation
from awcde.models.signature import WorkloadSignature
from awcde.models.telemetry import BenchmarkTelemetry

_CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS benchmark_telemetry (
    id TEXT PRIMARY KEY,
    data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workload_signatures (
    id TEXT PRIMARY KEY,
    data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workload_classifications (
    id TEXT PRIMARY KEY,
    data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS infrastructure_recommendations (
    id TEXT PRIMARY KEY,
    data TEXT NOT NULL
);
"""


class Repository:
    """Async SQLite repository for storing and retrieving pipeline entities.

    Each entity type is stored in its own table with a text primary key (id)
    and a JSON-serialized data column containing the full Pydantic model.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._db: aiosqlite.Connection | None = None

    async def init_db(self) -> None:
        """Initialize the database connection and create tables."""
        self._db = await aiosqlite.connect(self._db_path)
        await self._db.executescript(_CREATE_TABLES_SQL)
        await self._db.commit()

    async def _get_db(self) -> aiosqlite.Connection:
        """Get the database connection, initializing if needed."""
        if self._db is None:
            await self.init_db()
        assert self._db is not None
        return self._db

    async def close(self) -> None:
        """Close the database connection."""
        if self._db is not None:
            await self._db.close()
            self._db = None

    # --- BenchmarkTelemetry ---

    async def save_telemetry(self, telemetry: BenchmarkTelemetry) -> str:
        """Save a BenchmarkTelemetry instance.

        Args:
            telemetry: The telemetry data to persist.

        Returns:
            The id of the saved telemetry.
        """
        db = await self._get_db()
        await db.execute(
            "INSERT OR REPLACE INTO benchmark_telemetry (id, data) VALUES (?, ?)",
            (telemetry.id, telemetry.model_dump_json()),
        )
        await db.commit()
        return telemetry.id

    async def get_telemetry(self, id: str) -> BenchmarkTelemetry | None:
        """Retrieve a BenchmarkTelemetry by id.

        Args:
            id: The telemetry identifier.

        Returns:
            The BenchmarkTelemetry if found, or None.
        """
        db = await self._get_db()
        async with db.execute(
            "SELECT data FROM benchmark_telemetry WHERE id = ?", (id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return BenchmarkTelemetry.model_validate_json(row[0])

    # --- WorkloadSignature ---

    async def save_signature(self, signature: WorkloadSignature) -> str:
        """Save a WorkloadSignature instance.

        Args:
            signature: The signature to persist.

        Returns:
            The id of the saved signature.
        """
        db = await self._get_db()
        await db.execute(
            "INSERT OR REPLACE INTO workload_signatures (id, data) VALUES (?, ?)",
            (signature.id, signature.model_dump_json()),
        )
        await db.commit()
        return signature.id

    async def get_signature(self, id: str) -> WorkloadSignature | None:
        """Retrieve a WorkloadSignature by id.

        Args:
            id: The signature identifier.

        Returns:
            The WorkloadSignature if found, or None.
        """
        db = await self._get_db()
        async with db.execute(
            "SELECT data FROM workload_signatures WHERE id = ?", (id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return WorkloadSignature.model_validate_json(row[0])

    # --- WorkloadClassification ---

    async def save_classification(self, classification: WorkloadClassification) -> str:
        """Save a WorkloadClassification instance.

        Args:
            classification: The classification to persist.

        Returns:
            The id of the saved classification.
        """
        db = await self._get_db()
        await db.execute(
            "INSERT OR REPLACE INTO workload_classifications (id, data) VALUES (?, ?)",
            (classification.id, classification.model_dump_json()),
        )
        await db.commit()
        return classification.id

    async def get_classification(self, id: str) -> WorkloadClassification | None:
        """Retrieve a WorkloadClassification by id.

        Args:
            id: The classification identifier.

        Returns:
            The WorkloadClassification if found, or None.
        """
        db = await self._get_db()
        async with db.execute(
            "SELECT data FROM workload_classifications WHERE id = ?", (id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return WorkloadClassification.model_validate_json(row[0])

    # --- InfrastructureRecommendation ---

    async def save_recommendation(
        self, recommendation: InfrastructureRecommendation
    ) -> str:
        """Save an InfrastructureRecommendation instance.

        Args:
            recommendation: The recommendation to persist.

        Returns:
            The id of the saved recommendation.
        """
        db = await self._get_db()
        await db.execute(
            "INSERT OR REPLACE INTO infrastructure_recommendations (id, data) VALUES (?, ?)",
            (recommendation.id, recommendation.model_dump_json()),
        )
        await db.commit()
        return recommendation.id

    async def get_recommendation(
        self, id: str
    ) -> InfrastructureRecommendation | None:
        """Retrieve an InfrastructureRecommendation by id.

        Args:
            id: The recommendation identifier.

        Returns:
            The InfrastructureRecommendation if found, or None.
        """
        db = await self._get_db()
        async with db.execute(
            "SELECT data FROM infrastructure_recommendations WHERE id = ?", (id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return InfrastructureRecommendation.model_validate_json(row[0])

    # --- Batch operations ---

    async def save_all(
        self,
        telemetry: BenchmarkTelemetry,
        signature: WorkloadSignature,
        classification: WorkloadClassification,
        recommendation: InfrastructureRecommendation,
    ) -> None:
        """Save all pipeline entities in a single transaction.

        Args:
            telemetry: The benchmark telemetry data.
            signature: The derived workload signature.
            classification: The workload classification.
            recommendation: The infrastructure recommendation.
        """
        db = await self._get_db()
        await db.execute(
            "INSERT OR REPLACE INTO benchmark_telemetry (id, data) VALUES (?, ?)",
            (telemetry.id, telemetry.model_dump_json()),
        )
        await db.execute(
            "INSERT OR REPLACE INTO workload_signatures (id, data) VALUES (?, ?)",
            (signature.id, signature.model_dump_json()),
        )
        await db.execute(
            "INSERT OR REPLACE INTO workload_classifications (id, data) VALUES (?, ?)",
            (classification.id, classification.model_dump_json()),
        )
        await db.execute(
            "INSERT OR REPLACE INTO infrastructure_recommendations (id, data) VALUES (?, ?)",
            (recommendation.id, recommendation.model_dump_json()),
        )
        await db.commit()
