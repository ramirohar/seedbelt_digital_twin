import serial
import time

class Arduino:
    def __init__(self, port="COM3", baudrate=9600, timeout=1):
        self.serial = None
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            print(f"Conectado al puerto {port}")
            time.sleep(2)
        except serial.SerialException as e:
            print(f"Error al conectar al puerto {port}: {e}")
            raise

    def send_command(self, command):
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(f"{command}\r\n".encode())
                self.serial.flush()  
             #   print(f"COMMAND OK")
            except serial.SerialException as e:
                print(f"Error al enviar comando: {e}")
        else:
            print("No hay conexión serial")

    def get_data(self):
        if self.serial and self.serial.is_open:
            try:
                data = self.serial.readline().decode().strip()
                if data:
                    # print(f"OK")
                    return data
                return None
            except serial.SerialException as e:
                print(f"Error al leer datos: {e}")
                return None
            except UnicodeDecodeError:
                print("Error: No se pudo decodificar los datos recibidos")
                return None
        else:
            print("No hay conexión serial")
            return None

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Conexión serial cerrada")