import tornado, asyncio
from pymongo import AsyncMongoClient

async def aggiungi_elementi(giocatori, partite):
    await giocatori.insert_many(
        [
            {
                "nome": "Carlos Alcaraz",
                "nascita": 2003,
                "nazionalita": "Spagna"
            },
            {
                "nome": "Jannik Sinner",
                "nascita": 2001,
                "nazionalita": "Italia"
            },
            {
                "nome": "Alexander Zverev",
                "nascita": 1997,
                "nazionalita": "Germania"
            },
            {
                "nome": "Novak Djoković",
                "nascita": 1987,
                "nazionalita": "Serbia"
            },
            {
                "nome": "Félix Auger-Aliassime",
                "nascita": 2000,
                "nazionalita": "Canada"
            },
            {
                "nome": "Taylor Fritz",
                "nascita": 1997,
                "nazionalita": "USA"
            },
            {
                "nome": "Alex de Minaur",
                "nascita": 1999,
                "nazionalita": "Australia"
            },
            {
                "nome": "Lorenzo Musetti",
                "nascita": 2002,
                "nazionalita": "Italia"
            },
        ]
    )
    publishers = {}
    casaeds = pub.find()
    async for casaed in casaeds:
        publishers[casaed["name"]] = casaed["_id"]

    await book.insert_many([
  {
    "title": "Il barone rampante",
    "author": "Italo Calvino",
    "genre": "Romanzo",
    "year": 1957,
    "publisher_id": publishers["Einaudi"]
  },
  {
    "title": "Se una notte d'inverno un viaggiatore",
    "author": "Italo Calvino",
    "genre": "Romanzo",
    "year": 1979,
    "publisher_id": publishers["Einaudi"]
  },
  {
    "title": "Il nome della rosa",
    "author": "Umberto Eco",
    "genre": "Giallo",
    "year": 1980,
    "publisher_id": publishers["Einaudi"]
  },
  {
    "title": "Il codice da Vinci",
    "author": "Dan Brown",
    "genre": "Giallo",
    "year": 2003,
    "publisher_id": publishers["Penguin Random House"]
  },
  {
    "title": "Harry Potter e la pietra filosofale",
    "author": "J.K. Rowling",
    "genre": "Fantasy",
    "year": 1997,
    "publisher_id": publishers["Penguin Random House"]
  },
  {
    "title": "Il signore degli anelli",
    "author": "J.R.R. Tolkien",
    "genre": "Fantasy",
    "year": 1954,
    "publisher_id": publishers["Penguin Random House"]
  },
  {
    "title": "1984",
    "author": "George Orwell",
    "genre": "Romanzo",
    "year": 1949,
    "publisher_id": publishers["Mondadori"]
  },
  {
    "title": "Hunger Games",
    "author": "Suzanne Collins",
    "genre": "Fantasy",
    "year": 2008,
    "publisher_id": publishers["Mondadori"]
  },
  {
    "title": "La ragazza del treno",
    "author": "Paula Hawkins",
    "genre": "Giallo",
    "year": 2015,
    "publisher_id": publishers["Mondadori"]
  },
  {
    "title": "Harry Potter e il prigioniero di Azkaban",
    "author": "J.K. Rowling",
    "genre": "Fantasy",
    "year": 1999,
    "publisher_id": publishers["HarperCollins"]
  },
  {
    "title": "Il piccolo principe",
    "author": "Antoine de Saint-Exupéry",
    "genre": "Romanzo",
    "year": 1943,
    "publisher_id": publishers["HarperCollins"]
  },
  {
    "title": "Il vecchio e il mare",
    "author": "Ernest Hemingway",
    "genre": "Romanzo",
    "year": 1952,
    "publisher_id": publishers["HarperCollins"]
  },
  {
    "title": "Sostiene Pereira",
    "author": "Antonio Tabucchi",
    "genre": "Romanzo",
    "year": 1994,
    "publisher_id": publishers["Feltrinelli"]
  },
  {
    "title": "La ragazza del treno",
    "author": "Paula Hawkins",
    "genre": "Giallo",
    "year": 2015,
    "publisher_id": publishers["Feltrinelli"]
  },
  {
    "title": "Cecità",
    "author": "José Saramago",
    "genre": "Romanzo",
    "year": 1995,
    "publisher_id": publishers["Feltrinelli"]
  }
])
async def main():
    client = AsyncMongoClient('localhost', 27017)
    db = client['tennis']
    giocatori = db['giocatori']
    partite = db['partite']
    await aggiungi_elementi(giocatori, partite)

asyncio.run(main())