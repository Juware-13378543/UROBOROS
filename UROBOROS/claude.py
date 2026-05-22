import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import random
import os
from datetime import date, timedelta

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("dark-blue")


class DragoSystemApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("UROBOROS - Panel de Control Interactivo")
        self.geometry("1250x700")
        self.minsize(1000, 650)

        self.colors = {
            "primario":        "#5A0814",
            "hover":           "#730C1B",
            "acento":          "#87129E",
            "fondo_principal": "#FFFFFF",
            "fondo_entorno":   "#F4F5F7",
            "texto_principal": "#2B2D42",
            "texto_secundario":"#7A7D85",
            "seleccion":       "#40050E",
        }
        self.configure(fg_color=self.colors["fondo_entorno"])

        # ── Datos ──────────────────────────────────────────────────────────────
        self.db_postulaciones = []
        self.empresas  = ["Google", "Microsoft", "Oracle", "Amd"]
        self.carreras  = ["Ingeniería de Sistemas", "Diseño Visual",
                        "Ingeniería Industrial", "Administración"]

        self.tipos_validacion = [
            "Técnico", "Profesional", "Practicante", "Tecnólogo", "Auxiliar"
        ]

        self.estados_validos = ["Pendiente", "En Entrevista", "Revisado"]

        self.contador_ids = 1

        # Rutas estáticas de logos por empresa (sin interacción del usuario)
        self.logos_estaticos_empresas = {
            "Google":    os.path.join("assets", "google.png"),
            "Microsoft": os.path.join("assets", "microsoft.png"),
            "Oracle":    os.path.join("assets", "oracle.png"),
            "Amd":       os.path.join("assets", "amd.png"),
        }

        # Requisitos fijos por área — compartidos entre show_empresas y show_requisitos
        self.requisitos_area = {
            "Ingeniería de Sistemas": [
                "Lógica algorítmica y estructuras de datos.",
                "Programación en Python, Java o C++.",
                "Bases de datos SQL y NoSQL.",
                "Arquitectura de software y metodologías ágiles.",
            ],
            "Diseño Visual": [
                "Suite Adobe (Illustrator, Photoshop).",
                "Prototipado UI/UX con Figma.",
                "Teoría del color y tipografía.",
                "Creación de identidades de marca.",
            ],
            "Ingeniería Industrial": [
                "Optimización de procesos de producción.",
                "Logística y cadena de suministro.",
                "Gestión financiera y evaluación de proyectos.",
                "Lean Manufacturing y Six Sigma.",
            ],
            "Administración": [
                "Liderazgo estratégico y resolución de conflictos.",
                "Gestión integral de Recursos Humanos.",
                "Planificación de finanzas corporativas.",
                "Normativas empresariales y comerciales.",
            ],
        }

        self.lbl_ofertas       = None
        self.lbl_postulaciones = None
        self.lbl_tasa          = None
        self.foto_temporal     = None
        self._img_drago        = None

        self.generar_datos_simulados()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.setup_styles()
        self.build_sidebar()
        self.build_main_container()
        self.show_inicio()

        # ── Pantalla de inicio (Login) — se superpone al final del __init__ ──
        self.show_login_screen()

    # ── Pantalla de Login ─────────────────────────────────────────────────────

    def show_login_screen(self):
        """Capa roja de bloqueo que cubre toda la ventana al arrancar."""
        self.login_frame = ctk.CTkFrame(self, fg_color=self.colors["primario"],
                                        corner_radius=0)
        self.login_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.login_frame.lift()

        # Contenedor centrado vertical y horizontalmente
        center = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Logotipo escalado
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            try:
                logo_raw = Image.open(logo_path)
                logo_img = ctk.CTkImage(light_image=logo_raw, size=(110, 110))
                lbl_logo = ctk.CTkLabel(center, image=logo_img, text="",
                                        fg_color="transparent")
                lbl_logo._img_ref = logo_img          # evitar recolección de basura
                lbl_logo.pack(pady=(0, 24))
            except Exception:
                ctk.CTkLabel(center, text="🐉", font=("Segoe UI", 72),
                             text_color="white").pack(pady=(0, 24))
        else:
            ctk.CTkLabel(center, text="🐉", font=("Segoe UI", 72),
                         text_color="white").pack(pady=(0, 24))

        # Título principal
        ctk.CTkLabel(center, text="UROBOROS",
                     font=("Segoe UI", 52, "bold"),
                     text_color="white").pack(pady=(0, 48))

        # Botón Iniciar Sesión
        ctk.CTkButton(center, text="Iniciar Sesión",
                      fg_color="white",
                      text_color=self.colors["primario"],
                      hover_color="#F0F0F0",
                      font=("Segoe UI", 16, "bold"),
                      width=220, height=54,
                      corner_radius=10,
                      command=self.login_frame.destroy).pack()

    # ── Lógica de datos ───────────────────────────────────────────────────────

    def generar_fecha_2026(self):
        start = date(2026, 1, 1)
        end   = date(2026, 12, 31)
        return start + timedelta(days=random.randrange((end - start).days))

    def generar_habilidades(self, carrera):
        mapa = {
            "Ingeniería de Sistemas":  ["Python", "SQL", "Docker", "Machine Learning",
                                        "Arquitectura de Software", "C++"],
            "Diseño Visual":           ["UI/UX", "Minimalismo", "Branding", "Adobe Suite",
                                        "Figma", "Teoría del Color"],
            "Ingeniería Industrial":   ["Optimización de procesos", "Logística",
                                        "Gestión Financiera", "Lean Manufacturing", "Six Sigma"],
            "Administración":          ["Liderazgo Estratégico", "Finanzas Corporativas",
                                        "Recursos Humanos", "Gestión de Proyectos"],
        }
        skills = random.sample(mapa.get(carrera, mapa["Administración"]), 3)
        skills.append(f"{random.randint(0, 3)} años de exp. empresarial")
        return " | ".join(skills)

    def generar_datos_simulados(self):
        nombres = ["Julian Bejarano", "Ana Maria Silva", "Carlos Mendoza"]
        estados = ["Revisado", "En Entrevista", "Pendiente"]
        for i in range(3):
            carrera = self.carreras[i % len(self.carreras)]
            self.db_postulaciones.append({
                "id":         f"{self.contador_ids:03d}",
                "nombre":     nombres[i],
                "programa":   carrera,
                "estado":     estados[i],
                "empresa":    random.choice(self.empresas),
                "fecha":      self.generar_fecha_2026().strftime("%d/%m/%Y"),
                "habilidades":self.generar_habilidades(carrera),
                "validacion": random.choice(self.tipos_validacion),
                "foto":       None,
            })
            self.contador_ids += 1

    # ── Estilos ───────────────────────────────────────────────────────────────

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=self.colors["fondo_principal"],
                        foreground=self.colors["texto_principal"],
                        rowheight=40, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Custom.Treeview.Heading",
                        background=self.colors["fondo_principal"],
                        foreground=self.colors["texto_principal"],
                        font=("Segoe UI", 10, "bold"), borderwidth=0, relief="flat")
        style.map("Custom.Treeview",
                background=[('selected', self.colors["seleccion"])],
                foreground=[('selected', 'white')])

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=self.colors["primario"],
                                    corner_radius=0, width=240)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Identidad unificada: compound="left" con logo al costado del título
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            logo_image = ctk.CTkImage(Image.open(logo_path), size=(25, 25))
            ctk.CTkLabel(self.sidebar, text=" UROBOROS", image=logo_image,
                        compound="left", font=("Segoe UI", 18, "bold"),
                        text_color="white").pack(pady=(30, 40), padx=20, anchor="w")
        else:
            ctk.CTkLabel(self.sidebar, text="UROBOROS",
                        font=("Segoe UI", 18, "bold"),
                        text_color="white").pack(pady=(30, 40), padx=20, anchor="w")

        for menu in ["Inicio / Resumen", "Empresas Disponibles", "Requisitos por Área"]:
            ctk.CTkButton(self.sidebar, text=f"  {menu}",
                        fg_color="transparent", text_color="white",
                        hover_color=self.colors["hover"], corner_radius=0,
                        anchor="w", font=("Segoe UI", 12),
                        command=lambda m=menu: self.navigate(m)).pack(fill="x", pady=2, ipady=8)

        # Mascota
        frame_mascota = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_mascota.pack(side="bottom", fill="x", pady=(0, 10), padx=15)

        ruta_drago = os.path.join("assets", "drago.png")
        if os.path.exists(ruta_drago):
            try:
                img_raw = Image.open(ruta_drago)
                self._img_drago = ctk.CTkImage(light_image=img_raw, size=(125, 125))
                ctk.CTkLabel(frame_mascota, image=self._img_drago, text="",
                            fg_color="transparent").pack(anchor="w")
            except Exception:
                ctk.CTkLabel(frame_mascota, text="🐉", font=("Segoe UI", 40),
                            text_color="white").pack(anchor="w")
        else:
            ctk.CTkLabel(frame_mascota, text="🐉", font=("Segoe UI", 40),
                        text_color="white").pack(anchor="w")
            ctk.CTkLabel(frame_mascota, text="Pon drago.png\nen assets/",
                        font=("Segoe UI", 9),
                        text_color="#E0B6BB").pack(anchor="w")

        ctk.CTkLabel(frame_mascota, text="v2.1 UROBOROS.System",
                    font=("Segoe UI", 11),
                    text_color="#E0B6BB").pack(anchor="w", pady=(4, 0))

    # ── Contenedor principal ──────────────────────────────────────────────────

    def build_main_container(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(self.main_container, text="Panel de Control",
                                        font=("Segoe UI", 24, "bold"),
                                        text_color=self.colors["texto_principal"])
        self.header_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

    def navigate(self, menu_name):
        tabla = {
            "Inicio":     ("Resumen de Postulaciones",       self.show_inicio),
            "Empresas":   ("Directorio de Empresas (2026)",  self.show_empresas),
            "Requisitos": ("Requisitos por Área Académica",  self.show_requisitos),
        }
        for key, (titulo, fn) in tabla.items():
            if key in menu_name:
                self.header_label.configure(text=titulo)
                fn()
                return

    # ── KPIs ──────────────────────────────────────────────────────────────────

    def actualizar_kpis(self):
        total    = len(self.db_postulaciones)
        exitosos = sum(1 for p in self.db_postulaciones
                    if p["estado"] in ["Revisado", "En Entrevista"])
        tasa = f"{(exitosos / total * 100):.1f}%" if total > 0 else "0%"
        if self.lbl_postulaciones: self.lbl_postulaciones.configure(text=str(total))
        if self.lbl_tasa:          self.lbl_tasa.configure(text=tasa)
        if self.lbl_ofertas:       self.lbl_ofertas.configure(text=str(random.randint(20, 45)))

    # ── Vista 1: Inicio ───────────────────────────────────────────────────────

    def show_inicio(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        # KPI cards
        cards_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        cards_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="cards")

        self.lbl_ofertas       = self.create_card(cards_frame, 0, "Ofertas Disponibles",
                                                "0", "Nuevas en 2026", "👨‍💻")
        self.lbl_postulaciones = self.create_card(cards_frame, 1, "Postulaciones",
                                                "0", "Estudiantes activos", "🎓")
        self.lbl_tasa          = self.create_card(cards_frame, 2, "Tasa de Éxito",
                                                "0%", "Proceso avanzado", "📈")

        # Tabla wrapper
        table_wrapper = ctk.CTkFrame(self.content_frame,
                                    fg_color=self.colors["fondo_principal"], corner_radius=12)
        table_wrapper.grid(row=1, column=0, sticky="nsew")
        table_wrapper.grid_columnconfigure(0, weight=1)
        table_wrapper.grid_rowconfigure(1, weight=1)

        # Header tabla
        header_frame = ctk.CTkFrame(table_wrapper, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header_frame, text="Solicitudes Recientes",
                    font=("Segoe UI", 16, "bold"),
                    text_color=self.colors["texto_principal"]).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(header_frame, text="+ Registrar Postulante",
                    fg_color=self.colors["acento"], hover_color="#B51B27",
                    font=("Segoe UI", 12, "bold"),
                    command=self.abrir_modal_registro).grid(row=0, column=1, sticky="e")

        # Columnas con columna "Validación"
        columns = ("ID", "Estudiante", "Área", "Validación", "Estado", "Fecha (2026)", "Acciones")
        self.tree = ttk.Treeview(table_wrapper, columns=columns,
                                show="headings", style="Custom.Treeview")
        scrollbar = ttk.Scrollbar(table_wrapper, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(25, 0), pady=(0, 25))
        scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 25), pady=(0, 25))

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column("ID",           width=50,  anchor="center")
        self.tree.column("Estudiante",   width=150)
        self.tree.column("Área",         width=140)
        self.tree.column("Validación",   width=110, anchor="center")
        self.tree.column("Estado",       width=110, anchor="center")
        self.tree.column("Fecha (2026)", width=100, anchor="center")
        self.tree.column("Acciones",     width=120, anchor="center")

        self.tree.tag_configure("Revisado",      background="#D4EDDA", foreground="#155724")
        self.tree.tag_configure("En Entrevista", background="#CCE5FF", foreground="#004085")
        self.tree.tag_configure("Pendiente",     background="#FFF3CD", foreground="#856404")

        # Doble clic abre gestión
        self.tree.bind("<Double-1>", self.abrir_modal_gestion)

        self.cargar_datos_tabla()

    def create_card(self, parent, col, title, value, subtitle, icon):
        pad_x = (0, 15) if col < 2 else (0, 0)
        card  = ctk.CTkFrame(parent, fg_color=self.colors["fondo_principal"], corner_radius=12)
        card.grid(row=0, column=col, sticky="nsew", padx=pad_x)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=(20, 25))

        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x", anchor="w")
        ctk.CTkLabel(top, text=icon, font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(top, text=title, font=("Segoe UI", 16, "bold"),
                    text_color=self.colors["texto_principal"]).pack(side="left")

        lbl_valor = ctk.CTkLabel(inner, text=value, font=("Segoe UI", 32, "bold"),
                                text_color=self.colors["texto_principal"])
        lbl_valor.pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(inner, text=subtitle, font=("Segoe UI", 13),
                    text_color=self.colors["texto_secundario"]).pack(anchor="w")

        ctk.CTkFrame(card, fg_color=self.colors["acento"],
                    height=5, corner_radius=0).pack(side="bottom", fill="x")
        return lbl_valor

    def cargar_datos_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in reversed(self.db_postulaciones):
            self.tree.insert("", "end",
                            values=(r["id"], r["nombre"], r["programa"],
                                    r["validacion"], r["estado"], r["fecha"], "✏️ Gestionar"),
                            tags=(r["estado"],))
        self.actualizar_kpis()

    # ── Vista 2: Empresas ─────────────────────────────────────────────────────

    def show_empresas(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # Cache de referencias de imágenes para evitar recolección de basura
        self._logos_refs = {}

        for emp in self.empresas:
            # ── Tarjeta principal de la empresa ──────────────────────────────
            frame = ctk.CTkFrame(scroll, fg_color=self.colors["fondo_principal"],
                                 corner_radius=12)
            frame.pack(fill="x", pady=10, padx=5, ipady=12)

            # Cabecera: logo + nombre con compound="left"
            ruta_logo = self.logos_estaticos_empresas.get(emp, "")
            if ruta_logo and os.path.exists(ruta_logo):
                try:
                    logo_empresa = ctk.CTkImage(Image.open(ruta_logo), size=(25, 25))
                    self._logos_refs[emp] = logo_empresa
                    ctk.CTkLabel(frame,
                                 text=f" {emp}",
                                 image=logo_empresa,
                                 compound="left",
                                 font=("Segoe UI", 18, "bold"),
                                 text_color=self.colors["primario"]
                                 ).pack(anchor="w", padx=25, pady=(15, 8))
                except Exception:
                    ctk.CTkLabel(frame, text=f"🏢  {emp}",
                                 font=("Segoe UI", 18, "bold"),
                                 text_color=self.colors["primario"]
                                 ).pack(anchor="w", padx=25, pady=(15, 8))
            else:
                ctk.CTkLabel(frame, text=f"🏢  {emp}",
                             font=("Segoe UI", 18, "bold"),
                             text_color=self.colors["primario"]
                             ).pack(anchor="w", padx=25, pady=(15, 8))

            # Separador visual bajo el nombre de la empresa
            ctk.CTkFrame(frame, fg_color=self.colors["fondo_entorno"],
                         height=2, corner_radius=0).pack(fill="x", padx=25, pady=(0, 10))

            # ── Sub-tarjeta por cada perfil/carrera buscado ───────────────────
            for carrera in self.carreras:
                reqs = self.requisitos_area.get(carrera, [])

                sub = ctk.CTkFrame(frame,
                                   fg_color=self.colors["fondo_entorno"],
                                   corner_radius=8)
                sub.pack(fill="x", padx=(45, 25), pady=(0, 8))

                # Nombre del perfil buscado
                ctk.CTkLabel(sub,
                             text=f"📋  Buscando Perfil: {carrera}",
                             font=("Segoe UI", 12, "bold"),
                             text_color=self.colors["texto_principal"]
                             ).pack(anchor="w", padx=14, pady=(10, 4))

                # Requisitos de ese perfil (uno por línea)
                for req in reqs:
                    ctk.CTkLabel(sub,
                                 text=f"  •  {req}",
                                 font=("Segoe UI", 11),
                                 text_color=self.colors["texto_secundario"],
                                 anchor="w"
                                 ).pack(anchor="w", padx=14)

                # Pequeña barra de acento al pie de cada sub-tarjeta
                ctk.CTkFrame(sub, fg_color=self.colors["acento"],
                             height=3, corner_radius=0).pack(fill="x", pady=(8, 0))

    # ── Vista 3: Requisitos ───────────────────────────────────────────────────

    def show_requisitos(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        for area, reqs in self.requisitos_area.items():
            frame = ctk.CTkFrame(self.content_frame,
                                fg_color=self.colors["fondo_principal"], corner_radius=12)
            frame.pack(fill="x", pady=10, padx=5, ipady=10)
            ctk.CTkLabel(frame, text=f"📌 {area}", font=("Segoe UI", 16, "bold"),
                        text_color=self.colors["primario"]).pack(anchor="w", padx=25, pady=(10, 5))
            for r in reqs:
                ctk.CTkLabel(frame, text=f"• {r}", font=("Segoe UI", 13),
                            text_color=self.colors["texto_principal"]).pack(anchor="w", padx=40)

    # ── Modal: Registro ───────────────────────────────────────────────────────

    def abrir_modal_registro(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Nueva Postulación")
        modal.geometry("460x580")
        modal.transient(self)
        modal.grab_set()
        self.foto_temporal = None

        ctk.CTkLabel(modal, text="Registro Académico",
                    font=("Segoe UI", 18, "bold")).pack(pady=20)

        ctk.CTkLabel(modal, text="Nombre Completo:").pack(anchor="w", padx=40)
        ent_nombre = ctk.CTkEntry(modal, width=370)
        ent_nombre.pack(pady=(0, 12), padx=40)

        ctk.CTkLabel(modal, text="Programa Académico:").pack(anchor="w", padx=40)
        cmb_programa = ctk.CTkOptionMenu(modal, values=self.carreras, width=370)
        cmb_programa.pack(pady=(0, 12), padx=40)

        ctk.CTkLabel(modal, text="Empresa:").pack(anchor="w", padx=40)
        cmb_empresa = ctk.CTkOptionMenu(modal, values=self.empresas, width=370)
        cmb_empresa.pack(pady=(0, 12), padx=40)

        # Tipo de validación de conocimiento
        ctk.CTkLabel(modal, text="Tipo de Validación de Conocimiento:").pack(anchor="w", padx=40)
        cmb_validacion = ctk.CTkOptionMenu(modal, values=self.tipos_validacion, width=370)
        cmb_validacion.pack(pady=(0, 12), padx=40)

        # Foto de perfil
        frame_foto = ctk.CTkFrame(modal, fg_color="transparent")
        frame_foto.pack(fill="x", padx=40, pady=(0, 12))
        ctk.CTkLabel(frame_foto, text="Foto de Perfil (.png/.jpg):").pack(side="left")
        lbl_foto_status = ctk.CTkLabel(frame_foto, text="Sin asignar",
                                    text_color=self.colors["texto_secundario"])
        lbl_foto_status.pack(side="right", padx=10)

        def subir_foto():
            ruta = filedialog.askopenfilename(
                filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")], parent=modal)
            if ruta:
                self.foto_temporal = ruta
                lbl_foto_status.configure(text=os.path.basename(ruta)[:18] + "...")

        ctk.CTkButton(frame_foto, text="📂 Examinar", width=100,
                    command=subir_foto,
                    fg_color="#333333", hover_color="#555555").pack(side="right")

        def guardar():
            nombre = ent_nombre.get().strip()
            if not nombre:
                self.dialogo_alerta(modal, "Debes ingresar un nombre.")
                return
            carrera = cmb_programa.get()
            self.db_postulaciones.append({
                "id":          f"{self.contador_ids:03d}",
                "nombre":      nombre,
                "programa":    carrera,
                "estado":      "Pendiente",
                "empresa":     cmb_empresa.get(),
                "fecha":       self.generar_fecha_2026().strftime("%d/%m/%Y"),
                "habilidades": self.generar_habilidades(carrera),
                "validacion":  cmb_validacion.get(),
                "foto":        self.foto_temporal,
            })
            self.contador_ids += 1
            self.cargar_datos_tabla()
            modal.destroy()

        ctk.CTkButton(modal, text="Guardar Registro",
                    fg_color=self.colors["acento"],
                    hover_color=self.colors["hover"],
                    command=guardar).pack(pady=20)

    # ── Modal: Gestión (estado con botones + eliminar) ────────────────────────

    def abrir_modal_gestion(self, event=None, registro_id=None):
        if event is not None:
            item = self.tree.selection()
            if not item:
                return
            registro_id = self.tree.item(item, "values")[0]

        registro = next((r for r in self.db_postulaciones if r["id"] == registro_id), None)
        if not registro:
            return

        modal = ctk.CTkToplevel(self)
        modal.title(f"Gestión: {registro['nombre']}")
        modal.geometry("460x620")
        modal.transient(self)
        modal.grab_set()

        # Foto o avatar
        if registro["foto"] and os.path.exists(registro["foto"]):
            try:
                img      = Image.open(registro["foto"])
                foto_ctk = ctk.CTkImage(light_image=img, size=(100, 100))
                lbl_img  = ctk.CTkLabel(modal, image=foto_ctk, text="")
                lbl_img._img_ref = foto_ctk
                lbl_img.pack(pady=(20, 0))
            except Exception:
                ctk.CTkLabel(modal, text="👤", font=("Segoe UI", 50)).pack(pady=(20, 0))
        else:
            ctk.CTkLabel(modal, text="👤", font=("Segoe UI", 50)).pack(pady=(20, 0))

        ctk.CTkLabel(modal, text=registro["nombre"],
                     font=("Segoe UI", 20, "bold")).pack()
        ctk.CTkLabel(modal,
                     text=f"{registro['programa']}  |  {registro['empresa']}  |  {registro['validacion']}"
                     ).pack(pady=(0, 12))

        # Habilidades
        frame_hab = ctk.CTkFrame(modal, fg_color=self.colors["fondo_principal"], corner_radius=8)
        frame_hab.pack(fill="x", padx=40, pady=(0, 15), ipady=10)
        ctk.CTkLabel(frame_hab, text=f"Competencias en {registro['programa']}:",
                     font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10)
        ctk.CTkLabel(frame_hab, text=registro["habilidades"],
                     wraplength=350, justify="left").pack(anchor="w", padx=10, pady=5)

        # ── Estado con BOTONES de selección ──────────────────────────────────
        ctk.CTkLabel(modal, text="Cambiar Estado:",
                     font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=40)

        estado_var = tk.StringVar(value=registro["estado"])

        frame_estados = ctk.CTkFrame(modal, fg_color="transparent")
        frame_estados.pack(fill="x", padx=40, pady=(8, 20))

        btns_estado = {}

        def seleccionar_estado(est):
            estado_var.set(est)
            for e, btn in btns_estado.items():
                if e == est:
                    btn.configure(fg_color=self.colors["primario"], text_color="white")
                else:
                    btn.configure(fg_color=self.colors["fondo_entorno"],
                                  text_color=self.colors["texto_principal"])

        for est in self.estados_validos:
            btn = ctk.CTkButton(
                frame_estados, text=est, width=120,
                fg_color=self.colors["primario"] if est == registro["estado"]
                         else self.colors["fondo_entorno"],
                text_color="white" if est == registro["estado"]
                           else self.colors["texto_principal"],
                hover_color=self.colors["hover"],
                font=("Segoe UI", 12),
                command=lambda e=est: seleccionar_estado(e)
            )
            btn.pack(side="left", padx=5)
            btns_estado[est] = btn

        # ── Botones acción ────────────────────────────────────────────────────
        def actualizar():
            registro["estado"] = estado_var.get()
            self.cargar_datos_tabla()
            modal.destroy()

        def eliminar():
            self.dialogo_confirmar(
                modal,
                f"¿Eliminar a {registro['nombre']}?",
                on_confirm=lambda: (
                    self.db_postulaciones.remove(registro),
                    self.cargar_datos_tabla(),
                    modal.destroy()
                )
            )

        frame_btns = ctk.CTkFrame(modal, fg_color="transparent")
        frame_btns.pack(fill="x", padx=40, pady=10)

        ctk.CTkButton(frame_btns, text="✅ Guardar Estado",
                      fg_color=self.colors["acento"],
                      hover_color=self.colors["hover"],
                      command=actualizar).pack(side="left", expand=True, padx=5)

        ctk.CTkButton(frame_btns, text="🗑️ Eliminar Registro",
                      fg_color="#333333", hover_color="#5A0814",
                      command=eliminar).pack(side="right", expand=True, padx=5)

    # ── Diálogos ──────────────────────────────────────────────────────────────

    def dialogo_confirmar(self, parent, mensaje, on_confirm):
        dlg = ctk.CTkToplevel(parent)
        dlg.title("Confirmar")
        dlg.geometry("340x160")
        dlg.resizable(False, False)
        dlg.transient(parent)
        dlg.grab_set()
        dlg.lift()
        dlg.focus_force()

        ctk.CTkLabel(dlg, text=mensaje, font=("Segoe UI", 13),
                     wraplength=290).pack(pady=30)

        frame = ctk.CTkFrame(dlg, fg_color="transparent")
        frame.pack()

        def confirmar():
            dlg.destroy()
            on_confirm()

        ctk.CTkButton(frame, text="Sí, eliminar", width=130,
                      fg_color=self.colors["acento"], hover_color="#5A0814",
                      command=confirmar).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Cancelar", width=130,
                      fg_color="#555555", hover_color="#333333",
                      command=dlg.destroy).pack(side="right", padx=10)

    def dialogo_alerta(self, parent, mensaje):
        dlg = ctk.CTkToplevel(parent)
        dlg.title("Atención")
        dlg.geometry("300x130")
        dlg.resizable(False, False)
        dlg.transient(parent)
        dlg.grab_set()
        dlg.lift()
        dlg.focus_force()

        ctk.CTkLabel(dlg, text=mensaje, font=("Segoe UI", 13),
                     wraplength=260).pack(pady=25)
        ctk.CTkButton(dlg, text="Aceptar", width=120,
                      fg_color=self.colors["acento"],
                      hover_color=self.colors["hover"],
                      command=dlg.destroy).pack()


if __name__ == "__main__":
    app = DragoSystemApp()
    app.mainloop()