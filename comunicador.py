from dispositivo import Dispositivo
import time

class Comunicador:
    """
    Clase que abstrae el uso de Dispositivo.
    Puede operar en modo 'meshtastic' o 'mqtt' puro.
    """
    def __init__(self, modo, mensajes=None):
        if modo not in ("meshtastic", "mqtt"):
            raise ValueError("El modo debe ser 'meshtastic' o 'mqtt'.")

        self.modo = modo
        self.mensajes = mensajes if mensajes is not None else []

        # Configuración base
        if modo == "meshtastic":
            self.config = {
                "mqtt_broker": "mqtt.meshtastic.org",
                "mqtt_port": 1883,
                "mqtt_username": "meshdev",
                "mqtt_password": "large4cats",
                #"root_topic": "msh/EU_868/2/e/",
                "root_topic": "msh/EU_868/ES/2/e/",
                "channel": "TestMQTT",
                "key": "ymACgCy9Tdb8jHbLxUxZ/4ADX+BWLOGVihmKHcHTVyo="
            }
        else:  # modo == "mqtt"
            """
            self.config = {
                "mqtt_broker": "test.mosquitto.org",
                "mqtt_port": 1883,
                "mqtt_username": "",
                "mqtt_password": "",
                "root_topic": "test/",
                "channel": "canal_esther",
                "key": ""
            }
            """
            self.config = {
                "mqtt_broker": "broker.emqx.io",
                "mqtt_port": 1883,
                "mqtt_username": "",
                "mqtt_password": "",
                "root_topic": "sensor/data",
                "channel": ["sen55","gas_sensor","esther"],
                "key": ""
            }

        # Crear el dispositivo
        self.dispositivo = Dispositivo(
            mqtt_broker=self.config["mqtt_broker"],
            mqtt_port=self.config["mqtt_port"],
            mqtt_username=self.config["mqtt_username"],
            mqtt_password=self.config["mqtt_password"],
            root_topic=self.config["root_topic"],
            channel=self.config["channel"],
            key=self.config["key"],
            tipo=self.modo,
            #alt=888,
            userdata=self.mensajes
        )

    def enviar(self, texto, canal=None):
        """Enviar positicon GPS y mensaje de texto."""
        self.dispositivo.conectar()
        time.sleep(4)  # Espera para que se conecte
        ##self.dispositivo.enviar_node_info()
        ##time.sleep(4)
        if(self.modo=="meshtastic"):
            self.dispositivo.enviar_posicion() # se envia la posicion GPS solo en caso meshtastic
            time.sleep(4)
            self.dispositivo.enviar_texto(texto)
        else:
            self.dispositivo.enviar_texto(texto,canal)
        

    def recibir(self):
        """Permanece escuchando mensajes hasta que se interrumpe."""
        self.dispositivo.conectar()
        self.dispositivo.empezar_escucha()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.dispositivo.detener_escucha()
            self.dispositivo.desconectar()
            print("Escucha finalizada.")
