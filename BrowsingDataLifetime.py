import winreg
import json
import os
import re
from colorama import init, Fore, Style, Back

# Inicializar Colorama
init(autoreset=True)

# Definición de tipos de datos
TIPOS_DATOS = {
    1: ("browsing_history", "Historial de navegación"),
    2: ("download_history", "Historial de descargas"),
    3: ("cookies_and_other_site_data", "Cookies y otros datos de sitios"),
    4: ("cached_images_and_files", "Imágenes y archivos almacenados en caché"),
    5: ("password_signin", "Acceso mediante contraseña"),
    6: ("autofill", "Autocompletar"),
    7: ("site_settings", "Configuración de sitios"),
    8: ("hosted_app_data", "Datos de apps alojadas")
}

OPCIONES_TIEMPO = {
    1: ("1 día", 24),
    2: ("2 días", 48),
    3: ("3 días", 72),
    4: ("7 días", 168),
    5: ("1 mes (30 días)", 720),
    6: ("Personalizado", None)
}

RUTA_BASE = r"SOFTWARE\Policies\Google\Chrome"

def crear_claves_registro():
    """Crea las claves necesarias en el registro si no existen"""
    try:
        hive = winreg.HKEY_LOCAL_MACHINE
        partes = RUTA_BASE.split('\\')
        ruta_actual = ""
        
        for parte in partes:
            ruta_actual = ruta_actual + "\\" + parte if ruta_actual else parte
            try:
                winreg.OpenKey(hive, ruta_actual, 0, winreg.KEY_READ)
            except:
                winreg.CreateKey(hive, ruta_actual)
                print(f"{Fore.GREEN}Creada clave: {ruta_actual}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}Error creando claves: {e}")
        return False

def establecer_valor_registro(nombre, valor):
    """Establece un valor en el registro"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RUTA_BASE, 
                           0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, nombre, 0, winreg.REG_SZ, valor)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error estableciendo valor: {e}")
        return False

def eliminar_valor_registro(nombre):
    """Elimina un valor del registro"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RUTA_BASE, 
                           0, winreg.KEY_WRITE) as key:
            winreg.DeleteValue(key, nombre)
        return True
    except:
        # El valor ya no existe o no se pudo eliminar
        return False

def mostrar_menu_principal():
    """Muestra el menú principal"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
    print(" " * 15 + "CONFIGURADOR DE CHROME POLICIES")
    print("="*50)
    print(f"{Style.BRIGHT}{Fore.YELLOW}1.{Style.RESET_ALL} Configurar BrowsingDataLifetime")
    print(f"{Style.BRIGHT}{Fore.YELLOW}2.{Style.RESET_ALL} Configurar ClearBrowsingDataOnExitList")
    print(f"{Style.BRIGHT}{Fore.YELLOW}3.{Style.RESET_ALL} Eliminar configuración existente")
    print(f"{Style.BRIGHT}{Fore.YELLOW}0.{Style.RESET_ALL} Salir")
    print("="*50)
    
    opcion = input("\nSeleccione una opción: ")
    return opcion

def mostrar_seleccion_tipos(titulo, seleccion_inicial=None):
    """Muestra la interfaz para seleccionar tipos de datos"""
    seleccion = set(seleccion_inicial) if seleccion_inicial else set()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
        print(f" {titulo}")
        print("="*50)
        print("Seleccione los tipos de datos (ingrese números separados por comas)")
        print("Presione Enter sin ingresar nada para continuar")
        print("Ingrese un número nuevamente para deseleccionarlo")
        print("="*50 + "\n")
        
        # Mostrar todos los tipos con estado
        for num, (tipo, desc) in TIPOS_DATOS.items():
            estado = f"{Fore.GREEN}✓" if tipo in seleccion else f"{Fore.RED}✗"
            print(f"{Fore.YELLOW}{num}. {estado} {Fore.WHITE}{desc}{Style.RESET_ALL}")
        
        print("\n" + "="*50)
        entrada = input("\nIngrese los números (ej: 1,3,5) o 0 para continuar: ").strip()
        
        if entrada == "0" or entrada == "":
            break
            
        # Procesar entrada
        try:
            numeros = [int(n.strip()) for n in entrada.split(',') if n.strip().isdigit()]
            for num in numeros:
                tipo = TIPOS_DATOS.get(num, [None])[0]
                if tipo:
                    if tipo in seleccion:
                        seleccion.remove(tipo)
                    else:
                        seleccion.add(tipo)
        except:
            pass
            
    return [tipo for tipo in seleccion]

def seleccionar_tiempo(titulo):
    """Permite seleccionar el tiempo de vida"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
        print(f" {titulo}")
        print("="*50)
        print("Seleccione el tiempo de vida:")
        
        for num, (desc, horas) in OPCIONES_TIEMPO.items():
            print(f"{Fore.YELLOW}{num}. {Fore.WHITE}{desc}")
        
        print("="*50)
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion.isdigit():
            opcion = int(opcion)
            if opcion in OPCIONES_TIEMPO:
                if opcion == 6:  # Personalizado
                    while True:
                        custom = input("Ingrese horas (1-2147483647): ")
                        if custom.isdigit() and 1 <= int(custom) <= 2147483647:
                            return int(custom)
                        print(f"{Fore.RED}Valor inválido. Intente nuevamente.")
                else:
                    return OPCIONES_TIEMPO[opcion][1]
        
        print(f"{Fore.RED}Opción inválida. Intente nuevamente.")

def configurar_politica(nombre_politica, es_browsing=True):
    """Flujo de configuración para una política"""
    # Menú de configuración/eliminación
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
    print(f" CONFIGURAR {nombre_politica.upper()}")
    print("="*50)
    print(f"{Style.BRIGHT}{Fore.YELLOW}1.{Style.RESET_ALL} Configurar nueva política")
    print(f"{Style.BRIGHT}{Fore.YELLOW}2.{Style.RESET_ALL} Eliminar política existente")
    print(f"{Style.BRIGHT}{Fore.YELLOW}0.{Style.RESET_ALL} Volver al menú principal")
    print("="*50)
    
    opcion = input("\nSeleccione una opción: ")
    
    if opcion == "0":
        return
    elif opcion == "2":
        if eliminar_valor_registro(nombre_politica):
            print(f"\n{Fore.GREEN}Política {nombre_politica} eliminada con éxito!")
        else:
            print(f"\n{Fore.YELLOW}La política {nombre_politica} no existía o no pudo ser eliminada.")
        input("\nPresione Enter para continuar...")
        return
    
    # Configuración inicial para BrowsingDataLifetime
    seleccion_inicial = ["cookies_and_other_site_data", "cached_images_and_files"] if es_browsing else []
    
    # Selección de tipos de datos
    tipos_seleccionados = mostrar_seleccion_tipos(f"SELECCIÓN PARA {nombre_politica.upper()}", seleccion_inicial)
    
    if not tipos_seleccionados:
        print(f"{Fore.YELLOW}No se seleccionaron tipos. Operación cancelada.")
        input("\nPresione Enter para continuar...")
        return
    
    # Para ClearBrowsingDataOnExitList no se necesita tiempo
    if not es_browsing:
        # Crear estructura simple (lista de strings)
        valor_json = json.dumps(tipos_seleccionados)
        if establecer_valor_registro(nombre_politica, valor_json):
            print(f"\n{Fore.GREEN}Configuración aplicada con éxito!")
        else:
            print(f"\n{Fore.RED}Error aplicando configuración.")
        input("\nPresione Enter para continuar...")
        return
    
    # Para BrowsingDataLifetime necesitamos tiempo
    tiempo_general = seleccionar_tiempo("TIEMPO GENERAL PARA TODOS LOS TIPOS")
    
    # Preguntar si quiere configuraciones personalizadas
    configuraciones = []
    tipos_personalizados = []
    
    print(f"\n{Fore.CYAN}¿Desea configurar tiempos personalizados para tipos específicos? (s/n)")
    if input().lower() == 's':
        for tipo in tipos_seleccionados:
            # Encontrar la descripción del tipo
            desc = next((d for n, (t, d) in TIPOS_DATOS.items() if t == tipo), tipo)
            
            print(f"\n{Fore.YELLOW}Configurar tiempo personalizado para: {Fore.WHITE}{desc}")
            print(f"{Fore.CYAN}¿Desea un tiempo diferente al general? (s/n)")
            if input().lower() == 's':
                tiempo = seleccionar_tiempo(f"TIEMPO PARA {desc.upper()}")
                configuraciones.append({
                    "data_types": [tipo],
                    "time_to_live_in_hours": tiempo
                })
                tipos_personalizados.append(tipo)
    
    # Agregar los tipos no personalizados con el tiempo general
    tipos_restantes = [t for t in tipos_seleccionados if t not in tipos_personalizados]
    if tipos_restantes:
        configuraciones.insert(0, {
            "data_types": tipos_restantes,
            "time_to_live_in_hours": tiempo_general
        })
    
    # Crear el valor JSON final
    valor_json = json.dumps(configuraciones)
    
    # Aplicar al registro
    if crear_claves_registro() and establecer_valor_registro(nombre_politica, valor_json):
        print(f"\n{Fore.GREEN}Configuración aplicada con éxito!")
    else:
        print(f"\n{Fore.RED}Error aplicando configuración.")
    
    input("\nPresione Enter para continuar...")

def eliminar_configuracion():
    """Elimina la configuración existente"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
    print(" ELIMINAR CONFIGURACIÓN EXISTENTE")
    print("="*50)
    print(f"{Style.BRIGHT}{Fore.YELLOW}1.{Style.RESET_ALL} Eliminar BrowsingDataLifetime")
    print(f"{Style.BRIGHT}{Fore.YELLOW}2.{Style.RESET_ALL} Eliminar ClearBrowsingDataOnExitList")
    print(f"{Style.BRIGHT}{Fore.YELLOW}3.{Style.RESET_ALL} Eliminar ambas")
    print(f"{Style.BRIGHT}{Fore.YELLOW}0.{Style.RESET_ALL} Volver")
    print("="*50)
    
    opcion = input("\nSeleccione una opción: ")
    
    if opcion == "1":
        eliminar_valor_registro("BrowsingDataLifetime")
        print(f"\n{Fore.GREEN}BrowsingDataLifetime eliminada!")
    elif opcion == "2":
        eliminar_valor_registro("ClearBrowsingDataOnExitList")
        print(f"\n{Fore.GREEN}ClearBrowsingDataOnExitList eliminada!")
    elif opcion == "3":
        eliminar_valor_registro("BrowsingDataLifetime")
        eliminar_valor_registro("ClearBrowsingDataOnExitList")
        print(f"\n{Fore.GREEN}Ambas políticas eliminadas!")
    else:
        return
    
    input("\nPresione Enter para continuar...")

def main():
    """Función principal"""
    while True:
        opcion = mostrar_menu_principal()
        
        if opcion == "1":
            configurar_politica("BrowsingDataLifetime", es_browsing=True)
        elif opcion == "2":
            configurar_politica("ClearBrowsingDataOnExitList", es_browsing=False)
        elif opcion == "3":
            eliminar_configuracion()
        elif opcion == "0":
            print(f"\n{Fore.GREEN}¡Hasta pronto!\n")
            break
        else:
            print(f"\n{Fore.RED}Opción inválida. Intente nuevamente.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    # Requerir ejecución como administrador
    try:
        main()
    except PermissionError:
        print(f"\n{Fore.RED}ERROR: Este programa debe ejecutarse como administrador")
        input("Presione Enter para salir...")
    except Exception as e:
        print(f"\n{Fore.RED}Error inesperado: {e}")
        input("Presione Enter para salir...")