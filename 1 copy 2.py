import platform
import psutil
import os
import subprocess
import cpuinfo  # Librería para obtener detalles del procesador

def obtener_info_sistema():
    # Obtener el sistema operativo
    sistema_operativo = platform.system()

    # Obtener la versión exacta de Windows (Windows 10, Windows 11)
    if sistema_operativo == "Windows":
        version_so = platform.version()
        release = platform.release()

        # Detectamos si es Windows 10 o 11
        if "10" in release:
            version_so = "Windows 10 " + version_so
        elif "11" in release:
            version_so = "Windows 11 " + version_so
        else:
            version_so = "Versión desconocida de Windows"

    else:
        version_so = "No es un sistema Windows"

    # Obtener el procesador utilizando py-cpuinfo
    info_cpu = cpuinfo.get_cpu_info()
    procesador = info_cpu.get("cpu", "Desconocido")

    # Obtener el tipo de sistema (32 o 64 bits)
    tipo_sistema = platform.architecture()[0]

    # Obtener la RAM instalada
    memoria = psutil.virtual_memory()
    ram = f"{memoria.total / (1024 ** 3):.2f} GB"

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

    # Obtener la tarjeta gráfica usando 'wmic' (Windows Management Instrumentation)
    tarjeta_grafica = []
    try:
        gpu_info = subprocess.check_output('wmic path win32_videocontroller get caption', shell=True)
        gpu_info = gpu_info.decode().split('\n')[1:]  # Eliminar la primera línea (cabecera)
        tarjeta_grafica = [gpu.strip() for gpu in gpu_info if gpu.strip()]
    except subprocess.CalledProcessError:
        tarjeta_grafica.append('Desconocida')

    # Mostrar los resultados
    print("Sistema Operativo:", version_so)
    print("Procesador:", procesador)
    print("Tipo de sistema:", tipo_sistema)
    print("RAM:", ram)
    print("Disco Duro:")
    for disco in disco_duro:
        print(f"  {disco['disco']} - Tamaño: {disco['tamaño']} - Usado: {disco['usado']} - Libre: {disco['libre']}")
    
    if tarjeta_grafica:
        print("Tarjeta Gráfica(s):", ", ".join(tarjeta_grafica))
    else:
        print("No se detectaron tarjetas gráficas.")

if __name__ == "__main__":
    obtener_info_sistema()
