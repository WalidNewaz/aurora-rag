from abc import ABC, abstractmethod

from app.domain.models.artifact import Artifact


class ArtifactHandler(ABC):
    """
    Artifact handler abstract base class.
    Artifact handlers handle ingestion of artifacts.
    Artifacts are essentially files. They are handled based
    on their mime types.
    """

    @abstractmethod
    async def enqueue(self, artifact: Artifact) -> None:
        ...

