import socket
import pymysql

def scan_mysql_service(ip, port):
    try:
        # Intentar conectar al puerto especificado
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Tiempo de espera de 1 segundo
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            print(f"Puerto {port} en {ip} está abierto.")
            return True
        else:
            print(f"Puerto {port} en {ip} está cerrado.")
            return False
    except socket.error as e:
        print(f"Error al conectar al puerto {port} en {ip}: {e}")
        return False
    finally:
        sock.close()

def connect_to_mysql(ip, port, user, password, database):
    try:
        connection = pymysql.connect(
            host=ip,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("Conexión exitosa a MySQL")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def main():
    ip = input("Ingresa la dirección IP a escanear: ")
    port = int(input("Ingresa el puerto a escanear: "))
    user = input("Ingresa el usuario de MySQL: ")
    password = input("Ingresa la contraseña de MySQL: ")
    database = input("Ingresa el nombre de la base de datos a la que conectar: ")

    if scan_mysql_service(ip, port):
        connection = connect_to_mysql(ip, port, user, password, database)
        if connection:
            try:
                # Realiza operaciones en la base de datos
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE()")
                result = cursor.fetchone()
                print(f"Conectado a la base de datos: {result[0]}")
            except pymysql.MySQLError as e:
                print(f"Error ejecutando la consulta: {e}")
            finally:
                connection.close()
        else:
            print("No se pudo conectar a la base de datos MySQL.")
    else:
        print(f"No se detectó un servicio MySQL abierto en {ip}:{port}")

if __name__ == "__main__":
    main()
