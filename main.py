import asyncio
import random
import sys
import time

# Su Windows, forza l'uso di SelectorEventLoop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import json
import logging
import tornado.web
import tornado.websocket
import aiomqtt
from pymongo import AsyncMongoClient

client = AsyncMongoClient('localhost', 27017)
db = client['tennis']
giocatori = db['giocatori']
partite = db['partite']
lista_giocatori = []
lista_partite = []

BROKER = "test.mosquitto.org"
TOPIC = "simulatore/ARIANNA"

clients = set()

async def simulazione(punt1, punt2, id, corso):
    punti = [0, 0]
    game = [0, 0]
    while True:
        vincente = random.randint(0, 1)
        if punti[vincente] == 0:
            punti[vincente] = 15
        elif punti[vincente] == 15:
            punti[vincente] = 30
        elif punti[vincente] == 30:
            punti[vincente] = 40
        else:
            if punti[1 - vincente] == 40:
                if len(punti) == 2:
                    punti.append(vincente)
                else:
                    if punti[2] == vincente:
                        game[vincente] += 1
                        print(punti,game)
                        await partite.update_one({"_id": id}, {"$set": {corso: game}})
                        punti = [0, 0]
                    else:
                        punti.pop(2)
            else:
                game[vincente] += 1
                print(punti, game)
                await partite.update_one({"_id": id}, {"$set": {corso: game}})
                punti = [0, 0]
            if game[vincente] == 6 and game[vincente - 1] < 5:
                corso = "punteggioset"+str(int(corso[-1])+1)
                punti = [0, 0]
                game = [0, 0]
                if vincente == 0:
                    punt1 += 1
                else:
                    punt2 += 1
            if game[vincente] == 7:
                punti = [0, 0]
                game = [0, 0]
                if vincente == 0:
                    punt1 += 1
                else:
                    punt2 += 1
            if punt1 == 2:
                print(punti, game)
                partita = await partite.find_one({"_id": id})
                await partite.update_one({"_id": id}, {"$set": {"vincitore": partita["giocatore1"], "stato": "terminata"}})
                vincitore = await giocatori.find_one({"nome": partita["giocatore1"]})
                if vincitore["qualifica"] == "quarti":
                    await giocatori.update_one({"nome": partita["giocatore1"]}, {"$set": {"qualifica": "semifinale"}})
                    partita = await partite.find_one({"partita": "semifinale2"})
                elif vincitore["qualifica"] == "semifinale":
                    await giocatori.update_one({"nome": partita["giocatore1"]}, {"$set": {"qualifica": "finale"}})
                break
            if punt2 == 2:
                print(punti, game)
                partita = await partite.find_one({"_id": id})
                await partite.update_one({"_id": id}, {"$set": {"vincitore": partita["giocatore2"], "stato": "terminata"}})
                vincitore = await giocatori.find_one({"nome" : partita["giocatore2"]})
                if vincitore["qualifica"] == "quarti":
                    await giocatori.update_one({"nome" : partita["giocatore2"]}, {"$set": {"qualifica" : "semifinale"}})
                    partita = await partite.find_one({"partita": "semifinale2"})
                    if partita["giocatore1"] == "":
                        await partite.update_one({"partita": "semifinale2"}, {"$set": {"giocatore1" : vincitore["nome"]}})
                    else:
                        await partite.update_one({"partita": "semifinale2"},
                                                 {"$set": {"giocatore2": vincitore["nome"]}})
                elif vincitore["qualifica"] == "semifinale":
                    await giocatori.update_one({"nome" : partita["giocatore2"]}, {"$set": {"qualifica" : "finale"}})
                break

        await partite.update_one({"_id": id}, {"$set": {"setincorso": punti}})
        await asyncio.sleep(random.uniform(1.5, 3.5))

async def scorrimemto_tempo(tempo, id):
    partita = await partite.find_one({"_id": id})
    while partita["stato"]=="live":
        await asyncio.sleep(1)
        tempo += 1
        await partite.update_one({"_id": id},{"$set":{"minutaggio":tempo}})

class MainHandler(tornado.web.RequestHandler):
    inizio = False
    async def get(self):
        nthread = 0
        if not self.__class__.inizio:
            for partita in lista_partite:
                punt2 = 0
                punt1 = 0
                if partita["stato"] == "live":
                    if partita["punteggioset1"][0] == 6 or partita["punteggioset1"][0] == 7:
                        punt1 = 1
                        set_incorso = "punteggioset2"
                        if len(partita["punteggioset2"]) != 0:
                            punt2 = 1
                            set_incorso = "punteggioset3"
                    else:

                        set_incorso = "punteggioset1"
                        if partita["punteggioset1"][1] == 6 or partita["punteggioset1"][1] == 7:
                            punt2 = 1
                            set_incorso = "punteggioset2"
                            if len(partita["punteggioset2"]) != 0:
                                punt1 = 1
                                set_incorso = "punteggioset3"

                    # Rimuovi asyncio.to_thread() - usa direttamente asyncio.create_task()
                    asyncio.create_task(simulazione(punt1, punt2, partita["_id"], set_incorso))
                    asyncio.create_task(scorrimemto_tempo(partita["minutaggio"], partita["_id"]))
            self.__class__.inizio = True

        self.render("index.html", partite=lista_partite)

class SelectHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_query_argument("id")
        partita = next((p for p in lista_partite if str(p["_id"]) == id), None)
        self.render("partita.html", partita=partita)

class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket aperto")
        clients.add(self)

    def on_close(self):
        print("WebSocket chiuso")
        clients.remove(self)


async def richiamo_pagina():
    await asyncio.sleep(5)
    while True:  # Aggiungi il loop infinito
        lista_partite.clear()
        estraggo_pars = partite.find()
        async for par in estraggo_pars:
            lista_partite.append(par)
        # inoltro ai client WebSocket
        for c in list(clients):
            try:
                await c.write_message(json.dumps(lista_partite, default=str))  # Serializza in JSON
            except:
                clients.discard(c)

        await asyncio.sleep(1)  # Attendi 2 secondi prima del prossimo aggiornamento


async def main():
    logging.basicConfig(level=logging.INFO)

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/ws", WSHandler),
            (r"/selezionato", SelectHandler),
        ],
        template_path="pagine_web",
        static_path="static",
    )

    estraggo_gri = giocatori.find()
    async for gr in estraggo_gri:
        lista_giocatori.append(gr)
    estraggo_pars = partite.find()
    async for par in estraggo_pars:
        lista_partite.append(par)
    app.listen(8888)
    print("Server Tornado avviato su http://localhost:8888")

    asyncio.create_task(richiamo_pagina())

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())