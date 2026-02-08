# frontend.py - AGREGAR ESTOS MÉTODOS A LA CLASE
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import backend
from datetime import datetime
import json
import os
from datetime import datetime
from tkcalendar import Calendar

class AplicacionEventos:
    def __init__(self, gestor_datos, logica_negocio):
        # Inicializar backend
        self.gestor = gestor_datos
        self.logica = logica_negocio
        
        # Crear ventana principal
        self.window = tk.Tk()
        self.window.title("🎬 CINE EVENTOS PRO - Organizador De Eventos Cinematográficos")
        
        # Obtener dimensiones de la pantalla
        self.ancho_pantalla = self.window.winfo_screenwidth()
        self.alto_pantalla = self.window.winfo_screenheight()
        
        # Configurar tamaño de ventana (90% de la pantalla)
        self.ancho_ventana = int(self.ancho_pantalla * 0.9)
        self.alto_ventana = int(self.alto_pantalla * 0.9)
        
        # Posicionar ventana centrada
        pos_x = (self.ancho_pantalla - self.ancho_ventana) // 2
        pos_y = (self.alto_pantalla - self.alto_ventana) // 2
        
        # Configurar geometría de la ventana
        self.window.geometry(f"{self.ancho_ventana}x{self.alto_ventana}+{pos_x}+{pos_y}")
        
        # Hacer la ventana redimensionable
        self.window.resizable(True, True)
        
        # Configurar color de fondo
        self.window.configure(bg="#1a1a2e")
        self.window.attributes("-alpha", 0.95)
        
        # Configurar icono de la aplicación (si existe)
        try:
            self.window.iconbitmap('icon.ico')
        except:
            pass
        
        # Configurar cierre de ventana para guardar datos
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        # Atajo de teclado con el número 9 para pantalla completa
        self.window.bind("9", self.toggle_fullscreen)  # Tecla 9 normal
        self.window.bind("<Key-9>", self.toggle_fullscreen)  # También
        self.window.bind("<KP_9>", self.toggle_fullscreen)   # Teclado numérico
        self.window.bind("<Escape>", self.exit_fullscreen)   # ESC para salir
        
        # Variables para fuentes
        self.titulo_font = ("Arial", 20, "bold")
        self.subtitulo_font = ("Arial", 14)
        self.texto_font = ("Arial", 11)
        self.boton_font = ("Arial", 12, "bold")
        
        # Cargar imagen de fondo
        self.cargar_imagen_fondo()
        
        # Programar guardado automático
        self.guardado_automatico()
        
        # Mostrar pantalla inicial
        self.mostrar_pantalla_inicial()
    
    def cargar_imagen_fondo(self):
        """Carga y configura la imagen de fondo"""
        try:
            imagen = Image.open("newcinema.jpg")  
            # Redimensionar al tamaño de la ventana
            imagen = imagen.resize((self.ancho_ventana, self.alto_ventana), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(imagen)
        except FileNotFoundError:
            print("Imagen no encontrada, usando fondo blanco")
            self.bg_image = None
    
    def limpiar_pantalla(self):
        """Elimina todos los widgets de la ventana"""
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Volver a colocar el fondo si existe
        if hasattr(self, 'bg_image') and self.bg_image:
            self.fondo = tk.Label(self.window, image=self.bg_image)
            self.fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    def mostrar_pantalla_inicial(self):
        """Pantalla de bienvenida"""
        self.limpiar_pantalla()
        
        # Frame para contenido
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=800, height=400)
        
        # Label de título
        label_titulo = tk.Label(frame_principal, 
            text="🎬 CINE EVENTOS PRO 🎬", 
            font=("Arial", 20, "bold italic"), 
            bg="white", fg="darkblue")
        label_titulo.pack(pady=30)
        
        # Subtítulo
        label_subtitulo = tk.Label(frame_principal, 
            text="Welcome to our Company dedicated to organizing events\ndevoted to Cinema par Excellence", 
            font=("Arial", 14), 
            bg="white", fg="black", justify="center")
        label_subtitulo.pack(pady=10)
        
        # Separador
        ttk.Separator(frame_principal, orient='horizontal').pack(fill='x', pady=20, padx=20)
        
        # Label central
        label_central = tk.Label(frame_principal, 
            text="Join us to create unforgettable cinematic experiences!", 
            font=("Arial", 14, "italic"), 
            bg="white", fg="darkred")
        label_central.pack(pady=20)
        
        # Botón para continuar
        boton_continuar = tk.Button(frame_principal, 
            text='START YOUR JOURNEY 🚀', 
            font=("Arial", 16, "bold"), 
            bg="#4CAF50", fg="white", 
            relief='raised',
            bd=3,
            width=25,
            height=2,
            command=self.mostrar_menu_principal)
        boton_continuar.pack(pady=30)
    
    def mostrar_menu_principal(self):
        """Menú principal de la aplicación"""
        self.limpiar_pantalla()
        
        # Frame para el menú
        frame_menu = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_menu.place(relx=0.5, rely=0.5, anchor="center", width=900, height=500)
        
        # Título del menú
        titulo_menu = tk.Label(frame_menu,
            text="📋 MAIN MENU - EVENT ORGANIZER",
            font=("Arial", 20, "bold"),
            bg="white", fg="darkblue",
            relief="groove",
            bd=2,
            padx=20,
            pady=10)
        titulo_menu.pack(pady=20)
        
        # Frame para los botones del menú
        frame_botones = tk.Frame(frame_menu, bg="white")
        frame_botones.pack(pady=40, padx=50, fill="both", expand=True)
        
        # Botones de navegación
        botones_menu = [
            ("🎬 RESOURCE MANAGEMENT", self.mostrar_gestion_recursos),
            ("👥 STAFF MANAGEMENT", self.mostrar_gestion_personal),
            ("📊 SCENE PRODUCTION", self.mostrar_produccion_escenas),
            ("📅 PRODUCTION CALENDAR", self.mostrar_calendario_produccion),
            ("📈 EVENT STATISTICS", self.mostrar_estadisticas),
            ("⚙️ SETTINGS", self.mostrar_configuracion),
            ("🚪 EXIT", self.cerrar_aplicacion)
        ]
        
        for texto, comando in botones_menu:
            boton = tk.Button(frame_botones,
                text=texto,
                font=("Arial", 12, "bold"),
                bg="#2196F3",
                fg="white",
                relief="raised",
                bd=2,
                width=30,
                height=2,
                command=comando)
            boton.pack(pady=8)
    
    def mostrar_gestion_recursos(self):
        """Pantalla de gestión de recursos"""
        self.limpiar_pantalla()
        
        # Frame principal
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)
        
        # Título
        titulo = tk.Label(frame_principal,
            text="📦 RESOURCE MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg="white", fg="darkgreen")
        titulo.pack(pady=15)
        
        # Frame contenedor para scroll
        frame_contenedor = tk.Frame(frame_principal, bg="white")
        frame_contenedor.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(frame_contenedor, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg="white")
        
        # Configurar scroll
        frame_lista.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cabecera de la tabla
        tk.Label(frame_lista, text="RESOURCE", 
                font=("Arial", 12, "bold"), bg="lightgray", 
                width=50, anchor="w", relief="raised", bd=1).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(frame_lista, text="QUANTITY", 
                font=("Arial", 12, "bold"), bg="lightgray", 
                width=20, relief="raised", bd=1).grid(row=0, column=1, padx=5, pady=5)
        
        # Obtener recursos del backend
        recursos = self.gestor.obtener_recursos()
        
        # Mostrar recursos
        for i, (recurso, cantidad) in enumerate(recursos.items()):
            # Alternar colores para mejor legibilidad
            color_fondo = "#f0f0f0" if i % 2 == 0 else "#ffffff"
            
            tk.Label(frame_lista, text=recurso,
                    font=("Arial", 11), bg=color_fondo, 
                    width=50, anchor="w", relief="groove", bd=1).grid(
                    row=i+1, column=0, padx=5, pady=3, sticky="w")
            tk.Label(frame_lista, text=f"{cantidad} units",
                    font=("Arial", 11, "bold"), bg=color_fondo, 
                    fg="darkgreen", relief="groove", bd=1).grid(
                    row=i+1, column=1, padx=5, pady=3)
        
        # Asegurar que el frame_lista se expanda
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(1, weight=0)
        
        # Configurar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Frame para botones (FUERA del área de scroll)
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        # Botones de acción
        botones = [
            ("➕ Add Resource", "#4CAF50", self.agregar_recurso),
            ("➖ Remove Resource", "#F44336", self.eliminar_recurso),
            ("🔄 Refresh", "#FF9800", self.mostrar_gestion_recursos),
            ("⬅️ Back to Menu", "#607D8B", self.mostrar_menu_principal)
        ]
        
        for texto, color, comando in botones:
            tk.Button(frame_botones, text=texto,
                     font=("Arial", 11, "bold"),
                     bg=color, fg="white",
                     relief="raised",
                     bd=2,
                     padx=15,
                     pady=8,
                     command=comando).pack(side="left", padx=10)
    
    def mostrar_gestion_personal(self):
        """Pantalla de gestión de personal"""
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)
        
        titulo = tk.Label(frame_principal,
            text="👥 STAFF MANAGEMENT",
            font=("Arial", 18, "bold"),
            bg="white", fg="darkred")
        titulo.pack(pady=15)
        
        # Frame contenedor para scroll
        frame_contenedor = tk.Frame(frame_principal, bg="white")
        frame_contenedor.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(frame_contenedor, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg="white")
        
        # Configurar scroll
        frame_lista.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cabecera
        tk.Label(frame_lista, text="POSITION", 
                font=("Arial", 12, "bold"), bg="lightgray", 
                width=50, anchor="w", relief="raised", bd=1).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(frame_lista, text="STAFF", 
                font=("Arial", 12, "bold"), bg="lightgray", 
                width=20, relief="raised", bd=1).grid(row=0, column=1, padx=5, pady=5)
        
        # Obtener personal del backend
        personal = self.gestor.obtener_personal()
        
        # Mostrar personal
        for i, (puesto, cantidad) in enumerate(personal.items()):
            # Alternar colores para mejor legibilidad
            color_fondo = "#f0f0f0" if i % 2 == 0 else "#ffffff"
            
            tk.Label(frame_lista, text=puesto,
                    font=("Arial", 11), bg=color_fondo, 
                    width=50, anchor="w", relief="groove", bd=1).grid(
                    row=i+1, column=0, padx=5, pady=3, sticky="w")
            tk.Label(frame_lista, text=f"{cantidad} people",
                    font=("Arial", 11, "bold"), bg=color_fondo, 
                    fg="darkred", relief="groove", bd=1).grid(
                    row=i+1, column=1, padx=5, pady=3)
        
        # Asegurar que el frame_lista se expanda
        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(1, weight=0)
        
        # Configurar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Frame para botones (FUERA del área de scroll)
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        # Botones de acción
        botones = [
            ("➕ Hire Staff", "#4CAF50", self.agregar_personal),
            ("➖ Dismiss Staff", "#F44336", self.eliminar_personal),
            ("🔄 Refresh", "#FF9800", self.mostrar_gestion_personal),
            ("⬅️ Back to Menu", "#607D8B", self.mostrar_menu_principal)
        ]
        
        for texto, color, comando in botones:
            tk.Button(frame_botones, text=texto,
                     font=("Arial", 11, "bold"),
                     bg=color, fg="white",
                     relief="raised",
                     bd=2,
                     padx=15,
                     pady=8,
                     command=comando).pack(side="left", padx=10)
    
    def mostrar_calendario_produccion(self):
        """Nueva pantalla: Calendario de Producción"""
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=1200, height=700)
        
        # Título
        titulo = tk.Label(frame_principal,
            text="📅 PRODUCTION CALENDAR",
            font=("Arial", 20, "bold"),
            bg="white", fg="#2E86C1")
        titulo.pack(pady=15)
        
        # Frame para calendario y detalles
        frame_contenido = tk.Frame(frame_principal, bg="white")
        frame_contenido.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Frame izquierdo para calendario
        frame_calendario = tk.Frame(frame_contenido, bg="white", relief="groove", bd=2)
        frame_calendario.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # === PARTE IZQUIERDA: CALENDARIO ===
        tk.Label(frame_calendario, text="📅 Select Date", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        # Calendario
        self.calendar = Calendar(frame_calendario, 
                                selectmode='day',
                                year=datetime.now().year,
                                month=datetime.now().month,
                                day=datetime.now().day,
                                date_pattern='yyyy-mm-dd',
                                font=("Arial", 10))
        self.calendar.pack(pady=10, padx=10, fill="both", expand=True)
        
        # === BOTONES DEL CALENDARIO (NUEVA SECCIÓN) ===
        frame_botones_calendario = tk.Frame(frame_calendario, bg="white")
        frame_botones_calendario.pack(pady=10)
        
        # Botón para añadir nueva producción
        tk.Button(frame_botones_calendario, text="➕ Add New Production",
                 font=("Arial", 11, "bold"),
                 bg="#27AE60", fg="white",
                 command=self.agregar_produccion).pack(side="left", padx=5)
        
        # Botón para ver producciones del día seleccionado
        tk.Button(frame_botones_calendario, text="📋 View Day Productions",
                 font=("Arial", 11),
                 bg="#3498DB", fg="white",
                 command=self.ver_producciones_dia).pack(side="left", padx=5)
        
        # BOTÓN NUEVO: Ir al día de hoy
        tk.Button(frame_botones_calendario, text="📅 Go to Today",
                 font=("Arial", 11),
                 bg="#F39C12", fg="white",
                 command=self.ir_a_hoy).pack(side="left", padx=5)
        
        # Frame derecho para detalles
        frame_detalles = tk.Frame(frame_contenido, bg="white", relief="groove", bd=2)
        frame_detalles.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # === PARTE DERECHA: DETALLES ===
        tk.Label(frame_detalles, text="📊 Production Details", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        # Frame para mostrar detalles
        self.frame_info_dia = tk.Frame(frame_detalles, bg="white")
        self.frame_info_dia.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Mensaje inicial
        tk.Label(self.frame_info_dia, 
                text="Select a date to view or add productions",
                font=("Arial", 12), 
                bg="white", fg="gray").pack(expand=True)
        
        # Botones inferiores
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        botones = [
            ("🗓️ View Month Productions", "#9B59B6", self.ver_producciones_mes),
            ("📊 Production Statistics", "#F39C12", self.ver_estadisticas_produccion),
            ("🔄 Refresh Calendar", "#FF9800", self.mostrar_calendario_produccion),
            ("⬅️ Back to Menu", "#607D8B", self.mostrar_menu_principal)
        ]
        
        for texto, color, comando in botones:
            tk.Button(frame_botones, text=texto,
                     font=("Arial", 11),
                     bg=color, fg="white",
                     relief="raised",
                     bd=2,
                     padx=10,
                     pady=5,
                     command=comando).pack(side="left", padx=5)
    
    def ir_a_hoy(self):
        """Va al día actual en el calendario"""
        hoy = datetime.now()
        self.calendar.selection_set(hoy)
        self.ver_producciones_dia()
        
         
    def ver_producciones_dia(self):
        """Muestra las producciones del día seleccionado"""
        fecha_seleccionada = self.calendar.get_date()
        
        # Limpiar frame de detalles
        for widget in self.frame_info_dia.winfo_children():
            widget.destroy()
        
        # Obtener producciones del día
        producciones = self.gestor.obtener_producciones_por_fecha(fecha_seleccionada)
        
        if not producciones:
            tk.Label(self.frame_info_dia, 
                    text=f"No productions scheduled for {fecha_seleccionada}",
                    font=("Arial", 12), 
                    bg="white", fg="gray").pack(expand=True)
            return
        
        # Título con fecha
        tk.Label(self.frame_info_dia, 
                text=f"Productions for {fecha_seleccionada}",
                font=("Arial", 14, "bold"), 
                bg="white", fg="#2E86C1").pack(pady=10)
        
        # Frame para lista de producciones con scroll
        frame_lista_container = tk.Frame(self.frame_info_dia, bg="white")
        frame_lista_container.pack(fill="both", expand=True, pady=5)
        
        canvas = tk.Canvas(frame_lista_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_lista_container, orient="vertical", command=canvas.yview)
        frame_lista = tk.Frame(canvas, bg="white")
        
        frame_lista.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_lista, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar cada producción
        for i, prod in enumerate(producciones):
            color_fondo = "#E8F4F8" if i % 2 == 0 else "#FFFFFF"
            
            frame_prod = tk.Frame(frame_lista, bg=color_fondo, relief="groove", bd=1)
            frame_prod.pack(fill="x", pady=5, padx=5)
            
            # Información básica
            tk.Label(frame_prod, 
                    text=f"🎬 {prod.get('titulo', 'Production')}",
                    font=("Arial", 12, "bold"), 
                    bg=color_fondo, anchor="w").pack(fill="x", padx=10, pady=5)
            
            tk.Label(frame_prod, 
                    text=f"Scene: {prod.get('escena', 'Not specified')}",
                    font=("Arial", 10), 
                    bg=color_fondo, anchor="w").pack(fill="x", padx=10)
            
            tk.Label(frame_prod, 
                    text=f"Duration: {prod.get('duracion_horas', 0)} hours",
                    font=("Arial", 10), 
                    bg=color_fondo, anchor="w").pack(fill="x", padx=10)
            
            tk.Label(frame_prod, 
                    text=f"Status: {prod.get('estado', 'programada')}",
                    font=("Arial", 10), 
                    bg=color_fondo, fg=self.obtener_color_estado(prod.get('estado')),
                    anchor="w").pack(fill="x", padx=10, pady=5)
            
            # Botones de acción para esta producción
            frame_botones_prod = tk.Frame(frame_prod, bg=color_fondo)
            frame_botones_prod.pack(fill="x", padx=10, pady=5)
            
            tk.Button(frame_botones_prod, text="👁️ View Details",
                     font=("Arial", 9),
                     bg="#3498DB", fg="white",
                     command=lambda p=prod: self.ver_detalles_produccion(p)).pack(side="left", padx=2)
            
            tk.Button(frame_botones_prod, text="✏️ Edit",
                     font=("Arial", 9),
                     bg="#F39C12", fg="white",
                     command=lambda p=prod: self.editar_produccion(p)).pack(side="left", padx=2)
            
            tk.Button(frame_botones_prod, text="❌ Delete",
                     font=("Arial", 9),
                     bg="#E74C3C", fg="white",
                     command=lambda p=prod: self.eliminar_produccion(p)).pack(side="left", padx=2)
    
    def obtener_color_estado(self, estado):
        """Devuelve color según estado"""
        colores = {
            'programada': '#3498DB',  # Azul
            'en_progreso': '#F39C12', # Naranja
            'completada': '#27AE60',  # Verde
            'cancelada': '#E74C3C'    # Rojo
        }
        return colores.get(estado, '#95A5A6')  # Gris por defecto
    
    def agregar_produccion(self, fecha=None):
        """Abre diálogo para agregar nueva producción"""
        # Si no se pasa fecha, usar la seleccionada
        if fecha is None:
            fecha_seleccionada = self.calendar.get_date()
        else:
            fecha_seleccionada = fecha
            # Marcar fecha en calendario
            año, mes, dia = map(int, fecha_seleccionada.split('-'))
            self.calendar.selection_set(datetime(año, mes, dia))
        
        dialogo = tk.Toplevel(self.window)
        dialogo.title(f"Add Production - {fecha_seleccionada}")
        dialogo.geometry("900x700")
        dialogo.configure(bg="white")
        dialogo.transient(self.window)
        dialogo.grab_set()
        
        dialogo.geometry(f"900x700+{self.window.winfo_x()+50}+{self.window.winfo_y()+50}")
        
        # Título
        tk.Label(dialogo, text=f"🎬 ADD NEW PRODUCTION\nDate: {fecha_seleccionada}", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        # Frame con scroll
        frame_form_container = tk.Frame(dialogo, bg="white")
        frame_form_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        canvas = tk.Canvas(frame_form_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_form_container, orient="vertical", command=canvas.yview)
        frame_form = tk.Frame(canvas, bg="white")
        
        frame_form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_form, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Variables
        self.titulo_var = tk.StringVar()
        self.escena_var = tk.StringVar()
        self.duracion_var = tk.IntVar(value=8)
        
        # Campos
        tk.Label(frame_form, text="Production Title:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        entry_titulo = tk.Entry(frame_form, textvariable=self.titulo_var, 
                               font=("Arial", 11), width=50)
        entry_titulo.pack(fill="x", pady=5)
        entry_titulo.focus_set()
        
        # Escena
        tk.Label(frame_form, text="Select Scene:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        
        escenas_disponibles = self.gestor.obtener_escenas()
        if escenas_disponibles:
            self.escena_var.set(escenas_disponibles[0])
            combobox_escena = ttk.Combobox(frame_form, textvariable=self.escena_var,
                                          values=escenas_disponibles, state="readonly",
                                          font=("Arial", 11), width=48)
            combobox_escena.pack(fill="x", pady=5)
        else:
            tk.Label(frame_form, text="No scenes available. Add scenes first.",
                    font=("Arial", 10), bg="white", fg="red").pack(pady=5)
        
        # Duración
        tk.Label(frame_form, text="Duration (hours):", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        spinbox_duracion = tk.Spinbox(frame_form, from_=1, to=24, 
                                     textvariable=self.duracion_var,
                                     font=("Arial", 11), width=10)
        spinbox_duracion.pack(anchor="w", pady=5)
        
        # Descripción
        tk.Label(frame_form, text="Description:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        text_descripcion = tk.Text(frame_form, font=("Arial", 11), 
                                  height=4, width=60)
        text_descripcion.pack(fill="x", pady=5)
        
        # Recursos
        tk.Label(frame_form, text="\n📦 Resources Required:", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=10)
        
        recursos_disponibles = self.gestor.obtener_recursos()
        self.vars_recursos = {}
        
        for recurso in recursos_disponibles.keys():
            frame_recurso = tk.Frame(frame_form, bg="white")
            frame_recurso.pack(fill="x", pady=2)
            
            var_cantidad = tk.IntVar(value=0)
            self.vars_recursos[recurso] = var_cantidad
            
            tk.Label(frame_recurso, text=recurso, 
                    font=("Arial", 10), bg="white", width=40, anchor="w", wraplength=300).pack(side="left")
            
            spinbox_cantidad = tk.Spinbox(frame_recurso, from_=0, 
                                         to=recursos_disponibles[recurso],
                                         textvariable=var_cantidad,
                                         font=("Arial", 10), width=10)
            spinbox_cantidad.pack(side="left", padx=10)
            
            tk.Label(frame_recurso, 
                    text=f"(Max: {recursos_disponibles[recurso]})",
                    font=("Arial", 9), bg="white", fg="gray").pack(side="left")
        
        # Personal
        tk.Label(frame_form, text="\n👥 Staff Required:", 
                font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=10)
        
        personal_disponible = self.gestor.obtener_personal()
        self.vars_personal = {}
        
        for puesto in personal_disponible.keys():
            frame_puesto = tk.Frame(frame_form, bg="white")
            frame_puesto.pack(fill="x", pady=2)
            
            var_cantidad = tk.IntVar(value=0)
            self.vars_personal[puesto] = var_cantidad
            
            tk.Label(frame_puesto, text=puesto, 
                    font=("Arial", 10), bg="white", width=40, anchor="w", wraplength=300).pack(side="left")
            
            spinbox_cantidad = tk.Spinbox(frame_puesto, from_=0, 
                                         to=personal_disponible[puesto],
                                         textvariable=var_cantidad,
                                         font=("Arial", 10), width=10)
            spinbox_cantidad.pack(side="left", padx=10)
            
            tk.Label(frame_puesto, 
                    text=f"(Max: {personal_disponible[puesto]})",
                    font=("Arial", 9), bg="white", fg="gray").pack(side="left")
        
        def procesar_produccion():
            # Recoger datos
            titulo = self.titulo_var.get().strip()
            escena = self.escena_var.get()
            duracion = self.duracion_var.get()
            descripcion = text_descripcion.get("1.0", tk.END).strip()
            
            if not titulo:
                messagebox.showerror("Error", "Please enter a production title")
                return
            
            # Recoger recursos
            recursos_utilizados = {}
            for recurso, var in self.vars_recursos.items():
                cantidad = var.get()
                if cantidad > 0:
                    recursos_utilizados[recurso] = cantidad
            
            # Recoger personal
            personal_asignado = {}
            for puesto, var in self.vars_personal.items():
                cantidad = var.get()
                if cantidad > 0:
                    personal_asignado[puesto] = cantidad
            
            # Crear datos
            produccion_data = {
                'titulo': titulo,
                'escena': escena,
                'duracion_horas': duracion,
                'descripcion': descripcion,
                'recursos_utilizados': recursos_utilizados,
                'personal_asignado': personal_asignado,
                'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Verificar conflictos
            conflictos = self.logica.verificar_conflictos_recursos(
                fecha_seleccionada, recursos_utilizados, personal_asignado)
            
            if conflictos:
                mensaje_conflicto = "Resource/Staff conflicts found:\n\n" + "\n".join(conflictos)
                confirmar = messagebox.askyesno("Conflicts Found", 
                    f"{mensaje_conflicto}\n\nDo you want to continue anyway?")
                if not confirmar:
                    return
            
            # Calcular costo
            costo = self.logica.calcular_costo_produccion(produccion_data)
            produccion_data['costo_estimado'] = costo
            
            # Guardar producción
            produccion_id = self.gestor.agregar_produccion(fecha_seleccionada, produccion_data)
            
            if produccion_id:
                messagebox.showinfo("Success", 
                    f"Production '{titulo}' added successfully!\n\n"
                    f"Estimated Cost: ${costo:,.2f}\n"
                    f"Resources used: {sum(recursos_utilizados.values())}\n"
                    f"Staff assigned: {sum(personal_asignado.values())}")
                dialogo.destroy()
                self.ver_producciones_dia()
            else:
                messagebox.showerror("Error", "Could not add production")
        
        # Botones
        frame_botones_dialogo = tk.Frame(dialogo, bg="white")
        frame_botones_dialogo.pack(pady=20)
        
        tk.Button(frame_botones_dialogo, text="💾 Save Production",
                 font=("Arial", 11, "bold"),
                 bg="#27AE60", fg="white",
                 command=procesar_produccion).pack(side="left", padx=10)
        
        tk.Button(frame_botones_dialogo, text="✖️ Cancel",
                 font=("Arial", 11),
                 bg="#95A5A6", fg="white",
                 command=dialogo.destroy).pack(side="left", padx=10) 
    
    def ver_detalles_produccion(self, produccion):
        """Muestra detalles completos de una producción"""
        dialogo = tk.Toplevel(self.window)
        dialogo.title(f"🎬 {produccion.get('titulo', 'Production Details')}")
        dialogo.geometry("800x600")
        dialogo.configure(bg="white")
        dialogo.transient(self.window)
        dialogo.grab_set()
        
        dialogo.geometry(f"800x600+{self.window.winfo_x()+100}+{self.window.winfo_y()+50}")
        
        # Frame con scroll
        frame_container = tk.Frame(dialogo, bg="white")
        frame_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        canvas = tk.Canvas(frame_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
        frame_contenido = tk.Frame(canvas, bg="white")
        
        frame_contenido.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_contenido, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ===== INFORMACIÓN PRINCIPAL =====
        tk.Label(frame_contenido, 
                text=f"🎬 {produccion.get('titulo', 'Production')}",
                font=("Arial", 18, "bold"), 
                bg="white", fg="#2E86C1").pack(pady=15)
        
        # Frame para información
        frame_info_basica = tk.Frame(frame_contenido, bg="white", relief="groove", bd=2)
        frame_info_basica.pack(fill="x", pady=10, padx=10)
        
        # FECHA DESTACADA
        tk.Label(frame_info_basica, text="📅 PRODUCTION DATE:", 
                font=("Arial", 12, "bold"), bg="white", fg="#D35400").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(frame_info_basica, text=f"{produccion.get('fecha', 'Unknown')}", 
                font=("Arial", 14, "bold"), bg="white", fg="#E74C3C").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        info_fields = [
            ("🎭 Scene:", produccion.get('escena', 'Not specified')),
            ("⏱️ Duration:", f"{produccion.get('duracion_horas', 0)} hours"),
            ("💰 Estimated Cost:", f"${produccion.get('costo_estimado', 0):,.2f}"),
            ("📝 Status:", produccion.get('estado', 'programada')),
            ("🆔 ID:", produccion.get('id', 'Unknown')),
            ("📅 Created:", produccion.get('fecha_creacion', 'Unknown'))
        ]
        
        for i, (label, value) in enumerate(info_fields, start=1):
            tk.Label(frame_info_basica, text=label, 
                    font=("Arial", 11, "bold"), 
                    bg="white", anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=3)
            tk.Label(frame_info_basica, text=value, 
                    font=("Arial", 11), 
                    bg="white", anchor="w").grid(row=i, column=1, sticky="w", padx=10, pady=3)
        
        # ===== RECURSOS UTILIZADOS =====
        if 'recursos_utilizados' in produccion and produccion['recursos_utilizados']:
            tk.Label(frame_contenido, text="\n📦 RESOURCES USED:", 
                    font=("Arial", 14, "bold"), bg="white", fg="#27AE60").pack(anchor="w", pady=(20, 10), padx=10)
            
            frame_recursos = tk.Frame(frame_contenido, bg="#F8F9F9", relief="groove", bd=1)
            frame_recursos.pack(fill="x", pady=5, padx=10)
            
            total_recursos = 0
            for recurso, cantidad in produccion['recursos_utilizados'].items():
                total_recursos += cantidad
                frame_recurso = tk.Frame(frame_recursos, bg="#F8F9F9")
                frame_recurso.pack(fill="x", pady=3, padx=10)
                
                tk.Label(frame_recurso, text=f"  • {recurso}:", 
                        font=("Arial", 11), bg="#F8F9F9", width=40, anchor="w").pack(side="left")
                tk.Label(frame_recurso, text=f"{cantidad} units", 
                        font=("Arial", 11, "bold"), bg="#F8F9F9", fg="#2980B9").pack(side="right")
            
            tk.Label(frame_recursos, text=f"\n📊 TOTAL RESOURCES: {total_recursos} units", 
                    font=("Arial", 11, "bold"), bg="#F8F9F9", fg="#2C3E50").pack(anchor="w", pady=(5, 10), padx=10)
        else:
            tk.Label(frame_contenido, text="\n📦 No resources used for this production", 
                    font=("Arial", 11), bg="white", fg="gray").pack(anchor="w", pady=10, padx=10)
        
        # ===== PERSONAL ASIGNADO =====
        if 'personal_asignado' in produccion and produccion['personal_asignado']:
            tk.Label(frame_contenido, text="\n👥 STAFF ASSIGNED:", 
                    font=("Arial", 14, "bold"), bg="white", fg="#9B59B6").pack(anchor="w", pady=(20, 10), padx=10)
            
            frame_personal = tk.Frame(frame_contenido, bg="#F4ECF7", relief="groove", bd=1)
            frame_personal.pack(fill="x", pady=5, padx=10)
            
            total_personal = 0
            for puesto, cantidad in produccion['personal_asignado'].items():
                total_personal += cantidad
                frame_puesto = tk.Frame(frame_personal, bg="#F4ECF7")
                frame_puesto.pack(fill="x", pady=3, padx=10)
                
                tk.Label(frame_puesto, text=f"  • {puesto}:", 
                        font=("Arial", 11), bg="#F4ECF7", width=40, anchor="w").pack(side="left")
                tk.Label(frame_puesto, text=f"{cantidad} people", 
                        font=("Arial", 11, "bold"), bg="#F4ECF7", fg="#8E44AD").pack(side="right")
            
            tk.Label(frame_personal, text=f"\n👥 TOTAL STAFF: {total_personal} people", 
                    font=("Arial", 11, "bold"), bg="#F4ECF7", fg="#2C3E50").pack(anchor="w", pady=(5, 10), padx=10)
        
        # ===== DESCRIPCIÓN =====
        tk.Label(frame_contenido, text="\n📝 DESCRIPTION:", 
                font=("Arial", 14, "bold"), bg="white").pack(anchor="w", pady=(20, 10), padx=10)
        
        frame_desc = tk.Frame(frame_contenido, bg="#F8F9F9", relief="groove", bd=1)
        frame_desc.pack(fill="x", pady=5, padx=10)
        
        text_desc = tk.Text(frame_desc, font=("Arial", 11), 
                           height=5, width=70, wrap="word", bg="#F8F9F9")
        text_desc.insert("1.0", produccion.get('descripcion', 'No description available'))
        text_desc.config(state="disabled")
        text_desc.pack(pady=10, padx=10)
        
        # ===== BOTONES =====
        frame_botones = tk.Frame(dialogo, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="📅 View in Calendar",
                 font=("Arial", 11, "bold"),
                 bg="#3498DB", fg="white",
                 command=lambda: self.ver_en_calendario(produccion)).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="✏️ Edit",
                 font=("Arial", 11),
                 bg="#F39C12", fg="white",
                 command=lambda: self.editar_produccion(produccion)).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="✅ Mark as Complete",
                 font=("Arial", 11),
                 bg="#27AE60", fg="white",
                 command=lambda: self.marcar_completada(produccion)).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="🗑️ DELETE PRODUCTION",
                 font=("Arial", 11, "bold"),
                 bg="#E74C3C", fg="white",
                 command=lambda: self.eliminar_produccion_desde_calendario(produccion)).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="Close",
                 font=("Arial", 11),
                 bg="#95A5A6", fg="white",
                 command=dialogo.destroy).pack(side="left", padx=5)
    
    def editar_produccion(self, produccion):
        """Edita una producción existente"""
        # Implementación similar a agregar_produccion pero cargando datos existentes
        messagebox.showinfo("Edit Production", 
                          f"Edit functionality for '{produccion.get('titulo')}' would go here")
        # implementar esto similar a agregar_produccion pero cargando los valores existentes
    
    def eliminar_produccion(self, produccion):
        """Elimina una producción"""
        confirmar = messagebox.askyesno("Confirm Deletion", 
            f"Are you sure you want to delete production:\n\n'{produccion.get('titulo')}'?")
        
        if confirmar:
            fecha = produccion.get('fecha')
            produccion_id = produccion.get('id')
            
            if self.gestor.eliminar_produccion(fecha, produccion_id):
                messagebox.showinfo("Success", "Production deleted successfully")
                self.ver_producciones_dia()
            else:
                messagebox.showerror("Error", "Could not delete production")
    
    def marcar_completada(self, produccion):
        """Marca una producción como completada"""
        confirmar = messagebox.askyesno("Confirm Completion", 
            f"Mark production '{produccion.get('titulo')}' as completed?")
        
        if confirmar:
            fecha = produccion.get('fecha')
            produccion_id = produccion.get('id')
            nuevos_datos = {'estado': 'completada'}
            
            if self.gestor.actualizar_produccion(fecha, produccion_id, nuevos_datos):
                messagebox.showinfo("Success", "Production marked as completed")
                self.ver_producciones_dia()
            else:
                messagebox.showerror("Error", "Could not update production")
    
    def ver_producciones_mes(self):
        """Muestra producciones del mes actual"""
        fecha_actual = datetime.now()
        año = fecha_actual.year
        mes = fecha_actual.month
        
        producciones_mes = self.gestor.obtener_producciones_por_mes(año, mes)
        
        if not producciones_mes:
            messagebox.showinfo("Month Productions", 
                              f"No productions scheduled for {año}-{mes:02d}")
            return
        
        # Crear ventana con lista de producciones del mes
        dialogo = tk.Toplevel(self.window)
        dialogo.title(f"Productions for {año}-{mes:02d}")
        dialogo.geometry("800x600")
        dialogo.configure(bg="white")
        dialogo.transient(self.window)
        
        tk.Label(dialogo, text=f"📅 Productions for {año}-{mes:02d}", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        # Frame con scroll
        frame_container = tk.Frame(dialogo, bg="white")
        frame_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        canvas = tk.Canvas(frame_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
        frame_contenido = tk.Frame(canvas, bg="white")
        
        frame_contenido.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_contenido, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mostrar producciones por fecha
        total_producciones = 0
        for fecha in sorted(producciones_mes.keys()):
            tk.Label(frame_contenido, text=f"\n📅 {fecha}", 
                    font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=10)
            
            for prod in producciones_mes[fecha]:
                total_producciones += 1
                frame_prod = tk.Frame(frame_contenido, bg="#F8F9F9", relief="groove", bd=1)
                frame_prod.pack(fill="x", pady=5, padx=10)
                
                tk.Label(frame_prod, text=f"  • {prod.get('titulo')}", 
                        font=("Arial", 11), bg="#F8F9F9", anchor="w").pack(fill="x", padx=10, pady=5)
                
                tk.Label(frame_prod, 
                        text=f"    Scene: {prod.get('escena')} | Duration: {prod.get('duracion_horas')}h | Status: {prod.get('estado')}",
                        font=("Arial", 9), bg="#F8F9F9", anchor="w", fg="#5D6D7E").pack(fill="x", padx=10)
        
        tk.Label(frame_contenido, text=f"\nTotal productions: {total_producciones}", 
                font=("Arial", 11, "bold"), bg="white").pack(pady=10)
        
        tk.Button(dialogo, text="Close", 
                 command=dialogo.destroy).pack(pady=10)
    
    def ver_estadisticas_produccion(self):
        """Muestra estadísticas de producción"""
        estadisticas = self.logica.obtener_estadisticas_produccion()
        
        dialogo = tk.Toplevel(self.window)
        dialogo.title("Production Statistics")
        dialogo.geometry("500x400")
        dialogo.configure(bg="white")
        dialogo.transient(self.window)
        
        tk.Label(dialogo, text="📊 PRODUCTION STATISTICS", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        frame_stats = tk.Frame(dialogo, bg="white")
        frame_stats.pack(pady=20, padx=30, fill="both", expand=True)
        
        stats = [
            ("Total Productions", estadisticas['total_producciones'], "#3498DB"),
            ("Completed", estadisticas['completadas'], "#27AE60"),
            ("Scheduled", estadisticas['programadas'], "#F39C12"),
            ("Total Cost", f"${estadisticas['costo_total']:,.2f}", "#9B59B6"),
            ("Average Cost", f"${estadisticas['costo_promedio']:,.2f}", "#E74C3C")
        ]
        
        for i, (nombre, valor, color) in enumerate(stats):
            frame_stat = tk.Frame(frame_stats, bg="white", relief="ridge", bd=2)
            frame_stat.pack(fill="x", pady=8, padx=10)
            
            tk.Label(frame_stat, text=nombre, 
                    font=("Arial", 12), bg="white", width=20, anchor="w").pack(side="left", padx=10)
            tk.Label(frame_stat, text=str(valor), 
                    font=("Arial", 12, "bold"), bg="white", fg=color).pack(side="right", padx=10)
        
        tk.Button(dialogo, text="Close", 
                 command=dialogo.destroy).pack(pady=20)
    
    def mostrar_produccion_escenas(self):
        """Pantalla para producción de escenas"""
        self.limpiar_pantalla()
    
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=600)
    
        titulo = tk.Label(frame_principal,
        text="🎬 SCENE PRODUCTION",
        font=("Arial", 18, "bold"),
        bg="white", fg="purple")
        titulo.pack(pady=15)
    
        # Obtener escenas del backend - TUS ESCENAS EXACTAS
        escenas = self.gestor.obtener_escenas()
    
        # Frame con scroll para escenas
        frame_contenedor = tk.Frame(frame_principal, bg="white")
        frame_contenedor.pack(pady=10, padx=10, fill="both", expand=True)
    
        # Canvas para scroll
        canvas = tk.Canvas(frame_contenedor, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        frame_contenido = tk.Frame(canvas, bg="white")
    
        # Configurar scroll
        frame_contenido.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=frame_contenido, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        # Posicionar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # Lista de escenas
        tk.Label(frame_contenido, text="AVAILABLE SCENES:", 
            font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=10)
    
        for i, escena in enumerate(escenas):
            frame_escena = tk.Frame(frame_contenido, bg="#f9f7f7", relief="groove", bd=1)
            frame_escena.pack(fill="x", pady=5, padx=5)
        
            # Mostrar escena con wraplength para nombres largos
            tk.Label(frame_escena, text=f"{i+1}. {escena}",
                font=("Arial", 11), bg="#f9f7f7", anchor="w", 
                width=70, wraplength=600).pack(side="left", padx=10)
        
            # Botón para eliminar esta escena
            tk.Button(frame_escena, text="❌", 
                 font=("Arial", 8),
                 bg="#FF5252", fg="white",
                 command=lambda idx=i: self.eliminar_escena(idx)).pack(side="right")
    
        # Configurar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
        # Frame para nuevos botones
        frame_botones_superior = tk.Frame(frame_principal, bg="white")
        frame_botones_superior.pack(pady=10)
    
        tk.Button(frame_botones_superior, text="➕ Add New Scene",
             font=("Arial", 11),
             bg="#4CAF50", fg="white",
             command=self.agregar_escena).pack(side="left", padx=5)
    
        # Botones de producción INFERIORES (separados)
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
    
        tk.Button(frame_botones, text="🎬 Produce Scene",
             font=("Arial", 11),
             bg="#9C27B0", fg="white",
             command=lambda: self.producir_escena("escenas_de_principales")).pack(side="left", padx=5)
    
        tk.Button(frame_botones, text="⚠️ Produce Risk Scene",
             font=("Arial", 11),
             bg="#D32F2F", fg="white",
             command=lambda: self.producir_escena("escenas de riesgo")).pack(side="left", padx=5)
    
        tk.Button(frame_botones, text="📅 Go to Calendar",
             font=("Arial", 11),
             bg="#2E86C1", fg="white",
             command=self.mostrar_calendario_produccion).pack(side="left", padx=5)
    
        tk.Button(frame_botones, text="⬅️ Back to Menu",
             font=("Arial", 11),
             bg="#607D8B", fg="white",
             command=self.mostrar_menu_principal).pack(side="left", padx=10)
    
    def mostrar_estadisticas(self):
        """Nueva pantalla para estadísticas"""
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=900, height=500)
        
        titulo = tk.Label(frame_principal,
            text="📈 EVENT STATISTICS",
            font=("Arial", 18, "bold"),
            bg="white", fg="#FF5722")
        titulo.pack(pady=15)
        
        # Obtener datos del backend
        recursos = self.gestor.obtener_recursos()
        personal = self.gestor.obtener_personal()
        escenas = self.gestor.obtener_escenas()
        
        frame_contenido = tk.Frame(frame_principal, bg="white")
        frame_contenido.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Estadísticas
        total_recursos = sum(recursos.values())
        total_personal = sum(personal.values())
        total_escenas = len(escenas)
        
        stats = [
            ("Total Resources", total_recursos, "#4CAF50"),
            ("Total Staff", total_personal, "#2196F3"),
            ("Available Scenes", total_escenas, "#9C27B0"),
            ("Resource Types", len(recursos), "#FF9800"),
            ("Staff Positions", len(personal), "#F44336")
        ]
        
        for i, (nombre, valor, color) in enumerate(stats):
            frame_stat = tk.Frame(frame_contenido, bg="white", relief="groove", bd=2)
            frame_stat.pack(fill="x", pady=8, padx=10)
            
            tk.Label(frame_stat, text=nombre, 
                    font=("Arial", 12), bg="white", width=25, anchor="w").pack(side="left", padx=10)
            tk.Label(frame_stat, text=str(valor), 
                    font=("Arial", 14, "bold"), bg="white", fg=color).pack(side="right", padx=10)
        
        # Botones
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="🔄 Refresh Stats",
                 font=("Arial", 11),
                 bg="#FF9800", fg="white",
                 command=self.mostrar_estadisticas).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="⬅️ Back to Menu",
                 font=("Arial", 11),
                 bg="#607D8B", fg="white",
                 command=self.mostrar_menu_principal).pack(side="left", padx=10)
    
    def mostrar_configuracion(self):
        """Pantalla de configuración"""
        self.limpiar_pantalla()
        
        frame_principal = tk.Frame(self.window, bg="white", relief="raised", bd=3)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center", width=900, height=500)
        
        titulo = tk.Label(frame_principal,
            text="⚙️ SYSTEM SETTINGS",
            font=("Arial", 18, "bold"),
            bg="white", fg="brown")
        titulo.pack(pady=15)
        
        frame_contenido = tk.Frame(frame_principal, bg="white")
        frame_contenido.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Opciones de configuración
        opciones = [
            ("Interface Theme", "Configure visual theme"),
            ("System Language", "Select language"),
            ("Auto-save", "Enable/disable auto-save"),
            ("Notifications", "Configure alerts"),
            ("Automatic Backup", "Backup settings")
        ]
        
        for opcion, descripcion in opciones:
            frame_opcion = tk.Frame(frame_contenido, bg="white", relief="groove", bd=1)
            frame_opcion.pack(fill="x", pady=6, padx=10)
            
            tk.Label(frame_opcion, text=opcion,
                    font=("Arial", 12, "bold"), bg="white", width=20, anchor="w").pack(side="left", padx=10)
            tk.Label(frame_opcion, text=descripcion,
                    font=("Arial", 10), bg="white", fg="gray").pack(side="left", padx=10)
            
            tk.Button(frame_opcion, text="Configure",
                     font=("Arial", 10),
                     bg="#607D8B", fg="white").pack(side="right", padx=10)
        
        # Botones
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="💾 Save Settings",
                 font=("Arial", 11),
                 bg="#795548", fg="white",
                 command=self.guardar_configuracion).pack(side="left", padx=5)
        
        tk.Button(frame_botones, text="⬅️ Back to Menu",
                 font=("Arial", 11),
                 bg="#607D8B", fg="white",
                 command=self.mostrar_menu_principal).pack(side="left", padx=10)
    
    # ========== FUNCIONES PARA MANEJO DE DATOS ==========
    
    def agregar_recurso(self):
        """Función para agregar recurso"""
        from tkinter import simpledialog
        nuevo_recurso = simpledialog.askstring("Add Resource", "Resource name:")
        if not nuevo_recurso:
            return
            
        cantidad_recurso = simpledialog.askinteger("Add Quantity", "Quantity:")
        if cantidad_recurso is None:
            return
        
        if self.gestor.agregar_recurso(nuevo_recurso, cantidad_recurso):
            messagebox.showinfo("Success", f"Resource '{nuevo_recurso}' added with {cantidad_recurso} units")
            self.mostrar_gestion_recursos()
        else:
            messagebox.showerror("Error", "Could not add resource")
    
    def eliminar_recurso(self):
        """Función para eliminar recurso"""
        from tkinter import simpledialog
        
        recursos = self.gestor.obtener_recursos()
        if not recursos:
            messagebox.showwarning("Warning", "No resources available")
            return
        
        recurso_a_eliminar = simpledialog.askstring("Remove Resource", 
            "Resource name to remove:")
        
        if recurso_a_eliminar:
            if recurso_a_eliminar in recursos:
                confirmar = messagebox.askyesno("Confirm", 
                    f"Are you sure you want to remove '{recurso_a_eliminar}'?")
                
                if confirmar and self.gestor.eliminar_recurso(recurso_a_eliminar):
                    messagebox.showinfo("Success", f"Resource '{recurso_a_eliminar}' removed")
                    self.mostrar_gestion_recursos()
            else:
                messagebox.showerror("Error", f"Resource '{recurso_a_eliminar}' not found")
    
    def agregar_personal(self):
        """Función para agregar personal"""
        from tkinter import simpledialog
        nuevo_puesto = simpledialog.askstring("Hire Staff", "Position name:")
        if not nuevo_puesto:
            return
            
        cantidad_personal = simpledialog.askinteger("Add Staff", "Number of people:")
        if cantidad_personal is None:
            return
        
        if self.gestor.agregar_personal(nuevo_puesto, cantidad_personal):
            messagebox.showinfo("Success", f"Position '{nuevo_puesto}' added with {cantidad_personal} people")
            self.mostrar_gestion_personal()
        else:
            messagebox.showerror("Error", "Could not add staff")
    
    def eliminar_personal(self):
        """Función para eliminar personal"""
        from tkinter import simpledialog
        
        personal = self.gestor.obtener_personal()
        if not personal:
            messagebox.showwarning("Warning", "No staff available")
            return
        
        puesto_a_eliminar = simpledialog.askstring("Dismiss Staff", 
            "Position to remove:")
        
        if puesto_a_eliminar:
            if puesto_a_eliminar in personal:
                confirmar = messagebox.askyesno("Confirm", 
                    f"Are you sure you want to dismiss '{puesto_a_eliminar}'?")
                
                if confirmar and self.gestor.eliminar_personal(puesto_a_eliminar):
                    messagebox.showinfo("Success", f"Position '{puesto_a_eliminar}' removed")
                    self.mostrar_gestion_personal()
            else:
                messagebox.showerror("Error", f"Position '{puesto_a_eliminar}' not found")
    
    def agregar_escena(self):
        """Función para agregar escenas"""
        from tkinter import simpledialog
        nueva_escena = simpledialog.askstring("Add Scene", "Scene description:")
        
        if nueva_escena:
            if self.gestor.agregar_escena(nueva_escena):
                messagebox.showinfo("Success", f"Scene '{nueva_escena}' added")
                self.mostrar_produccion_escenas()
            else:
                messagebox.showerror("Error", "Could not add scene")
    
    def eliminar_escena(self, indice):
        """Función para eliminar escena por índice"""
        escenas = self.gestor.obtener_escenas()
        if 0 <= indice < len(escenas):
            escena = escenas[indice]
            confirmar = messagebox.askyesno("Confirm", 
                f"Are you sure you want to remove scene: '{escena}'?")
            
            if confirmar and self.gestor.eliminar_escena(indice):
                messagebox.showinfo("Success", "Scene removed")
                self.mostrar_produccion_escenas()
    
    def producir_escena(self, tipo):
        """Función para producir escena"""
        resultado = self.logica.producir_escena(tipo)
        messagebox.showinfo("Production", resultado)
    
    def ver_en_calendario(self, produccion):
        """Abre el calendario y marca la fecha de la producción"""
        self.mostrar_calendario_produccion()
        
        # Marcar la fecha en el calendario
        fecha = produccion.get('fecha')
        if fecha:
            try:
                año, mes, dia = map(int, fecha.split('-'))
                self.calendar.selection_set(datetime(año, mes, dia))
                self.ver_producciones_dia()
            except:
                pass

    def eliminar_produccion_desde_calendario(self, produccion):
        """Elimina una producción desde la vista del calendario"""
        confirmar = messagebox.askyesno("Confirm Deletion", 
            f"⚠️ ARE YOU SURE YOU WANT TO DELETE THIS PRODUCTION?\n\n"
            f"📅 Date: {produccion.get('fecha')}\n"
            f"🎬 Title: {produccion.get('titulo')}\n"
            f"🎭 Scene: {produccion.get('escena')}\n\n"
            f"This action will RESTORE all used resources and staff.")
        
        if confirmar:
            fecha = produccion.get('fecha')
            produccion_id = produccion.get('id')
            
            if self.gestor.eliminar_produccion(fecha, produccion_id):
                messagebox.showinfo("Success", 
                    f"✅ Production deleted successfully!\n\n"
                    f"Resources and staff have been restored to inventory.")
                
                # Actualizar vista
                self.ver_producciones_dia()
                
                # Cerrar diálogo de detalles
                for widget in self.window.winfo_children():
                    if isinstance(widget, tk.Toplevel):
                        if "Production Details" in widget.title():
                            widget.destroy()
            else:
                messagebox.showerror("Error", "Could not delete production")

    def ir_a_hoy(self):
        """Va al día actual en el calendario"""
        hoy = datetime.now()
        self.calendar.selection_set(hoy)
        self.ver_producciones_dia()
    
    def guardar_configuracion(self):
        """Guarda la configuración"""
        self.gestor.guardar_todo()
        messagebox.showinfo("Settings", "All settings saved successfully")
    
    def guardado_automatico(self):
        """Guarda automáticamente cada 5 minutos"""
        try:
            self.gestor.guardar_todo()
            print("Auto-save completed")
        except Exception as e:
            print(f"Auto-save error: {e}")
        
        # Programar próximo guardado en 5 minutos (300,000 ms)
        self.window.after(300000, self.guardado_automatico)
    
    def toggle_fullscreen(self, event=None):
        """Alterna entre pantalla completa y ventana normal con la tecla 9"""
        self.window.attributes('-fullscreen', not self.window.attributes('-fullscreen'))
        return "break"
    
    def exit_fullscreen(self, event=None):
        """Sale del modo pantalla completa con la tecla ESC"""
        self.window.attributes('-fullscreen', False)
        return "break"
    
    def cerrar_aplicacion(self):
        """Guarda todos los datos antes de cerrar"""
        self.gestor.guardar_todo()
        self.window.quit()
    
    def ejecutar(self):
        """Inicia la aplicación"""
        self.window.mainloop()
