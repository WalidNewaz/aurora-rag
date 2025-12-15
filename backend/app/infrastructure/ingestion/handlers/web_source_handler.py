import psycopg

from app.domain.ingestion.source_handler import SourceHandler
from app.domain.models.source import Source
from app.domain.models.artifact import Artifact
from app.domain.repositories.site_repository import SiteRepository
from app.core.logging import logger

class WebSourceHandler(SourceHandler):
    def __init__(self, site_repo: SiteRepository):
        self.site_repo = site_repo

    async def on_created(
            self,
            source: Source,
            *,
            conn: psycopg.AsyncConnection
    ) -> None:
        config = source.config

        site = await self.site_repo.create(
            source_id=source.id,
            url=config["start_url"],
            name=source.name,
            start_url=config["start_url"],
            allowed_domains=config["allowed_domains"],
            max_depth=config["max_depth"],
            conn=conn
        )
        logger.info("Added site", extra={"site_id": site.id})


    async def on_updated(
            self,
            source: Source,
            *,
            conn: psycopg.AsyncConnection
    ) -> None:
        site = await self.site_repo.get_by_source_id(source.id, conn=conn)
        config = source.config

        if site is not None:
            updated_site = await self.site_repo.update(
                site.id,
                {
                    "name": source.name,
                    "start_url": config["start_url"],
                    "allowed_domains": config["allowed_domains"],
                    "max_depth": config["max_depth"],
                },
                conn=conn,
            )
            logger.info("Updated site", extra={"site_id": site.id, "updated": bool(updated_site)})

        else:
            await self.site_repo.create(
                source_id=source.id,
                url=config["start_url"],
                name=source.name or "",
                start_url=config["start_url"],
                allowed_domains=config["allowed_domains"],
                max_depth=config["max_depth"],
                conn=conn,
            )
            logger.info("Created site for source", extra={"source_id": source.id})

    async def on_deleted(
            self,
            source: Source,
            *,
            conn: psycopg.AsyncConnection
    ) -> None:
        site = await self.site_repo.get(source.id, conn=conn)
        if site:
            await self.site_repo.delete(site.id, conn=conn)
            logger.info("Deleted site", extra={"site_id": site.id})

    async def on_artifact_created(self, artifact: Artifact) -> None:
        logger.info(
            "Web artifact uploaded",
            extra={
                "artifact_id": artifact.id,
                "mime": artifact.mime_type,
                "path": artifact.path,
            },
        )

        # FUTURE:
        # - HTML → Document
        # - PDF → OCR / text extract
        # - ZIP → explode → new artifacts