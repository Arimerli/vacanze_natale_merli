import asyncio
import json
import logging
import tornado.web
import tornado.websocket
import aiomqtt

BROKER = "test.mosquitto.org"
TOPIC = "sensor/ARIANNA"

clients = set()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class SelectHandler(tornado.web.RequestHandler):
    def get(self):
        sensore = self.get_query_argument("sensor")
        self.render("selezionato.html", sensor=sensore)

class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket aperto")
        clients.add(self)

    def on_close(self):
        print("WebSocket chiuso")
        clients.remove(self)


async def mqtt_listener():

    logging.info("Connessione al broker MQTT...")

    async with aiomqtt.Client(BROKER) as client:
        await client.subscribe(TOPIC)
        logging.info(f"Iscritto al topic: {TOPIC}")

        async for message in client.messages:
            payload = message.payload.decode()
            data = json.loads(payload)

            ws_message = json.dumps({
                "type": "sensor",
                "data": data
            })

            # inoltro ai client WebSocket
            for c in list(clients):
                await c.write_message(ws_message)


async def main():
    logging.basicConfig(level=logging.INFO)

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/ws", WSHandler),
            (r"/selezionato", SelectHandler),
        ],
        template_path="templates",
    )

    app.listen(8888)
    print("Server Tornado avviato su http://localhost:8888")

    asyncio.create_task(mqtt_listener())

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())