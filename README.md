# NeosEbookAPI
A simple API server written in fastapi for reading books inside of Neos. After all, what's better than a good book and a handful of chaos around you?


# Developent
## setting up the environment: 
- vagrant up
## Running tests:
- pytest 
## Generating migrations and upgrading the database
- alembic revision --autogenerate -m "migration name"
- alembic upgrade head
## Processing the books via command line
- python3 ./NeosEbook/commands/import_epub.py "/location/of/the/book.epub""
