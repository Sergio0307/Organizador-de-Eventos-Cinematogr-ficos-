# backend.py - VERSIÓN CON TUS DATOS EXACTOS
import json
import os
from datetime import datetime

class GestorDatos:
    def __init__(self):
        # NOMBRES EXACTOS DE TUS ARCHIVOS JSON
        self.archivos = {
            'recursos': "recursos.json",  # Tu archivo exacto
            'personal': "personal.json",  # Tu archivo exacto
            'escenas': "escenas.json",  # Tu archivo exacto (pero ojo: el tuyo es diccionario, no lista)
            'config': "configuracion.json",
            'producciones': "producciones.json"  # Nuevo archivo para calendario
        }
        self.cargar_configuracion()
        self.cargar_datos()

    def cargar_configuracion(self):
        """Carga o crea configuración del sistema"""
        if os.path.exists(self.archivos['config']):
            with open(self.archivos['config'], 'r', encoding='utf-8') as f:
                self.configuracion = json.load(f)
        else:
            self.configuracion = {
                "auto_save": True,
                "auto_save_interval": 300,
                "last_backup": None,
                "theme": "light",
                "language": "en"
            }
            self.guardar_configuracion()

    def cargar_datos(self):
        """Carga los datos desde los archivos JSON EXACTAMENTE como los tienes"""
        self.datos = {}
        
        # 1. CARGAR RECURSOS - TUS DATOS EXACTOS
        if os.path.exists(self.archivos['recursos']):
            with open(self.archivos['recursos'], 'r', encoding='utf-8') as f:
                self.datos['recursos'] = json.load(f)
        else:
            # TUS RECURSOS EXACTOS
            self.datos['recursos'] = {
                "camara": 6,
                "equipo implementador de vestimenta": 2,
                "silla del director": 2,
                "claqueta": 2,
                "altavoces": 3,
                "luces": 4,
                "autos": 2,
                "armas blancas falsas": 2,
                "equipo de proteccion": 3,
                "equipo de pirotecnia": 2
            }
            self.guardar_recursos()
        
        # 2. CARGAR PERSONAL - TUS DATOS EXACTOS
        if os.path.exists(self.archivos['personal']):
            with open(self.archivos['personal'], 'r', encoding='utf-8') as f:
                self.datos['personal'] = json.load(f)
        else:
            # TU PERSONAL EXACTO
            self.datos['personal'] = {
                "actor_principal_1": 1,
                "actor_principal_2": 1,
                "secundarios": 4,
                "doblaje": 1,
                "de riesgo": 2,
                "director_de_escena": 1,
                "vicedirector de escenas": 1,
                "personal de inicio de escenas": 2,
                "profesional de camaras": 4,
                "sujetador de claqueta": 2,
                "profesional de edicion": 1,
                "profesional de iluminacion": 2,
                "profesional en conduccion": 2
            }
            self.guardar_personal()
        
        # 3. CARGAR ESCENAS - OJO: EL TUYO ES DICCIONARIO, NO LISTA
        if os.path.exists(self.archivos['escenas']):
            with open(self.archivos['escenas'], 'r', encoding='utf-8') as f:
                escenas_data = json.load(f)
                # Convertir diccionario a lista si es necesario
                if isinstance(escenas_data, dict):
                    self.datos['escenas'] = list(escenas_data.keys())
                else:
                    self.datos['escenas'] = escenas_data
        else:
            # ESCENAS EXACTAS 
            self.datos['escenas'] = [
                "sala de maquillaje",
                "escenas_de_principales",
                "escenas de riesgo",
                "escenas_secundarias",
                "camerino",
                "camerino de actores principales",
                "salon de edicion"
            ]
            self.guardar_escenas()
        
        # 4. CARGAR PRODUCCIONES (nuevo para calendario)
        if os.path.exists(self.archivos['producciones']):
            with open(self.archivos['producciones'], 'r', encoding='utf-8') as f:
                self.datos['producciones'] = json.load(f)
        else:
            self.datos['producciones'] = {}
            self.guardar_producciones()
        
        return self.datos

    # ========== MÉTODOS PARA OBTENER DATOS ==========
    def obtener_recursos(self):
        return self.datos['recursos']
    
    def obtener_personal(self):
        return self.datos['personal']
    
    def obtener_escenas(self):
        return self.datos['escenas']
    
    def obtener_configuracion(self):
        return self.configuracion
    
    def obtener_producciones(self):
        return self.datos['producciones']
    
    # ========== MÉTODOS PARA AGREGAR ==========
    def agregar_recurso(self, nombre, cantidad):
        """Agrega un recurso - SI EXISTE SUMA, SI NO CREA NUEVO"""
        if nombre in self.datos['recursos']:
            # Si ya existe, SUMAR la cantidad
            self.datos['recursos'][nombre] += cantidad
        else:
            # Si no existe, crear nuevo
            self.datos['recursos'][nombre] = cantidad
        self.guardar_recursos()
        return True

    def agregar_personal(self, puesto, cantidad):
        """Agrega personal - SI EXISTE SUMA, SI NO CREA NUEVO"""
        if puesto in self.datos['personal']:
            # Si ya existe, SUMAR la cantidad
            self.datos['personal'][puesto] += cantidad
        else:
            # Si no existe, crear nuevo
            self.datos['personal'][puesto] = cantidad
        self.guardar_personal()
        return True

    def agregar_escena(self, descripcion):
        """Agrega una escena"""
        if descripcion not in self.datos['escenas']:
            self.datos['escenas'].append(descripcion)
            self.guardar_escenas()
            return True
        return False

    # NUEVO: Agregar producción programada
    
    def agregar_produccion(self, fecha, produccion_data):
        """
        Agrega una producción programada y descuenta recursos/personal
        """
        if fecha not in self.datos['producciones']:
            self.datos['producciones'][fecha] = []
        
        # Asignar ID único
        produccion_id = f"prod_{len(self.datos['producciones'][fecha]) + 1:03d}"
        produccion_data['id'] = produccion_id
        produccion_data['fecha'] = fecha
        produccion_data['estado'] = 'programada'
        
        # Descontar recursos utilizados
        recursos_utilizados = produccion_data.get('recursos_utilizados', {})
        for recurso, cantidad in recursos_utilizados.items():
            if recurso in self.datos['recursos']:
                self.datos['recursos'][recurso] -= cantidad
                if self.datos['recursos'][recurso] < 0:
                    self.datos['recursos'][recurso] = 0
        
        # Descontar personal asignado
        personal_asignado = produccion_data.get('personal_asignado', {})
        for puesto, cantidad in personal_asignado.items():
            if puesto in self.datos['personal']:
                self.datos['personal'][puesto] -= cantidad
                if self.datos['personal'][puesto] < 0:
                    self.datos['personal'][puesto] = 0
        
        self.datos['producciones'][fecha].append(produccion_data)
        
        # Guardar cambios
        self.guardar_recursos()
        self.guardar_personal()
        self.guardar_producciones()
        
        return produccion_id
    
    # ========== MÉTODOS PARA ELIMINAR ==========
    def eliminar_recurso(self, nombre):
        if nombre in self.datos['recursos']:
            del self.datos['recursos'][nombre]
            self.guardar_recursos()
            return True
        return False

    def eliminar_personal(self, puesto):
        if puesto in self.datos['personal']:
            del self.datos['personal'][puesto]
            self.guardar_personal()
            return True
        return False

    def eliminar_escena(self, indice):
        if 0 <= indice < len(self.datos['escenas']):
            del self.datos['escenas'][indice]
            self.guardar_escenas()
            return True
        return False

    # NUEVO: Eliminar producción
    
    def eliminar_produccion(self, fecha, produccion_id):
        """Elimina una producción y restaura recursos/personal"""
        if fecha in self.datos['producciones']:
            for i, prod in enumerate(self.datos['producciones'][fecha]):
                if prod.get('id') == produccion_id:
                    # Restaurar recursos
                    recursos_utilizados = prod.get('recursos_utilizados', {})
                    for recurso, cantidad in recursos_utilizados.items():
                        if recurso in self.datos['recursos']:
                            self.datos['recursos'][recurso] += cantidad
                    
                    # Restaurar personal
                    personal_asignado = prod.get('personal_asignado', {})
                    for puesto, cantidad in personal_asignado.items():
                        if puesto in self.datos['personal']:
                            self.datos['personal'][puesto] += cantidad
                    
                    # Eliminar producción
                    del self.datos['producciones'][fecha][i]
                    
                    if not self.datos['producciones'][fecha]:
                        del self.datos['producciones'][fecha]
                    
                    # Guardar cambios
                    self.guardar_recursos()
                    self.guardar_personal()
                    self.guardar_producciones()
                    
                    return True
        return False
    
    # ========== MÉTODOS PARA ACTUALIZAR ==========
    def actualizar_recurso(self, nombre, nueva_cantidad):
        if nombre in self.datos['recursos']:
            self.datos['recursos'][nombre] = nueva_cantidad
            self.guardar_recursos()
            return True
        return False

    # NUEVO: Actualizar producción
    
    def actualizar_produccion(self, fecha, produccion_id, nuevos_datos):
        """Actualiza una producción existente"""
        if fecha in self.datos['producciones']:
            for i, prod in enumerate(self.datos['producciones'][fecha]):
                if prod.get('id') == produccion_id:
                    # Aquí podrías implementar lógica para actualizar recursos
                    # Por ahora solo actualiza los datos
                    self.datos['producciones'][fecha][i].update(nuevos_datos)
                    self.guardar_producciones()
                    return True
        return False

    def verificar_disponibilidad_real_time(self, recursos_necesarios, personal_necesario):
        """Verifica disponibilidad considerando producciones programadas"""
        disponibles = {
            'recursos': {},
            'personal': {},
            'total_recursos_disponibles': self.datos['recursos'].copy(),
            'total_personal_disponible': self.datos['personal'].copy()
        }
        
        # Descontar recursos de todas las producciones programadas
        for fecha, prods in self.datos['producciones'].items():
            for prod in prods:
                if prod.get('estado') != 'cancelada':
                    # Descontar recursos
                    for recurso, cantidad in prod.get('recursos_utilizados', {}).items():
                        if recurso in disponibles['total_recursos_disponibles']:
                            disponibles['total_recursos_disponibles'][recurso] -= cantidad
                    
                    # Descontar personal
                    for puesto, cantidad in prod.get('personal_asignado', {}).items():
                        if puesto in disponibles['total_personal_disponible']:
                            disponibles['total_personal_disponible'][puesto] -= cantidad
        
        # Verificar disponibilidad para los nuevos recursos solicitados
        conflictos = []
        
        for recurso, cantidad_necesaria in recursos_necesarios.items():
            disponible = disponibles['total_recursos_disponibles'].get(recurso, 0)
            if disponible < cantidad_necesaria:
                conflictos.append(f"Recurso '{recurso}': {disponible} disponibles, {cantidad_necesaria} necesarios")
            else:
                disponibles['recursos'][recurso] = disponible - cantidad_necesaria
        
        for puesto, cantidad_necesaria in personal_necesario.items():
            disponible = disponibles['total_personal_disponible'].get(puesto, 0)
            if disponible < cantidad_necesaria:
                conflictos.append(f"Personal '{puesto}': {disponible} disponibles, {cantidad_necesaria} necesarios")
            else:
                disponibles['personal'][puesto] = disponible - cantidad_necesaria
        
        return conflictos, disponibles
    
    # ========== MÉTODOS PARA OBTENER ESPECÍFICOS ==========
    # NUEVO: Obtener producciones por fecha
    def obtener_producciones_por_fecha(self, fecha):
        """Obtiene todas las producciones de una fecha específica"""
        return self.datos['producciones'].get(fecha, [])

    # NUEVO: Obtener producciones por mes
    def obtener_producciones_por_mes(self, año, mes):
        """Obtiene todas las producciones de un mes específico"""
        producciones_mes = {}
        for fecha, prods in self.datos['producciones'].items():
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                if fecha_obj.year == año and fecha_obj.month == mes:
                    producciones_mes[fecha] = prods
            except:
                continue
        return producciones_mes

    # ========== MÉTODOS PARA GUARDAR ==========
    def guardar_recursos(self):
        try:
            with open(self.archivos['recursos'], 'w', encoding='utf-8') as f:
                json.dump(self.datos['recursos'], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving resources: {e}")
            return False

    def guardar_personal(self):
        try:
            with open(self.archivos['personal'], 'w', encoding='utf-8') as f:
                json.dump(self.datos['personal'], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving staff: {e}")
            return False

    def guardar_escenas(self):
        try:
            # Guardar como lista (para consistencia con el sistema)
            with open(self.archivos['escenas'], 'w', encoding='utf-8') as f:
                json.dump(self.datos['escenas'], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving scenes: {e}")
            return False

    # NUEVO: Guardar producciones
    def guardar_producciones(self):
        try:
            with open(self.archivos['producciones'], 'w', encoding='utf-8') as f:
                json.dump(self.datos['producciones'], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving productions: {e}")
            return False

    def guardar_configuracion(self):
        try:
            with open(self.archivos['config'], 'w', encoding='utf-8') as f:
                json.dump(self.configuracion, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False

    def guardar_todo(self):
        success = True
        success = self.guardar_recursos() and success
        success = self.guardar_personal() and success
        success = self.guardar_escenas() and success
        success = self.guardar_producciones() and success
        success = self.guardar_configuracion() and success
        
        if success:
            self.configuracion['last_backup'] = datetime.now().isoformat()
            self.guardar_configuracion()
            print("All data saved successfully")
        else:
            print("Some data could not be saved")
        
        return success


class LogicaNegocio:
    def __init__(self, gestor_datos):
        self.gestor = gestor_datos
        
        # PRECIOS para TUS RECURSOS EXACTOS
        self.precios_recursos = {
            "camara": 5000,
            "equipo implementador de vestimenta": 1500,
            "silla del director": 300,
            "claqueta": 200,
            "altavoces": 800,
            "luces": 1200,
            "autos": 20000,
            "armas blancas falsas": 500,
            "equipo de proteccion": 1000,
            "equipo de pirotecnia": 2500
        }
        
        # SALARIOS para TU PERSONAL EXACTO
        self.salarios_personal = {
            "actor_principal_1": 10000,
            "actor_principal_2": 9000,
            "secundarios": 3000,
            "doblaje": 4000,
            "de riesgo": 6000,
            "director_de_escena": 12000,
            "vicedirector de escenas": 8000,
            "personal de inicio de escenas": 2500,
            "profesional de camaras": 5000,
            "sujetador de claqueta": 2000,
            "profesional de edicion": 4500,
            "profesional de iluminacion": 4000,
            "profesional en conduccion": 3500
        }
    
    def producir_escena(self, tipo_escena):
        """Produce una escena específica"""
        recursos_necesarios = self.sugerir_recursos_para_escena(tipo_escena)
        
        if not recursos_necesarios:
            return f"No se pudo determinar los recursos para la escena: {tipo_escena}"
        
        # Verificar disponibilidad de recursos
        recursos_disponibles = self.gestor.obtener_recursos()
        recursos_faltantes = []
        
        for recurso in recursos_necesarios:
            if recurso not in recursos_disponibles or recursos_disponibles[recurso] <= 0:
                recursos_faltantes.append(recurso)
        
        if recursos_faltantes:
            return f"Faltan recursos para producir la escena '{tipo_escena}': {', '.join(recursos_faltantes)}"
        
        # Calcular costo estimado
        costo_estimado = self.calcular_costo_evento()
        
        return f"✅ Escena '{tipo_escena}' producida exitosamente!\n\nRecursos utilizados: {', '.join(recursos_necesarios)}\nCosto estimado: ${costo_estimado:,.2f}"
    
    def calcular_costo_evento(self, duracion_horas=8):
        """Calcula el costo estimado de un evento"""
        costo_total = 0
        
        # Costo de recursos
        recursos = self.gestor.obtener_recursos()
        for recurso, cantidad in recursos.items():
            precio_unitario = self.precios_recursos.get(recurso, 100)
            costo_total += (cantidad * 0.5 * precio_unitario) * (duracion_horas / 24)
        
        # Costo de personal
        personal = self.gestor.obtener_personal()
        for puesto, cantidad in personal.items():
            salario_mensual = self.salarios_personal.get(puesto, 3000)
            salario_diario = salario_mensual / 20  # 20 días laborales
            costo_total += cantidad * salario_diario
        
        return round(costo_total, 2)
    
    def verificar_disponibilidad(self, recurso, cantidad_necesaria):
        """Verifica si hay suficientes recursos"""
        recursos = self.gestor.obtener_recursos()
        if recurso in recursos:
            return recursos[recurso] >= cantidad_necesaria
        return False
    
    # NUEVO: Calcular costo de producción
    def calcular_costo_produccion(self, produccion_data):
        """Calcula el costo de una producción específica"""
        costo_total = 0
        
        # Costo de recursos utilizados
        if 'recursos_utilizados' in produccion_data:
            for recurso, cantidad in produccion_data['recursos_utilizados'].items():
                precio = self.precios_recursos.get(recurso, 100)
                costo_total += precio * cantidad
        
        # Costo de personal asignado
        if 'personal_asignado' in produccion_data:
            for puesto, cantidad in produccion_data['personal_asignado'].items():
                salario = self.salarios_personal.get(puesto, 3000)
                costo_diario = salario / 20  # 20 días laborales al mes
                duracion = produccion_data.get('duracion_horas', 8) / 8  # Convertir a días
                costo_total += cantidad * costo_diario * duracion
        
        # Costo adicional de escena
        costo_total += produccion_data.get('costo_adicional', 0)
        
        return round(costo_total, 2)
    
    # NUEVO: Verificar conflictos de recursos
    
    # En backend.py, en la clase LogicaNegocio:
    
    def verificar_conflictos_recursos(self, fecha, recursos_necesarios, personal_necesario=None):
        """Verifica conflictos de recursos Y personal"""
        conflictos = []
        
        # Verificar recursos
        recursos_totales = self.gestor.obtener_recursos()
        for recurso, cantidad_necesaria in recursos_necesarios.items():
            disponible_total = recursos_totales.get(recurso, 0)
            if disponible_total < cantidad_necesaria:
                conflictos.append(f"Resource '{recurso}': {disponible_total} available, {cantidad_necesaria} needed")
        
        # Verificar personal
        if personal_necesario:
            personal_total = self.gestor.obtener_personal()
            for puesto, cantidad_necesaria in personal_necesario.items():
                disponible_total = personal_total.get(puesto, 0)
                if disponible_total < cantidad_necesaria:
                    conflictos.append(f"Staff '{puesto}': {disponible_total} available, {cantidad_necesaria} needed")
        
        return conflictos
    
    # NUEVO: Verificar disponibilidad de personal
    def verificar_disponibilidad_personal(self, fecha, personal_necesario):
        """Verifica si hay suficiente personal disponible"""
        personal_total = self.gestor.obtener_personal()
        
        conflictos = []
        for puesto, cantidad_necesaria in personal_necesario.items():
            disponible_total = personal_total.get(puesto, 0)
            if disponible_total < cantidad_necesaria:
                conflictos.append(f"{puesto}: {disponible_total} disponibles, {cantidad_necesaria} necesarios")
        
        return conflictos
    
    # NUEVO: Obtener estadísticas de producción
    def obtener_estadisticas_produccion(self, año=None, mes=None):
        """Obtiene estadísticas de producción"""
        if año and mes:
            producciones = self.gestor.obtener_producciones_por_mes(año, mes)
        else:
            producciones = self.gestor.obtener_producciones()
        
        total_producciones = 0
        producciones_completadas = 0
        producciones_programadas = 0
        costo_total = 0
        
        for fecha, prods in producciones.items():
            total_producciones += len(prods)
            for prod in prods:
                if prod.get('estado') == 'completada':
                    producciones_completadas += 1
                elif prod.get('estado') == 'programada':
                    producciones_programadas += 1
                
                costo_total += self.calcular_costo_produccion(prod)
        
        return {
            "total_producciones": total_producciones,
            "completadas": producciones_completadas,
            "programadas": producciones_programadas,
            "costo_total": round(costo_total, 2),
            "costo_promedio": round(costo_total / max(total_producciones, 1), 2)
        }
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas detalladas"""
        recursos = self.gestor.obtener_recursos()
        personal = self.gestor.obtener_personal()
        escenas = self.gestor.obtener_escenas()
        
        return {
            "total_recursos": sum(recursos.values()),
            "total_personal": sum(personal.values()),
            "total_escenas": len(escenas),
            "tipos_recursos": len(recursos),
            "tipos_personal": len(personal),
            "costo_evento_promedio": self.calcular_costo_evento()
        }
    
    def sugerir_recursos_para_escena(self, tipo_escena):
        """Sugiere recursos según el tipo de escena"""
        sugerencias = {
            "sala de maquillaje": ["luces", "silla del director"],
            "escenas_de_principales": ["camara", "luces", "claqueta"],
            "escenas de riesgo": ["equipo de proteccion", "profesional en conduccion"],
            "escenas_secundarias": ["camara", "altavoces"],  # CORREGIDO: sin espacio
            "camerino": ["silla del director", "equipo implementador de vestimenta"],
            "camerino de actores principales": ["equipo implementador de vestimenta", "silla del director"],
            "salon de edicion": ["camara", "profesional de edicion"]
        }
        
        return sugerencias.get(tipo_escena, [])