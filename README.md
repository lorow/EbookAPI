# SimpleEbookAPI
A simple API server written with the help of FastAPI as an excuse to learn. 
Designed for reading books in Neos / VRC / anything that can interface with API or OSC. 

After all, what's better than a good book and a handful of chaos around you?

# Development
## setting up the environment: 
- vagrant up
## Running tests:
- pytest 
## Generating migrations and upgrading the database
- alembic revision --autogenerate -m "migration name"
- alembic upgrade head
## Processing the books via command line
- python3 ./NeosEbook/commands/import_epub.py "/location/of/the/book.epub""
