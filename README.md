# 🛠️ Script de Configuración de Políticas de Chrome (BrowsingDataLifetime & ClearBrowsingDataOnExitList)

Este script de terminal permite **configurar fácilmente dos políticas de privacidad de Google Chrome** mediante una interfaz en español, clara y visualmente atractiva:

- [`BrowsingDataLifetime`](https://chromeenterprise.google/policies/?policy=BrowsingDataLifetime)
- [`ClearBrowsingDataOnExitList`](https://chromeenterprise.google/policies/?policy=ClearBrowsingDataOnExitList)

Ideal para entornos empresariales, instituciones educativas o usuarios que desean mejorar su privacidad de navegación.

---

## ✨ Características Principales

✅ **Interfaz amigable en español**  
Diseñada con `Colorama` para mostrar menús y mensajes con colores y formatos que mejoran la experiencia del usuario.

✅ **Menú principal interactivo**  
Ofrece tres funciones clave:
1. Configurar `BrowsingDataLifetime`
2. Configurar `ClearBrowsingDataOnExitList`
3. Eliminar configuraciones existentes

✅ **Selección de datos personalizada**  
- Lista numerada de tipos de datos con descripción clara en español  
- Selección o deselección mediante números separados por comas  
- Indicadores visuales: `✓✓` (activo) y `✗✗` (inactivo)

✅ **Configuración flexible del tiempo (BrowsingDataLifetime)**  
- Opciones predefinidas: 1 día, 2 días, 7 días, etc.  
- Opción personalizada con validación de entrada  
- Posibilidad de asignar un tiempo diferente a cada tipo de dato

✅ **Gestión completa del registro (Windows Registry)**  
- Crea automáticamente las claves necesarias si no existen  
- Elimina políticas previas de forma segura  
- Escribe datos en formato JSON válido según las políticas de Chrome

✅ **Robustez y validación**  
- Detecta si se requieren permisos de administrador  
- Maneja errores comunes de permisos y entradas incorrectas  
- Validaciones detalladas para evitar fallos en la ejecución

---

## 🔧 Requisitos

- 🖥️ Sistema operativo: Windows  
- 🐍 Python 3.7 o superior  
- 📦 Paquete adicional: `colorama`

Instalación de Colorama:
```bash
pip install colorama
```
---

## 🚀 Cómo usar

1. Ejecuta el script con permisos de administrador.
2. Sigue el menú interactivo en pantalla.
3. Elige y configura los tipos de datos y tiempos según tus preferencias.
4. ¡Listo! Las políticas quedarán aplicadas automáticamente en el registro de Windows.

---

## 📁 Estructura del proyecto

```
📂 chrome-policy-config
├── script.py
├── README.md
└── requirements.txt
```

---

## 🛑 Advertencia

Este script **modifica directamente el Registro de Windows**. Se recomienda usar con precaución y siempre ejecutar con permisos de administrador. Úsalo bajo tu propio riesgo.

---

## 💡 Ejemplo visual (próximamente)

> Estamos trabajando en agregar capturas de pantalla o una demo animada para mostrar la experiencia en terminal. ¡Estén atentos!

---

## 🧑‍💻 Autor

Desarrollado por MCPRDev

