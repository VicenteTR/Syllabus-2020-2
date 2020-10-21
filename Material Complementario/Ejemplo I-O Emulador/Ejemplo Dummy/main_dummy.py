from emu_lib import Config, AppCB


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
        # NO LO VOY A USAR A PROPÓSITO, PARA QUE TENGAN LA OPORTUNIDAD
        # DE RESOLVERLO USTEDES.
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
        print(f"LEYENDO {direccion}")
        print("\tAquí deberían llamar al dispositivo")
        return 42

    def write_into(self, direccion, valor):
        """
            Método que recibe la dirección de memoria que está siendo escrita,
            el valor que queremos escribir y no retorna nada.
            
            A partir de la dirección, determina qué dispositivo y qué parte
            de este debes consultar.
        """
        print(f"ESCRIBIENDO {valor} en {direccion}")
        print("\tAquí deberían llamar al dispositivo")


class Dummy:
    def __init__(self):
        pass
    
    def foo(self):
        print(f"Leyendo puerto")
        return 43
    
    def bar(self, value):
        print(f"Recibiendo {value} en el puerto")


if __name__ == "__main__":
    c = AppCB()
    g = Config(auto_mode=False)
    d = Dummy()  # dispositivo del ejemplo
    a = AddressDecoder()
    # aquí le deberían pasar TODOS los dispositivos que funcionan con memory mapped
    # al address decoder

    c.load_config(g)
    c.load_isa_from_file("../core-emu/ISA.ron")  # depende de donde tengas guardada la ISA en tu computador
    c.load_io_from_file("dummy_io.ron", d)  # para la comunicación por puertos
    c.load_address_decoder(a)
    c.load_code("ejemplo_dummy.asm")
    c.print_program()
    c.run()
    c.print_logs()
