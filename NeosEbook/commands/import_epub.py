import argparse
import asyncio
import time

from NeosEbook.database import get_db
from NeosEbook.service import NeosEbookService
from NeosEbook.settings import config


async def main(book_path):
    db = get_db(config)
    await db.connect()

    service = NeosEbookService(db)
    await service.add_book_from_path(book_path)

    await db.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Add an epub book")
    parser.add_argument(
        "book_path", type=str, help="a path to a valid epub book, with extension"
    )
    args = parser.parse_args()

    print(f"Processing {args.book_path}")
    start_time = time.time()
    asyncio.run(main(book_path=args.book_path))
    print(f"Done in {time.time() - start_time}")
