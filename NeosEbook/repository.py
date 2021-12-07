from typing import Iterable

import databases
import models


class BookRepository:

	def __init__(self, db: databases.Database):
		self.db = db

	def get_all_books(self) -> Iterable[dict]:
		pass

	def get_book_content_for_page(self, uuid, page) -> dict:
		pass

	def add_book(self, book: models.Book) -> bool:
		pass

	def remove_book(self, uuid) -> bool:
		pass
