import subprocess
import psutil


def ejecutar_comando_batch(comando):
    """Ejecuta un comando batch y devuelve la salida."""
    resultado = subprocess.check_output(comando, shell=True, encoding="utf-8")
    return resultado.strip()


def obtener_info_sistema():
    # Ejecutar el comando batch para obtener información del sistema
    print("==== INFORMACIÓN DEL SISTEMA ====")

    # Obtener Sistema Operativo
    print("Sistema Operativo:")
    print(ejecutar_comando_batch(
        "systeminfo | findstr /B /C:\"Nombre del sistema operativo\""))
    print()

    # Obtener la información del disco duro
    particiones = psutil.disk_partitions()
    disco_duro = []
    for particion in particiones:
        uso = psutil.disk_usage(particion.mountpoint)
        disco_duro.append({
            'disco': particion.device,
            'tamaño': f"{uso.total / (1024 ** 3):.2f} GB",
            'usado': f"{uso.used / (1024 ** 3):.2f} GB",
            'libre': f"{uso.free / (1024 ** 3):.2f} GB"
        })

    print("Disco Duro:")
    for disco in disco_duro:
        print(
            f"  {disco['disco']} - Tamaño: {disco['tamaño']} - Usado: {disco['usado']} - Libre: {disco['libre']}")

    # Obtener Tarjeta Gráfica
    print()

    # Obtener Procesador
    print("Procesador:")
    print(ejecutar_comando_batch(
        "wmic cpu get Name | findstr /R \"i[3579]-\""))
    print()

    # Obtener Tipo de sistema
    print(ejecutar_comando_batch("systeminfo | findstr /B /C:\"Tipo de sistema\""))
    print()

    # Obtener la RAM instalada
    memoria = psutil.virtual_memory()
    ram = f"{memoria.total / (1024 ** 3):.2f} GB"

    print("RAM:", ram)
    print()

    # Obtener la tarjeta gráfica usando 'wmic' (Windows Management Instrumentation)
    tarjeta_grafica = []
    try:
        gpu_info = subprocess.check_output(
            'wmic path win32_videocontroller get caption', shell=True)
        # Eliminar la primera línea (cabecera)
        gpu_info = gpu_info.decode().split('\n')[1:]
        tarjeta_grafica = [gpu.strip() for gpu in gpu_info if gpu.strip()]
    except subprocess.CalledProcessError:
        tarjeta_grafica.append('Desconocida')

    if tarjeta_grafica:
        print("Tarjeta Gráfica(s):", ", ".join(tarjeta_grafica))
    else:
        print("No se detectaron tarjetas gráficas.")

    print("")

    # Añadir un mensaje para que el usuario presione Enter para salir
    input("Pulse Enter para salir...")


if __name__ == "__main__":
    obtener_info_sistema()
