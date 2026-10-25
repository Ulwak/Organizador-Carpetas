import shutil
from pathlib import Path

def listar_archivos_de_la_carpeta_del_usuario(ruta, ruta_script, mover_ocultos):
    # Verifica si el usuario queria mover los archivos ocultos o unicamente los normales.
    if mover_ocultos:
        # guarda en una sola lista todos los archivos de la carpeta actual evitandose a si mismo
        archivo = [n for n in ruta.iterdir() if n.is_file() and n.name != ruta_script.name]
    else:
        archivo = [n for n in ruta.iterdir() if n.is_file() and not n.name.startswith('.') and n.name != ruta_script.name]
    return archivo

def evitar_reemplazar_repetidos(ruta_archivo):
    #aumenta vuelta haciendo que cada archivo salga con un numero mas evitando repetidos y reemplazar archivos por error
    vuelta = 1
    ruta_nueva = ruta_archivo
    while ruta_nueva.exists():
        ruta_nueva = ruta_archivo.with_name(f"{ruta_archivo.stem}({vuelta}){ruta_archivo.suffix}")
        vuelta += 1
    return ruta_nueva

def main():
    while True:
        respuesta = input("Desea mover los archivos ocultos para organizarlos tambien? (Si/No, S/N, Yes/No, Y/N): ").lower()
        if respuesta in ["si", "s", "yes", "y"]:
            mover_ocultos = True
            break
        elif respuesta in ["no", "n"]:
            mover_ocultos = False
            break
        else:
            print("Ingrese una respuesta valida. (Si/No, S/N, Yes/No, Y/N)")
    ruta_script = Path(__file__).resolve()
    ruta = ruta_script.parent
    archivos = listar_archivos_de_la_carpeta_del_usuario(ruta, ruta_script, mover_ocultos)
    #verifica que haya algun archivo para organizar
    if archivos:
    #recorre cada archivo en la carpeta.
        for archivo in archivos:    
            nombre = archivo.name
            extension = archivo.suffix.upper().replace(".", "")
            if not extension:
                extension = "SIN EXTENSION O OCULTOS"
            print(f"Moviendo Archivo: {nombre}")
            ruta_carpeta = ruta / extension
            ruta_carpeta.mkdir(parents=True, exist_ok=True)
            ruta_nueva = evitar_reemplazar_repetidos(ruta_carpeta / nombre)
            try:
                #mueve el archivo entre carpetas
                shutil.move(archivo, ruta_nueva)
                print(f"Archivo {nombre} movido a la carpeta {extension}")
            except Exception as error_movimiento:
                #captura el error aunque es bastante generico (Se podria poner como que el archivo esta en uso o para permisos)
                print(f"Ocurrio un error al mover el archivo: {error_movimiento}")
    else:
        print("No hay archivos para organizar en esta carpeta")
if __name__ == "__main__":
    main()