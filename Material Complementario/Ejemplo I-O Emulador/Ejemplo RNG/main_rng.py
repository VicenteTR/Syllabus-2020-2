from random import randint, expovariate, seed
from time import time

from emu_lib import Config, AppCB


LAMBDA_EXP = 4  # media = 0.25 segundos
PATH_A_LA_ISA = "../core-emu/ISA.ron"


class Rng:
    def __init__(self, debug=False):
        self.estado = 0
        self.numero_generado = 30  # dummy value
        self.seed = None
        """
            Como la actualización de los dispositivos no es instantánea queremos
            simular tiempos de delay, que conseguimos con un "ancla" de tiempo
            que nos dice la última actualización que hicimos y un buffer que guarda
            los futuros resultados y en cuánto tiempo deben actualizarse.
            
            Hay más soluciones a este problema, yo me quedo con esta.
        """
        self.anchor_time = time()
        self.buffer_escritura = []
        self.debug = debug

    def update_from_buffer(self):
        # se actualiza de uno a la vez!
        # es una limitante bastante fuerte que tiene este diseño
        if self.debug:
            print("===")
            self.print_status()
            print("===")
        if len(self.buffer_escritura) == 0:
            # nada que hacer aquí~
            return 
        # si ya llegué al momento en el que tengo que imprimir la cosa...
        if self.anchor_time + self.buffer_escritura[0][0] <= time():
            update = self.buffer_escritura.pop(0)
            setattr(self, update[1], update[2])  # miren la docu de python
            self.anchor_time = time()

    def agregar_buffer(self, destino, valor):
        # si mi buffer está vacío, es posible que no lo haya usado desde hace
        # mucho, así que actualizo el tiempo ancla
        if len(self.buffer_escritura) == 0:
            self.anchor_time = time()
        # y ahora meto el nuevo valor al buffer
        self.buffer_escritura.append((expovariate(LAMBDA_EXP), destino, valor))
        if self.debug:
            # veamos lo último que agregué!
            print(self.buffer_escritura[-1])

    def puerto_estado(self):
        self.update_from_buffer()
        return self.estado

    def puerto_num_generado(self):
        self.update_from_buffer()
        return self.numero_generado

    def puerto_semilla(self, valor):
        self.update_from_buffer()
        self.agregar_buffer("seed", valor)
        self.agregar_buffer("estado", 2)

    def puerto_comando(self, value):
        self.update_from_buffer()
        if value == 0:
            self.estado = 1
            if self.debug:
                print("SETEANDO SEMILLA:", self.seed)
            seed(self.seed)
            self.agregar_buffer("estado", 2)
        elif value == 1:
            self.estado = 3
            self.agregar_buffer("numero_generado", randint(0, 255))
            self.agregar_buffer("estado", 2)
        elif 2:
            self.estado = 3
            self.agregar_buffer("seed", None)
            self.agregar_buffer("numero_generado", 0)
            self.agregar_buffer("estado", 0)

    def print_status(self):
        # para debug si se quiere...
        print("ESTADO:", self.estado)
        print("NUM:", self.numero_generado)
        print("SEED:", self.seed)
        print("TIME:", self.anchor_time)
        print("BUF:", self.buffer_escritura)
        print("raw_:", self.__dict__)  # por si el setattr hace cosas raras


class AddressDecoder:
    """
        Ejemplo con la interfaz pedida para el address decoder
    """
    def __init__(self):
        """
            Constructor del address decoder, aquí deberías tener referencias
            a los distintos dispositivos I/O con los que te comuniques mediante
            memory mapped.
        """
        pass

    def agregar_io(self, io, info):
        """
            Dado que un mismo I/O se puede comunicar por puertos y mapeo de
            memoria "a la vez", entonces necesitamos una forma de instanciarlos
            fuera del address decoder y pasarlo luego a este, mientras luego le
            pasamos la referencia al AppCB del mismo objeto que representa nuestro
            dispositivo I/O y así el estado queda compartido
            
            ¿no son maravillosos los punteros? ;D
        """
        pass
    
    def read_from(self, direccion) -> int:
        """
            Método que recibe la dirección de memoria que está siendo leída
            y retorna un entero de 8 bits.
            
            A partir de la dirección, determina qué dispositivo y qué parte
            de este debes consultar.
        """
        pass

    def write_into(self, direccion, valor):
        """
            Método que recibe la dirección de memoria que está siendo escrita,
            el valor que queremos escribir y no retorna nada.
            
            A partir de la dirección, determina qué dispositivo y qué parte
            de este debes consultar.
        """
        pass


if __name__ == "__main__":
    # hay que tener buenos modales
    # y no correr código random cuando nos importan
    HIDE_PRINTS = True
    g = Config(limit_of_ticks=20000, auto_mode=True, hide_prints=HIDE_PRINTS)
    rng = Rng()
    c = AppCB()
    c.load_config(g)
    c.load_isa_from_file(PATH_A_LA_ISA)
    c.load_code("rng.asm")
    c.load_io_from_file("rng.ron", rng)
    c.print_program()
    c.run()
    if HIDE_PRINTS:
        # como ocultamos los prints, el estado final de la memoria 
        # no se mostrará al final de la ejecución
        c.print_memory()
    c.print_logs()
