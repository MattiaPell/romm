import json
import emoji

from logger.logger import log
from utils import fs, fastapi
from utils.exceptions import PlatformsNotFoundException, RomsNotFoundException
from handler import dbh
from models.platform import Platform
from models.rom import Rom
from handler.socket_manager import SocketManager


async def scan(
    sm: SocketManager, _sid: str, platforms: str, complete_rescan: bool = True
):
    """Scan platforms and roms and write them in database."""

    log.info(emoji.emojize(":magnifying_glass_tilted_right: Scanning "))
    fs.store_default_resources()

    try:  # Scanning platforms
        fs_platforms: list[str] = fs.get_platforms()
    except PlatformsNotFoundException as e:
        log.error(e)
        await sm.emit("scan:done_ko", e.message)
        return

    platforms: list[str] = (
        json.loads(platforms) if len(json.loads(platforms)) > 0 else fs_platforms
    )
    log.info(f"Platforms to be scanned: {', '.join(platforms)}")
    for platform in platforms:
        try:
            scanned_platform: Platform = fastapi.scan_platform(platform)
        except RomsNotFoundException as e:
            log.error(e)
            continue

        await sm.emit(
            "scan:scanning_platform",
            {"p_name": scanned_platform.name, "p_slug": scanned_platform.slug},
            ignore_queue=True,
        )

        dbh.add_platform(scanned_platform)

        # Scanning roms
        fs_roms: list[str] = fs.get_roms(scanned_platform.fs_slug)
        for rom in fs_roms:
            rom_id: int = dbh.rom_exists(scanned_platform.slug, rom["file_name"])
            if rom_id and not complete_rescan:
                continue

            scanned_rom: Rom = fastapi.scan_rom(scanned_platform, rom)
            await sm.emit(
                "scan:scanning_rom",
                {
                    "p_slug": scanned_platform.slug,
                    "file_name": scanned_rom.file_name,
                    "r_name": scanned_rom.r_name,
                },
                ignore_queue=True,
            )

            if rom_id:
                scanned_rom.id = rom_id

            dbh.add_rom(scanned_rom)
        dbh.purge_roms(scanned_platform.slug, [rom["file_name"] for rom in fs_roms])
    dbh.purge_platforms(fs_platforms)
    await sm.emit("scan:done")
