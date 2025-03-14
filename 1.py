import platform
import psutil
import os
import subprocess
from gpuinfo import GPUInfo

def obtener_info_sistema():
    # Obtener el sistema operativo
    sistema_operativo = platform.system()
    version_so = platform.version()

    # Obtener el procesador
    procesador = platform.processor()

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
    print("Sistema Operativo:", sistema_operativo, version_so)
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
