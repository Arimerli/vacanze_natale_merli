import tornado, asyncio
import random
from pymongo import AsyncMongoClient
async def main():
    client = AsyncMongoClient('localhost', 27017)
    db = client['tennis']
    giocatori = db['giocatori']
    partite = db['partite']
    lista_giocatori = []
    estraggo_gri = giocatori.find()
    async for gr in estraggo_gri:
        lista_giocatori.append(gr)
    i = 7
    for _ in range(4):
        n1 = random.randint(0, i)
        g1 = lista_giocatori.pop(n1)
        i-=1
        n2 = random.randint(0, i)
        g2 = lista_giocatori.pop(n2)
        i -= 1
        inserimento = await partite.insert_one({
            "giocatore1" : g1["nome"],
            "giocatore2" : g2["nome"],
            "punteggio" : "0:0",
            "minutaggio" : 0
        })

asyncio.run(main())



#<p>{{ partite[0]['giocatore1'] }} VS {{ partite[0]['giocatore2'] }}                 {{ partite[0]['setg1'] }}:{{ partite[0]['setg2'] }}</p>