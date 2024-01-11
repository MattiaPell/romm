import emoji
from fastapi import APIRouter, Request
from handler import dbh, igdbh
from logger.logger import log
from utils.oauth import protected_route

from endpoints.responses.search import RomSearchResponse

router = APIRouter()


@protected_route(router.put, "/search/roms/igdb", ["roms.read"])
async def search_rom_igdb(
    request: Request, rom_id: str, query: str = None, field: str = "Name"
) -> RomSearchResponse:
    """Search rom into IGDB database

    Args:
        request (Request): Fastapi Request object
        rom_id (str): Rom internal id
        query (str, optional): Query to search the rom (IGDB name or IGDB id). Defaults to None.
        field (str, optional): field with which to search for the rom (name | id). Defaults to "Name".

    Returns:
        RomSearchResponse: List of objects with all the matched roms
    """

    rom = dbh.get_rom(rom_id)
    query = query or rom.file_name_no_tags

    log.info(emoji.emojize(":magnifying_glass_tilted_right: IGDB Searching"))
    matched_roms: list = []

    log.info(f"Searching by {field}: {query}")
    log.info(emoji.emojize(f":video_game: {rom.platform_slug}: {rom.file_name}"))
    if field.lower() == "id":
        matched_roms = igdbh.get_matched_roms_by_id(int(query))
    elif field.lower() == "name":
        matched_roms = igdbh.get_matched_roms_by_name(query, rom.platform.igdb_id)

    log.info("Results:")
    for m_rom in matched_roms:
        log.info(f"\t - {m_rom['name']}")

    return {"roms": matched_roms, "msg": "success"}
