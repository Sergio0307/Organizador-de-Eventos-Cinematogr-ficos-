# Organizador-de-Eventos-Cinematogr-ficos-
Aplicación dedicada a una organización detallada de eventos de cine teniendo en cuenta el personal disponible, los recursos, y las escenas a tratar en cuestión, haciendo un trabajo más fácil para la gestión y planificación de las grabaciones en cuestión

🎥 Descripción del Proyecto
CINE EVENTOS PRO es una aplicación de software completa para planificar eventos cinematográficos que consumen recursos de un inventario limitado. El sistema garantiza que no existan conflictos en la asignación de recursos y respeta un conjunto de reglas y restricciones personalizadas específicas para la producción cinematográfica.

🎯 Objetivos Principales
Evitar conflictos de recursos: Ningún recurso puede asignarse a más de una producción simultáneamente
Validar restricciones: Todas las producciones deben cumplir con reglas específicas del dominio cinematográfico
Gestión inteligente: Búsqueda automática de horarios disponibles y validación en tiempo real

🎭 Dominio Elegido: Producción Cinematográfica
He elegido el dominio de producción cinematográfica porque:
Complejidad: Combina recursos físicos, personal especializado y equipamiento técnico
Restricciones reales: Existen reglas estrictas sobre combinaciones de recursos y personal
Planificación crítica: La coordinación de recursos es esencial para el éxito de cualquier producción
Escalabilidad: Puede gestionar desde pequeñas escenas hasta grandes producciones

✨ Características Principales
📅 Gestión de Calendario
Calendario interactivo con marcadores visuales
Vista diaria, mensual y anual de producciones
Marcadores de color según estado de producción

🎬 Planificación de Producciones
Creación de nuevas producciones con validación en tiempo real
Asignación de recursos y personal especializado
Validación automática de restricciones y conflictos
Cálculo automático de costos estimados

📊 Gestión de Recursos
Inventario completo de recursos físicos
Base de datos de personal especializado
Control de disponibilidad en tiempo real
Historial de uso de recursos

⚙️ Sistema de Validación
9 tipos de errores de validación diferentes
Validación en tiempo real durante la planificación
Sistema de colores para indicar estado de validación
Sugerencias automáticas para corrección

💾 Persistencia de Datos
Guardado automático cada 5 minutos
Carga inicial desde archivos JSON
Backup automático de configuración
Exportación de estadísticas

Flujo de Datos
Interfaz de Usuario (Tkinter) ←→ Controlador (frontend.py)
Controlador ←→ Lógica de Negocio (backend3.py)
Lógica de Negocio ←→ Gestor de Datos (backend.py)
Gestor de Datos ←→ Archivos JSON (persistencia)

Requisitos del Sistema
Software Requerido
Python 3.8 o superior

Bibliotecas Python:
text
tkinter (incluido en Python)
Pillow (PIL) >= 9.0.0
tkcalendar >= 1.6.1

Hardware Recomendado ( Broma hahaha)
Procesador: Intel i5 o equivalente
RAM: 4 GB mínimo
Espacio en disco: 100 MB
Resolución de pantalla: 1280x720 mínimo

Pantalla Principal:
Pantalla de Bienvenida: Presentación de la aplicación
Menú Principal: Acceso a todas las funcionalidades
Navegación intuitiva: Botones descriptivos con iconos

Tecnologías Utilizadas
Lenguajes y Frameworks
Python 3.10+: Lenguaje principal
Tkinter: Interfaz gráfica nativa
Pillow (PIL): Procesamiento de imágenes
tkcalendar: Widget de calendario avanzado

Estructura de Código
Programación orientada a objetos
Separación de responsabilidades
Manejo de excepciones robusto
Documentación en línea extensa

¡Gracias por usar CINE EVENTOS PRO!
Este proyecto representa meses de desarrollo dedicado a resolver problemas reales en la planificación de producciones cinematográficas. Esperamos que esta herramienta sea invaluable para tu trabajo y te invitamos a contribuir a su mejora continua.

¡Lights, Camera, Action! 🎬
