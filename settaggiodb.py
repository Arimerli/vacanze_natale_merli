import tornado, asyncio, random
from pymongo import AsyncMongoClient


def simulo_set(setg1, setg2):
    win = random.randint(0, 1)
    set = []
    gameperdente = random.randint(0, 5)
    if win == 0:
        setg1 += 1
        if gameperdente == 5:
            set.append(7)
        else:
            set.append(6)
        set.append(gameperdente)
    else:
        setg2 += 1
        set.append(gameperdente)
        if gameperdente == 5:
            set.append(7)
        else:
            set.append(6)

    return setg1, setg2, set

async def aggiungi_elementi(giocatori, partite):
    await giocatori.insert_many(
        [
            {
                "nome": "Carlos Alcaraz",
                "nascita": 2003,
                "nazionalita": "Spagna",
                "qualifica" : "quarti"
            },
            {
                "nome": "Jannik Sinner",
                "nascita": 2001,
                "nazionalita": "Italia",
                "qualifica": "quarti"
            },
            {
                "nome": "Alexander Zverev",
                "nascita": 1997,
                "nazionalita": "Germania",
                "qualifica": "quarti"
            },
            {
                "nome": "Novak Djoković",
                "nascita": 1987,
                "nazionalita": "Serbia",
                "qualifica": "quarti"
            },
            {
                "nome": "Félix Auger-Aliassime",
                "nascita": 2000,
                "nazionalita": "Canada",
                "qualifica": "quarti"
            },
            {
                "nome": "Taylor Fritz",
                "nascita": 1997,
                "nazionalita": "USA",
                "qualifica": "quarti"
            },
            {
                "nome": "Alex de Minaur",
                "nascita": 1999,
                "nazionalita": "Australia",
                "qualifica": "quarti"
            },
            {
                "nome": "Lorenzo Musetti",
                "nascita": 2002,
                "nazionalita": "Italia",
                "qualifica": "quarti"
            },
        ]
    )
    lista_giocatori = []
    estraggo_gri = giocatori.find()
    async for gr in estraggo_gri:
        lista_giocatori.append(gr)
    i = 7
    for _ in range(4):
        n1 = random.randint(0, i)
        g1 = lista_giocatori.pop(n1)
        i -= 1
        n2 = random.randint(0, i)
        g2 = lista_giocatori.pop(n2)
        i -= 1
        setg1 = 0
        setg2 = 0
        sets = [[], [], []]
        vincitore = ""
        if i >= 3:
            minutaggio = random.randint(120, 180)
            for set in range(3):
                setg1,setg2,sets[set]= simulo_set(setg1,setg2)
                if setg2 == 2 or setg1 == 2:
                    break
            if setg2 == 2 :
                vincitore = g2["nome"]
                await giocatori.update_one({'nome': g2["nome"]},
                                           {'$set': {'qualifica': "semifinale"}})
            else:
                vincitore = g1["nome"]
                await giocatori.update_one({'nome': g1["nome"]},
                                           {'$set': {'qualifica': "semifinale"}})
            stato = "terminata"
        else:
            minutaggio = random.randint(60, 120)
            stato = "live"
            for x in range(random.randint(1,2)):
                setg1,setg2,sets[x] = simulo_set(setg1,setg2)
                if setg2 == 2 or setg1 == 2:
                    if setg1 == 2:
                        vincitore = g1["nome"]
                        await giocatori.update_one({'nome': g1["nome"]},
                                                   {'$set': {'qualifica': "semifinale"}})
                    else:
                        vincitore = g2["nome"]
                        await giocatori.update_one({'nome': g2["nome"]},
                                                   {'$set': {'qualifica': "semifinale"}})
                    stato = "terminata"

        await partite.insert_one({
            "giocatore1" : g1["nome"],
            "giocatore2": g2["nome"],
            "minutaggio" : minutaggio,
            "punteggioset1" : sets[0],
            "punteggioset2": sets[1],
            "punteggioset3": sets[2],
            "vincitore" : vincitore,
            "stato" : stato
        })
    semifinali = []
    giocatori = giocatori.find({'qualifica' : 'semifinale'})
    async for giocatore in giocatori:
        semifinali.append(giocatore)
    await partite.insert_one({
        "giocatore1": semifinali[0]["nome"],
        "giocatore2": semifinali[1]["nome"],
        "minutaggio": 0,
        "punteggioset1": [],
        "punteggioset2": [],
        "punteggioset3": [],
        "vincitore": "",
        "stato": "programmata"
    })

async def main():
    client = AsyncMongoClient('localhost', 27017)
    db = client['tennis']
    giocatori = db['giocatori']
    await giocatori.delete_many({})
    partite = db['partite']
    await partite.delete_many({})
    await aggiungi_elementi(giocatori, partite)

asyncio.run(main())