"""
================================================================================
UROBOROS — Panel de Control Interactivo de Postulaciones
================================================================================

Proyecto   : UROBOROS System v3.0
Asignatura : Introducción a la Programación (Primer Semestre)
Descripción: Aplicación de escritorio para gestionar postulaciones de
            estudiantes universitarios a empresas colombianas.
            Permite registrar, visualizar, editar y eliminar postulantes
            desde una interfaz gráfica moderna construida con CustomTkinter.

Librerías utilizadas:
    - customtkinter : Interfaz gráfica moderna basada en Tkinter
    - tkinter       : Widgets estándar (Spinbox, Treeview, filedialog)
    - Pillow (PIL)  : Carga y redimensionado de imágenes
    - random        : Generación de datos simulados aleatorios
    - os            : Manejo de rutas de archivos del sistema
    - datetime      : Generación de fechas dentro del año 2026
    - winsound      : Retroalimentación auditiva (solo Windows)

Estructura del archivo:
    1. Importaciones y configuración inicial
    2. Constantes y datos globales
    3. Funciones de sonido        (feedback auditivo con winsound)
    4. Funciones de datos          (generar, simular)
    5. Funciones de UI — KPIs      (tarjetas de resumen)
    6. Funciones de UI — Tabla     (Treeview de postulaciones)
    7. Funciones de UI — Diálogos  (alertas y confirmaciones)
    8. Funciones de UI — Modales   (registro y gestión)
    9. Funciones de UI — Vistas    (inicio, empresas, requisitos)
    10. Construcción de la app      (sidebar, contenedor, login)
    11. Punto de entrada             (función main)

================================================================================
"""

# ── Importaciones ─────────────────────────────────────────────────────────────
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import random
import os
import threading                          # Para ejecutar winsound sin congelar la UI
import winsound                           # Sonidos del sistema operativo Windows
from datetime import date, timedelta

# ── Configuración visual global de CustomTkinter ──────────────────────────────
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("dark-blue")


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 1 — CONSTANTES Y DATOS GLOBALES
# ══════════════════════════════════════════════════════════════════════════════

COLORS = {
    "primario":         "#5A0814",
    "hover":            "#730C1B",
    "acento":           "#87129E",
    "fondo_principal":  "#FFFFFF",
    "fondo_entorno":    "#F4F5F7",
    "texto_principal":  "#2B2D42",
    "texto_secundario": "#7A7D85",
    "seleccion":        "#40050E",
}

EMPRESAS_COLOMBIA = [
    "Ecopetrol", "Bancolombia", "Grupo Éxito", "Avianca", "Claro Colombia",
    "Grupo Sura", "Davivienda", "Cemex Colombia", "Postobón", "Bavaria",
    "Alpina", "Corona", "Terpel", "Cementos Argos", "ISA (Interconexión Eléctrica)",
    "Colpatria", "Procredit Colombia", "Nutresa", "ETB", "Telefónica Movistar",
    "Samsung Colombia", "Sodimac Colombia", "Falabella", "Rappi", "Mercado Libre Colombia"
]

NIVELES_EDUCACION = [
    "Técnica Profesional",
    "Tecnólogo",
    "Auxiliar",
    "Practicante",
    "Profesional",
]

REQUISITOS_AREA = {
    "Ingeniería de Sistemas / Informática": {
        "icono": "💻",
        "color_acento": "#0D47A1",
        "requisitos": [
            ("Fundamentos de programación", "Python, Java, C++, JavaScript"),
            ("Bases de datos", "SQL (PostgreSQL, MySQL) y NoSQL (MongoDB, Redis)"),
            ("Arquitectura de software", "Patrones de diseño, microservicios, API REST"),
            ("Metodologías ágiles", "Scrum, Kanban, DevOps, CI/CD"),
            ("Redes y seguridad", "TCP/IP, ciberseguridad básica, OWASP"),
            ("Inteligencia Artificial", "Machine Learning, redes neuronales, scikit-learn"),
            ("Cloud Computing", "AWS, Google Cloud o Azure (nivel básico-medio)"),
            ("Control de versiones", "Git, GitHub/GitLab, flujos de trabajo colaborativo"),
        ],
        "soft_skills": ["Pensamiento lógico", "Resolución de problemas", "Trabajo en equipo", "Aprendizaje continuo"],
    },
    "Diseño Visual / Gráfico": {
        "icono": "🎨",
        "color_acento": "#6A1B9A",
        "requisitos": [
            ("Suite Adobe", "Illustrator, Photoshop, InDesign, After Effects"),
            ("Diseño UI/UX", "Figma, Adobe XD, prototipado de alta fidelidad"),
            ("Teoría del color y tipografía", "Psicología del color, jerarquía visual, grid systems"),
            ("Identidad de marca", "Branding, manual de marca, diseño de logos"),
            ("Motion Graphics", "Animación básica, transiciones, microinteracciones"),
            ("Fotografía y edición", "Composición, retoque fotográfico, dirección de arte"),
            ("Impresión y producción", "Preparación de archivos para imprenta, formatos"),
            ("Marketing digital", "Diseño para redes sociales, banners, email marketing"),
        ],
        "soft_skills": ["Creatividad", "Atención al detalle", "Comunicación visual", "Adaptabilidad"],
    },
    "Ingeniería Industrial": {
        "icono": "⚙️",
        "color_acento": "#E65100",
        "requisitos": [
            ("Optimización de procesos", "Lean Manufacturing, Six Sigma, Kaizen"),
            ("Logística y cadena de suministro", "SCM, gestión de inventarios, distribución"),
            ("Gestión de calidad", "ISO 9001, control estadístico de procesos (SPC)"),
            ("Seguridad industrial", "HSEQ, normativa ARL, gestión de riesgos"),
            ("Gestión financiera", "Evaluación de proyectos, VPN, TIR, costos industriales"),
            ("Automatización", "PLC básico, robótica industrial, Industria 4.0"),
            ("Simulación y modelado", "Arena, ProModel, análisis de sistemas"),
            ("Gestión de proyectos", "PMI/PMP, MS Project, cronogramas y presupuestos"),
        ],
        "soft_skills": ["Liderazgo operativo", "Análisis crítico", "Trabajo bajo presión", "Gestión del tiempo"],
    },
    "Administración de Empresas": {
        "icono": "📊",
        "color_acento": "#1B5E20",
        "requisitos": [
            ("Liderazgo y gestión", "Dirección de equipos, toma de decisiones estratégicas"),
            ("Finanzas corporativas", "Análisis financiero, presupuestos, estados financieros"),
            ("Recursos Humanos", "Selección, capacitación, gestión del desempeño, nómina"),
            ("Marketing y ventas", "Estrategias comerciales, CRM, marketing digital"),
            ("Derecho empresarial", "Normativas laborales, contratos, régimen tributario"),
            ("Gestión de proyectos", "PMI, metodologías ágiles, OKRs, KPIs"),
            ("Emprendimiento", "Modelos de negocio, Canvas, pitch, financiación"),
            ("Comercio internacional", "Incoterms, exportaciones, regulaciones aduaneras"),
        ],
        "soft_skills": ["Visión estratégica", "Negociación", "Comunicación efectiva", "Inteligencia emocional"],
    },
    "Medicina / Ciencias de la Salud": {
        "icono": "🏥",
        "color_acento": "#B71C1C",
        "requisitos": [
            ("Ciencias básicas", "Anatomía, fisiología, bioquímica, farmacología"),
            ("Clínica y diagnóstico", "Semiología, historia clínica, interpretación de exámenes"),
            ("Urgencias y primeros auxilios", "RCP, manejo de trauma, soporte vital básico"),
            ("Salud pública", "Epidemiología, estadística, medicina preventiva"),
            ("Ética médica", "Bioética, consentimiento informado, confidencialidad"),
            ("Tecnología médica", "Historia clínica electrónica (HCE), telemedicina"),
            ("Investigación clínica", "Metodología de investigación, GCP, ensayos clínicos"),
            ("Especialidades", "Rotaciones en medicina interna, pediatría, cirugía, psiquiatría"),
        ],
        "soft_skills": ["Empatía", "Comunicación con pacientes", "Trabajo en equipo multidisciplinar", "Resiliencia"],
    },
    "Derecho": {
        "icono": "⚖️",
        "color_acento": "#37474F",
        "requisitos": [
            ("Derecho civil y comercial", "Contratos, obligaciones, responsabilidad civil"),
            ("Derecho laboral", "Código Sustantivo del Trabajo, nómina, seguridad social"),
            ("Derecho penal", "Código Penal colombiano, procedimiento penal acusatorio"),
            ("Derecho constitucional", "Tutelas, acciones populares, derechos fundamentales"),
            ("Litigio y oralidad", "Técnicas de argumentación, oratoria, audiencias orales"),
            ("Derecho tributario", "DIAN, obligaciones fiscales, declaraciones de renta"),
            ("Derecho internacional", "Tratados, DIH, comercio exterior"),
            ("Investigación jurídica", "Bases de datos legales, doctrina, jurisprudencia"),
        ],
        "soft_skills": ["Argumentación lógica", "Ética profesional", "Redacción jurídica", "Gestión del tiempo"],
    },
}

LOGOS_ESTATICOS = {
    "Google":    os.path.join("assets", "google.png"),
    "Microsoft": os.path.join("assets", "microsoft.png"),
    "Oracle":    os.path.join("assets", "oracle.png"),
    "Amd":       os.path.join("assets", "amd.png"),
}

# ── Variables globales de estado ──────────────────────────────────────────────
db_postulaciones = []
contador_ids     = [1]
_img_refs        = {}
tree_widget      = None
lbl_ofertas_kpi  = None
lbl_post_kpi     = None
lbl_tasa_kpi     = None


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 2 — FUNCIONES DE SONIDO
#
#  Todas las funciones de sonido usan threading.Thread para ejecutarse en
#  un hilo separado. Esto es IMPORTANTE: winsound.Beep() bloquea el hilo
#  mientras suena. Si lo llamamos desde el hilo principal, la interfaz
#  gráfica se "congela" hasta que el sonido termina.
#  Ejecutándolo en un hilo aparte, la UI sigue respondiendo normalmente.
#
#  Cada función tiene un propósito semántico claro:
#    - sonido_login()    → bienvenida al iniciar sesión
#    - sonido_exito()    → confirmación al guardar datos
#    - sonido_error()    → alerta cuando hay un error de validación
#    - sonido_eliminar() → advertencia antes/durante eliminación
#    - sonido_clic()     → feedback suave de navegación
#    - sonido_modal()    → apertura de ventana emergente
# ══════════════════════════════════════════════════════════════════════════════

def _reproducir_en_hilo(secuencia):
    """
    Función interna que ejecuta una secuencia de Beep en un hilo separado.

    Parámetros:
        secuencia (list of tuples) : Lista de (frecuencia_hz, duracion_ms)
                                     Ejemplo: [(880, 100), (1100, 80)]

    Uso interno: las funciones públicas de sonido llaman a esta función
    para no bloquear la interfaz gráfica mientras suena el audio.
    """
    def _run():
        for frecuencia, duracion in secuencia:
            winsound.Beep(frecuencia, duracion)

    threading.Thread(target=_run, daemon=True).start()
    # daemon=True: el hilo se cierra automáticamente cuando la app termina


def sonido_login():
    """
    Fanfare de bienvenida al presionar 'Iniciar Sesión'.

    Melodía ascendente de 4 notas que da sensación de apertura y bienvenida.
    Notas: Do4 → Mi4 → Sol4 → Do5 (acorde de Do mayor arpeggiado)
    """
    _reproducir_en_hilo([
        (523, 90),   # Do4
        (659, 90),   # Mi4
        (784, 90),   # Sol4
        (1047, 140), # Do5
    ])


def sonido_exito():
    """
    Confirmación positiva al guardar un nuevo postulante o editar uno existente.

    Dos notas ascendentes cortas: sensación de "listo" / "completado".
    """
    _reproducir_en_hilo([
        (880, 100),  # La5
        (1100, 120), # Do#6 (nota más alta = éxito)
    ])


def sonido_error():
    """
    Alerta de error al dejar campos obligatorios vacíos.

    Nota grave repetida con pausa: comunica "algo está mal".
    La frecuencia baja (300 Hz) se percibe como seria y urgente.
    """
    _reproducir_en_hilo([
        (300, 180),  # Re3 — nota grave de advertencia
        (50, 40),    # Silencio breve (frecuencia muy baja = inaudible)
        (300, 180),  # Re3 — repite para reforzar la alerta
    ])


def sonido_eliminar():
    """
    Sonido descendente al confirmar la eliminación de un registro.

    Tres notas descendentes: comunica "algo desapareció" / "acción irreversible".
    El patrón descendente es universalmente reconocido como "fin" o "salida".
    """
    _reproducir_en_hilo([
        (600, 100),  # Re5 — inicio
        (450, 100),  # La4 — descenso
        (300, 160),  # Re3 — cierre grave
    ])


def sonido_clic():
    """
    Feedback auditivo suave al hacer clic en botones del menú lateral.

    Un único beep corto y agudo: discreto, no intrusivo.
    Frecuencia media-alta (700 Hz) para que se perciba como "táctil".
    """
    _reproducir_en_hilo([
        (700, 55),   # Fa5 — clic suave
    ])


def sonido_modal():
    """
    Sonido de apertura al mostrar una ventana modal (registro o gestión).

    Dos notas: la segunda más alta, dando sensación de "expansión" o "apertura".
    Más suave que el sonido de éxito para no ser intrusivo.
    """
    _reproducir_en_hilo([
        (600, 70),   # Re5
        (800, 80),   # Sol5
    ])


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 3 — FUNCIONES DE DATOS
# ══════════════════════════════════════════════════════════════════════════════

def generar_fecha_2026():
    """
    Genera y retorna una fecha aleatoria dentro del año 2026.
    """
    inicio = date(2026, 1, 1)
    fin    = date(2026, 12, 31)
    return inicio + timedelta(days=random.randrange((fin - inicio).days))


def generar_datos_simulados():
    """
    Agrega 3 postulantes de ejemplo a la lista global db_postulaciones.
    """
    nombres  = ["Julian Bejarano", "Ana Maria Silva", "Carlos Mendoza"]
    estados  = ["Revisado", "En Entrevista", "Pendiente"]
    carreras = ["Ingeniería de Sistemas", "Diseño Visual", "Administración"]
    competencias_muestra = [
        "Python | SQL | Docker | 2 años de exp. empresarial",
        "Figma | Adobe Suite | UI/UX | 1 año de exp. empresarial",
        "Liderazgo | Finanzas | Gestión de Proyectos | 0 años de exp. empresarial",
    ]

    for i in range(3):
        db_postulaciones.append({
            "id":           f"{contador_ids[0]:03d}",
            "nombre":       nombres[i],
            "programa":     carreras[i],
            "estado":       estados[i],
            "empresa":      random.choice(EMPRESAS_COLOMBIA),
            "fecha":        generar_fecha_2026().strftime("%d/%m/%Y"),
            "competencias": competencias_muestra[i],
            "nivel_edu":    NIVELES_EDUCACION[i % len(NIVELES_EDUCACION)],
            "anios_exp":    random.randint(0, 3),
            "foto":         None,
        })
        contador_ids[0] += 1


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 4 — FUNCIONES DE UI: KPIs
# ══════════════════════════════════════════════════════════════════════════════

def actualizar_kpis():
    global lbl_ofertas_kpi, lbl_post_kpi, lbl_tasa_kpi

    total    = len(db_postulaciones)
    exitosos = sum(1 for p in db_postulaciones if p["estado"] in ["Revisado", "En Entrevista"])
    tasa     = f"{(exitosos / total * 100):.1f}%" if total > 0 else "0%"

    if lbl_post_kpi:    lbl_post_kpi.configure(text=str(total))
    if lbl_tasa_kpi:    lbl_tasa_kpi.configure(text=tasa)
    if lbl_ofertas_kpi: lbl_ofertas_kpi.configure(text=str(random.randint(20, 45)))


def create_card(parent, col, title, value, subtitle, icon):
    global lbl_ofertas_kpi, lbl_post_kpi, lbl_tasa_kpi

    pad_x = (0, 15) if col < 2 else (0, 0)
    card  = ctk.CTkFrame(parent, fg_color=COLORS["fondo_principal"], corner_radius=12)
    card.grid(row=0, column=col, sticky="nsew", padx=pad_x)

    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(fill="both", expand=True, padx=20, pady=(20, 25))

    top = ctk.CTkFrame(inner, fg_color="transparent")
    top.pack(fill="x", anchor="w")
    ctk.CTkLabel(top, text=icon,  font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
    ctk.CTkLabel(top, text=title, font=("Segoe UI", 16, "bold"),
                 text_color=COLORS["texto_principal"]).pack(side="left")

    lbl_valor = ctk.CTkLabel(inner, text=value, font=("Segoe UI", 32, "bold"),
                              text_color=COLORS["texto_principal"])
    lbl_valor.pack(anchor="w", pady=(10, 0))

    ctk.CTkLabel(inner, text=subtitle, font=("Segoe UI", 13),
                 text_color=COLORS["texto_secundario"]).pack(anchor="w")

    ctk.CTkFrame(card, fg_color=COLORS["acento"], height=5, corner_radius=0).pack(side="bottom", fill="x")

    if col == 0:   lbl_ofertas_kpi = lbl_valor
    elif col == 1: lbl_post_kpi    = lbl_valor
    elif col == 2: lbl_tasa_kpi    = lbl_valor

    return lbl_valor


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 5 — FUNCIONES DE UI: TABLA (Treeview)
# ══════════════════════════════════════════════════════════════════════════════

def cargar_datos_tabla():
    global tree_widget

    if tree_widget is None:
        return

    for row in tree_widget.get_children():
        tree_widget.delete(row)

    for r in reversed(db_postulaciones):
        tree_widget.insert(
            "", "end",
            values=(
                r["id"], r["nombre"], r["programa"],
                r["nivel_edu"], r["estado"], r["fecha"], "✏️ Gestionar"
            ),
            tags=(r["estado"],)
        )

    actualizar_kpis()


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 6 — FUNCIONES DE UI: DIÁLOGOS
# ══════════════════════════════════════════════════════════════════════════════

def dialogo_alerta(parent, mensaje):
    """
    Muestra una ventana emergente de aviso.
    Reproduce sonido_error() al abrirse para alertar al usuario.
    """
    sonido_error()   # ← Sonido de error al mostrar la alerta

    dlg = ctk.CTkToplevel(parent)
    dlg.title("Atención")
    dlg.geometry("300x130")
    dlg.resizable(False, False)
    dlg.transient(parent)
    dlg.grab_set()
    dlg.lift()
    dlg.focus_force()

    ctk.CTkLabel(dlg, text=mensaje, font=("Segoe UI", 13), wraplength=260).pack(pady=25)
    ctk.CTkButton(dlg, text="Aceptar", width=120,
                  fg_color=COLORS["acento"], hover_color=COLORS["hover"],
                  command=dlg.destroy).pack()


def dialogo_confirmar(parent, mensaje, on_confirm):
    """
    Muestra una ventana de confirmación antes de eliminar un registro.
    El sonido de eliminación suena al confirmar (no al abrir el diálogo).
    """
    dlg = ctk.CTkToplevel(parent)
    dlg.title("Confirmar")
    dlg.geometry("340x160")
    dlg.resizable(False, False)
    dlg.transient(parent)
    dlg.grab_set()
    dlg.lift()
    dlg.focus_force()

    ctk.CTkLabel(dlg, text=mensaje, font=("Segoe UI", 13), wraplength=290).pack(pady=30)

    frame = ctk.CTkFrame(dlg, fg_color="transparent")
    frame.pack()

    def confirmar():
        """
        Reproduce sonido_eliminar() ANTES de ejecutar la acción de borrado,
        para que el usuario reciba feedback inmediato de la confirmación.
        """
        sonido_eliminar()   # ← Sonido de eliminación al confirmar
        dlg.destroy()
        on_confirm()

    ctk.CTkButton(frame, text="Sí, eliminar", width=130,
                  fg_color=COLORS["acento"], hover_color="#20BF3B",
                  command=confirmar).pack(side="left", padx=10)

    ctk.CTkButton(frame, text="Cancelar", width=130,
                  fg_color="#555555", hover_color="#941A1A",
                  command=dlg.destroy).pack(side="right", padx=10)


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 7 — FUNCIONES DE UI: MODALES
# ══════════════════════════════════════════════════════════════════════════════

def abrir_modal_registro(app):
    """
    Abre la ventana modal para registrar un nuevo postulante.
    Reproduce sonido_modal() al abrirse.
    """
    sonido_modal()   # ← Sonido de apertura de ventana modal

    foto_temporal = [None]

    modal = ctk.CTkToplevel(app)
    modal.title("Nueva Postulación")
    modal.geometry("500x660")
    modal.transient(app)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Registro de Postulante",
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 5))

    ctk.CTkLabel(modal, text="Nombre Completo:", anchor="w").pack(anchor="w", padx=40)
    ent_nombre = ctk.CTkEntry(modal, width=400, placeholder_text="Ej: Laura Gómez Pérez")
    ent_nombre.pack(pady=(0, 12), padx=40)

    ctk.CTkLabel(modal, text="Programa Académico (escribe la carrera):", anchor="w").pack(anchor="w", padx=40)
    ent_programa = ctk.CTkEntry(modal, width=400, placeholder_text="Ej: Ingeniería Mecatrónica")
    ent_programa.pack(pady=(0, 12), padx=40)

    ctk.CTkLabel(modal, text="Empresa:", anchor="w").pack(anchor="w", padx=40)
    cmb_empresa = ctk.CTkOptionMenu(modal, values=EMPRESAS_COLOMBIA, width=400)
    cmb_empresa.pack(pady=(0, 12), padx=40)

    ctk.CTkLabel(modal, text="Nivel de Educación:", anchor="w").pack(anchor="w", padx=40)
    cmb_nivel = ctk.CTkOptionMenu(modal, values=NIVELES_EDUCACION, width=400)
    cmb_nivel.set(NIVELES_EDUCACION[0])
    cmb_nivel.pack(pady=(0, 12), padx=40)

    frame_exp = ctk.CTkFrame(modal, fg_color="transparent")
    frame_exp.pack(fill="x", padx=40, pady=(0, 12))
    ctk.CTkLabel(frame_exp, text="Años de Experiencia Laboral:").pack(side="left")
    spin_exp = tk.Spinbox(frame_exp, from_=0, to=30, width=5,
                          font=("Segoe UI", 13), justify="center")
    spin_exp.delete(0, "end")
    spin_exp.insert(0, "0")
    spin_exp.pack(side="right")

    ctk.CTkLabel(modal, text="Competencias del Postulante:", anchor="w").pack(anchor="w", padx=40)
    txt_competencias = ctk.CTkTextbox(modal, width=400, height=80)
    txt_competencias.pack(pady=(0, 4), padx=40)
    ctk.CTkLabel(modal,
                 text="Escribe las habilidades separadas por | (ej: Python | SQL | Liderazgo)",
                 font=("Segoe UI", 10), text_color=COLORS["texto_secundario"]
                 ).pack(anchor="w", padx=40, pady=(0, 10))

    frame_foto = ctk.CTkFrame(modal, fg_color="transparent")
    frame_foto.pack(fill="x", padx=40, pady=(0, 12))
    ctk.CTkLabel(frame_foto, text="Foto de Perfil (.png/.jpg):").pack(side="left")
    lbl_foto_status = ctk.CTkLabel(frame_foto, text="Sin asignar",
                                   text_color=COLORS["texto_secundario"])
    lbl_foto_status.pack(side="right", padx=10)

    def subir_foto():
        ruta = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")], parent=modal)
        if ruta:
            foto_temporal[0] = ruta
            lbl_foto_status.configure(text=os.path.basename(ruta)[:20] + "...")

    ctk.CTkButton(frame_foto, text="📂 Examinar", width=110,
                  fg_color="#CF5F1A", hover_color="#A53912",
                  command=subir_foto).pack(side="right")

    def guardar():
        """
        Valida y guarda el nuevo postulante.
        - Si hay error: reproduce sonido_error() a través de dialogo_alerta()
        - Si guarda bien: reproduce sonido_exito()
        """
        nombre   = ent_nombre.get().strip()
        programa = ent_programa.get().strip()

        if not nombre:
            dialogo_alerta(modal, "Debes ingresar el nombre del postulante.")
            return
        if not programa:
            dialogo_alerta(modal, "Debes ingresar el programa académico.")
            return

        competencias_txt  = txt_competencias.get("1.0", "end").strip()
        anios             = int(spin_exp.get())
        competencias_final = (
            competencias_txt + f" | {anios} año(s) de exp. laboral"
            if competencias_txt else f"{anios} año(s) de exp. laboral"
        )

        db_postulaciones.append({
            "id":           f"{contador_ids[0]:03d}",
            "nombre":       nombre,
            "programa":     programa,
            "estado":       "Pendiente",
            "empresa":      cmb_empresa.get(),
            "fecha":        generar_fecha_2026().strftime("%d/%m/%Y"),
            "competencias": competencias_final,
            "nivel_edu":    cmb_nivel.get(),
            "anios_exp":    anios,
            "foto":         foto_temporal[0],
        })
        contador_ids[0] += 1

        sonido_exito()       # ← Sonido de éxito al guardar el nuevo postulante
        cargar_datos_tabla()
        modal.destroy()

    ctk.CTkButton(modal, text="💾  Guardar Registro",
                  fg_color=COLORS["acento"], hover_color=COLORS["hover"],
                  font=("Segoe UI", 13, "bold"), height=42,
                  command=guardar).pack(pady=16)


def abrir_modal_gestion(app, event=None, registro_id=None):
    """
    Abre la ventana modal para ver y editar un postulante existente.
    Reproduce sonido_modal() al abrirse.
    Al guardar cambios: sonido_exito()
    Al eliminar: sonido_eliminar() (dentro de dialogo_confirmar)
    """
    global tree_widget

    if event is not None:
        item = tree_widget.selection()
        if not item:
            return
        registro_id = tree_widget.item(item, "values")[0]

    registro = next((r for r in db_postulaciones if r["id"] == registro_id), None)
    if not registro:
        return

    sonido_modal()   # ← Sonido de apertura al mostrar el modal de gestión

    modal = ctk.CTkToplevel(app)
    modal.title(f"Gestión: {registro['nombre']}")
    modal.geometry("480x660")
    modal.transient(app)
    modal.grab_set()

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
                 text=f"{registro['programa']}  |  {registro['empresa']}  |  {registro['nivel_edu']}"
                 ).pack(pady=(0, 10))

    frame_comp = ctk.CTkFrame(modal, fg_color=COLORS["fondo_principal"], corner_radius=8)
    frame_comp.pack(fill="x", padx=35, pady=(0, 10), ipady=8)
    ctk.CTkLabel(frame_comp,
                 text=f"Competencias en {registro['programa']}:",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(6, 2))
    txt_comp_edit = ctk.CTkTextbox(frame_comp, width=390, height=70)
    txt_comp_edit.insert("1.0", registro["competencias"])
    txt_comp_edit.pack(padx=12, pady=(0, 6))

    frame_exp = ctk.CTkFrame(modal, fg_color="transparent")
    frame_exp.pack(fill="x", padx=35, pady=(0, 10))
    ctk.CTkLabel(frame_exp, text="Años de Experiencia:").pack(side="left")
    spin_exp2 = tk.Spinbox(frame_exp, from_=0, to=30, width=5,
                           font=("Segoe UI", 13), justify="center")
    spin_exp2.delete(0, "end")
    spin_exp2.insert(0, str(registro.get("anios_exp", 0)))
    spin_exp2.pack(side="right")

    ctk.CTkLabel(modal, text="Cambiar Estado:",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=35)

    estados_validos = ["Pendiente", "En Entrevista", "Revisado"]
    estado_var      = tk.StringVar(value=registro["estado"])
    frame_estados   = ctk.CTkFrame(modal, fg_color="transparent")
    frame_estados.pack(fill="x", padx=35, pady=(8, 16))
    btns_estado = {}

    def seleccionar_estado(est):
        estado_var.set(est)
        sonido_clic()   # ← Sonido suave al cambiar el estado del postulante
        for e, btn in btns_estado.items():
            if e == est:
                btn.configure(fg_color=COLORS["primario"], text_color="white")
            else:
                btn.configure(fg_color=COLORS["fondo_entorno"],
                              text_color=COLORS["texto_principal"])

    for est in estados_validos:
        btn = ctk.CTkButton(
            frame_estados, text=est, width=130,
            fg_color=COLORS["primario"] if est == registro["estado"] else COLORS["fondo_entorno"],
            text_color="white" if est == registro["estado"] else COLORS["texto_principal"],
            hover_color=COLORS["hover"], font=("Segoe UI", 12),
            command=lambda e=est: seleccionar_estado(e)
        )
        btn.pack(side="left", padx=4)
        btns_estado[est] = btn

    def actualizar():
        """
        Guarda los cambios del postulante y reproduce sonido_exito().
        """
        registro["estado"]       = estado_var.get()
        registro["competencias"] = txt_comp_edit.get("1.0", "end").strip()
        registro["anios_exp"]    = int(spin_exp2.get())
        sonido_exito()       # ← Sonido de éxito al guardar los cambios
        cargar_datos_tabla()
        modal.destroy()

    def eliminar():
        """
        Abre diálogo de confirmación. El sonido de eliminación se reproduce
        dentro de dialogo_confirmar() al presionar 'Sí, eliminar'.
        """
        dialogo_confirmar(
            modal,
            f"¿Eliminar a {registro['nombre']}?",
            on_confirm=lambda: (
                db_postulaciones.remove(registro),
                cargar_datos_tabla(),
                modal.destroy()
            )
        )

    frame_btns = ctk.CTkFrame(modal, fg_color="transparent")
    frame_btns.pack(fill="x", padx=35, pady=8)

    ctk.CTkButton(frame_btns, text="✅ Guardar Cambios",
                  fg_color=COLORS["acento"], hover_color=COLORS["hover"],
                  command=actualizar).pack(side="left", expand=True, padx=5)

    ctk.CTkButton(frame_btns, text="🗑️ Eliminar Registro",
                  fg_color="#333333", hover_color="#5A0814",
                  command=eliminar).pack(side="right", expand=True, padx=5)


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 8 — FUNCIONES DE UI: VISTAS PRINCIPALES
# ══════════════════════════════════════════════════════════════════════════════

def show_inicio(content_frame, app):
    global tree_widget, lbl_ofertas_kpi, lbl_post_kpi, lbl_tasa_kpi

    for w in content_frame.winfo_children():
        w.destroy()

    cards_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    cards_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
    cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="cards")

    create_card(cards_frame, 0, "Ofertas Disponibles", "0", "Nuevas en 2026", "👨‍💻")
    create_card(cards_frame, 1, "Postulaciones",        "0", "Estudiantes activos", "🎓")
    create_card(cards_frame, 2, "Tasa de Éxito",        "0%", "Proceso avanzado",   "📈")

    table_wrapper = ctk.CTkFrame(content_frame, fg_color=COLORS["fondo_principal"], corner_radius=12)
    table_wrapper.grid(row=1, column=0, sticky="nsew")
    table_wrapper.grid_columnconfigure(0, weight=1)
    table_wrapper.grid_rowconfigure(1, weight=1)

    header_frame = ctk.CTkFrame(table_wrapper, fg_color="transparent")
    header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 10))
    header_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(header_frame, text="Solicitudes Recientes",
                 font=("Segoe UI", 16, "bold"),
                 text_color=COLORS["texto_principal"]).grid(row=0, column=0, sticky="w")

    ctk.CTkButton(header_frame, text="+ Registrar Postulante",
                  fg_color=COLORS["acento"], hover_color="#B51B27",
                  font=("Segoe UI", 12, "bold"),
                  command=lambda: abrir_modal_registro(app)).grid(row=0, column=1, sticky="e")

    columns = ("ID", "Estudiante", "Programa", "Nivel Edu.", "Estado", "Fecha (2026)", "Acciones")
    tree_widget = ttk.Treeview(table_wrapper, columns=columns,
                               show="headings", style="Custom.Treeview")

    scrollbar = ttk.Scrollbar(table_wrapper, orient="vertical", command=tree_widget.yview)
    tree_widget.configure(yscroll=scrollbar.set)

    tree_widget.grid(row=1, column=0, sticky="nsew", padx=(25, 0), pady=(0, 25))
    scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 25), pady=(0, 25))

    for col in columns:
        tree_widget.heading(col, text=col)
    tree_widget.column("ID",           width=50,  anchor="center")
    tree_widget.column("Estudiante",   width=150)
    tree_widget.column("Programa",     width=160)
    tree_widget.column("Nivel Edu.",   width=130, anchor="center")
    tree_widget.column("Estado",       width=110, anchor="center")
    tree_widget.column("Fecha (2026)", width=100, anchor="center")
    tree_widget.column("Acciones",     width=110, anchor="center")

    tree_widget.tag_configure("Revisado",      background="#D4EDDA", foreground="#155724")
    tree_widget.tag_configure("En Entrevista", background="#CCE5FF", foreground="#004085")
    tree_widget.tag_configure("Pendiente",     background="#FFF3CD", foreground="#856404")

    tree_widget.bind("<Double-1>", lambda e: abrir_modal_gestion(app, event=e))

    cargar_datos_tabla()


def show_empresas(content_frame):
    for w in content_frame.winfo_children():
        w.destroy()

    scroll = ctk.CTkScrollableFrame(content_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True)

    iconos_empresa = ["🏭", "🏦", "🛒", "✈️", "📡", "🏗️", "💳", "🧱", "🥤", "🍺",
                      "🥛", "🏺", "⛽", "🪨", "⚡", "🏛️", "💼", "🍫", "📞", "📱",
                      "📺", "🛋️", "🛍️", "🚀", "🛒"]
    sectores = ["Energía", "Financiero", "Retail", "Transporte", "Telecomunicaciones",
                "Construcción", "Financiero", "Construcción", "Bebidas", "Bebidas",
                "Alimentos", "Cerámica", "Combustibles", "Materiales", "Energía",
                "Seguros", "Financiero", "Alimentos", "Telecomunicaciones", "Telecomunicaciones",
                "Tecnología", "Retail", "Retail", "Tecnología/Delivery", "E-commerce"]

    empresas_con_info = []
    for i, emp in enumerate(EMPRESAS_COLOMBIA):
        empresas_con_info.append({
            "nombre":   emp,
            "icono":    iconos_empresa[i % len(iconos_empresa)],
            "sector":   sectores[i % len(sectores)],
            "ciudad":   random.choice(["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga"]),
            "vacantes": random.randint(1, 12),
            "perfiles": random.sample(list(REQUISITOS_AREA.keys()), k=random.randint(2, 3)),
        })

    ctk.CTkLabel(scroll, text="🏢  Directorio de Empresas Colombia 2026",
                 font=("Segoe UI", 20, "bold"),
                 text_color=COLORS["primario"]).pack(anchor="w", padx=5, pady=(0, 16))

    grid_frame = ctk.CTkFrame(scroll, fg_color="transparent")
    grid_frame.pack(fill="both", expand=True)
    grid_frame.columnconfigure((0, 1, 2), weight=1, uniform="emp")

    for idx, emp_info in enumerate(empresas_con_info):
        fila = idx // 3
        col  = idx %  3

        card = ctk.CTkFrame(grid_frame, fg_color=COLORS["fondo_principal"], corner_radius=12)
        card.grid(row=fila, column=col, padx=8, pady=8, sticky="nsew")

        ctk.CTkFrame(card, fg_color=COLORS["primario"], corner_radius=0, height=12).pack(fill="x")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        ctk.CTkLabel(inner,
                     text=f"{emp_info['icono']}  {emp_info['nombre']}",
                     font=("Segoe UI", 13, "bold"),
                     text_color=COLORS["primario"], anchor="w").pack(anchor="w")

        ctk.CTkLabel(inner,
                     text=f"📍 {emp_info['ciudad']}   🏷️ {emp_info['sector']}",
                     font=("Segoe UI", 10),
                     text_color=COLORS["texto_secundario"], anchor="w").pack(anchor="w", pady=(2, 6))

        ctk.CTkLabel(inner,
                     text=f"🔍 {emp_info['vacantes']} vacante(s) disponibles",
                     font=("Segoe UI", 11, "bold"),
                     text_color=COLORS["acento"], anchor="w").pack(anchor="w", pady=(0, 6))

        ctk.CTkLabel(inner, text="Perfiles buscados:",
                     font=("Segoe UI", 10, "bold"),
                     text_color=COLORS["texto_principal"], anchor="w").pack(anchor="w")
        for perfil in emp_info["perfiles"]:
            icono_area = REQUISITOS_AREA.get(perfil, {}).get("icono", "📋")
            ctk.CTkLabel(inner,
                         text=f"  {icono_area} {perfil}",
                         font=("Segoe UI", 10),
                         text_color=COLORS["texto_secundario"], anchor="w").pack(anchor="w")


def show_requisitos(content_frame):
    for w in content_frame.winfo_children():
        w.destroy()

    scroll = ctk.CTkScrollableFrame(content_frame, fg_color="transparent")
    scroll.pack(fill="both", expand=True)

    ctk.CTkLabel(scroll, text="📚  Requisitos por Área Académica",
                 font=("Segoe UI", 20, "bold"),
                 text_color=COLORS["primario"]).pack(anchor="w", padx=5, pady=(0, 16))

    for area, info in REQUISITOS_AREA.items():
        frame = ctk.CTkFrame(scroll, fg_color=COLORS["fondo_principal"], corner_radius=14)
        frame.pack(fill="x", pady=10, padx=4, ipady=6)

        ctk.CTkFrame(frame, fg_color=info["color_acento"], corner_radius=0, height=6).pack(fill="x")

        title_row = ctk.CTkFrame(frame, fg_color="transparent")
        title_row.pack(fill="x", padx=24, pady=(14, 6))
        ctk.CTkLabel(title_row,
                     text=f"{info['icono']}  {area}",
                     font=("Segoe UI", 17, "bold"),
                     text_color=COLORS["primario"]).pack(side="left")

        grid_req = ctk.CTkFrame(frame, fg_color="transparent")
        grid_req.pack(fill="x", padx=24, pady=(0, 10))
        grid_req.columnconfigure((0, 1), weight=1, uniform="req")

        for i, (titulo_req, detalle_req) in enumerate(info["requisitos"]):
            fila_r = i // 2
            col_r  = i %  2

            sub = ctk.CTkFrame(grid_req, fg_color=COLORS["fondo_entorno"], corner_radius=8)
            sub.grid(row=fila_r, column=col_r, padx=6, pady=5, sticky="nsew")

            inner_sub = ctk.CTkFrame(sub, fg_color="transparent")
            inner_sub.pack(fill="both", padx=12, pady=8)

            ctk.CTkLabel(inner_sub,
                         text=f"✦ {titulo_req}",
                         font=("Segoe UI", 11, "bold"),
                         text_color=info["color_acento"],
                         anchor="w").pack(anchor="w")

            ctk.CTkLabel(inner_sub,
                         text=detalle_req,
                         font=("Segoe UI", 10),
                         text_color=COLORS["texto_principal"],
                         wraplength=230,
                         anchor="w",
                         justify="left").pack(anchor="w", pady=(2, 0))

        soft_frame = ctk.CTkFrame(frame, fg_color=COLORS["fondo_entorno"], corner_radius=8)
        soft_frame.pack(fill="x", padx=24, pady=(0, 14))
        soft_inner = ctk.CTkFrame(soft_frame, fg_color="transparent")
        soft_inner.pack(fill="x", padx=12, pady=8)

        ctk.CTkLabel(soft_inner,
                     text="🤝  Habilidades Blandas:",
                     font=("Segoe UI", 11, "bold"),
                     text_color=COLORS["texto_principal"]).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(soft_inner,
                     text="  •  ".join(info["soft_skills"]),
                     font=("Segoe UI", 10),
                     text_color=COLORS["texto_secundario"]).pack(side="left")


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 9 — CONSTRUCCIÓN DE LA APP
# ══════════════════════════════════════════════════════════════════════════════

def setup_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=COLORS["fondo_principal"],
                    foreground=COLORS["texto_principal"],
                    rowheight=40,
                    borderwidth=0,
                    font=("Segoe UI", 10))
    style.configure("Custom.Treeview.Heading",
                    background=COLORS["fondo_principal"],
                    foreground=COLORS["texto_principal"],
                    font=("Segoe UI", 10, "bold"),
                    borderwidth=0,
                    relief="flat")
    style.map("Custom.Treeview",
              background=[('selected', COLORS["seleccion"])],
              foreground=[('selected', 'white')])


def build_sidebar(root, header_label, content_frame):
    sidebar = ctk.CTkFrame(root, fg_color=COLORS["primario"], corner_radius=0, width=240)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)

    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        logo_image = ctk.CTkImage(Image.open(logo_path), size=(25, 25))
        _img_refs["logo_sidebar"] = logo_image
        ctk.CTkLabel(sidebar, text=" UROBOROS", image=logo_image,
                     compound="left",
                     font=("Segoe UI", 18, "bold"),
                     text_color="white").pack(pady=(30, 40), padx=20, anchor="w")
    else:
        ctk.CTkLabel(sidebar, text="UROBOROS", font=("Segoe UI", 18, "bold"),
                     text_color="white").pack(pady=(30, 40), padx=20, anchor="w")

    menu_items = {
        "Inicio / Resumen":     ("Resumen de Postulaciones",      lambda: show_inicio(content_frame, root)),
        "Empresas Disponibles": ("Directorio de Empresas (2026)", lambda: show_empresas(content_frame)),
        "Requisitos por Área":  ("Requisitos por Área Académica", lambda: show_requisitos(content_frame)),
    }

    def navigate(titulo, fn):
        """
        Cambia la vista activa y reproduce sonido_clic() como feedback
        auditivo de navegación.
        """
        sonido_clic()                    # ← Sonido suave al navegar entre secciones
        header_label.configure(text=titulo)
        fn()

    for label, (titulo, fn) in menu_items.items():
        ctk.CTkButton(sidebar, text=f"  {label}",
                      fg_color="transparent",
                      text_color="white",
                      hover_color=COLORS["hover"],
                      corner_radius=0,
                      anchor="w",
                      font=("Segoe UI", 12),
                      command=lambda t=titulo, f=fn: navigate(t, f)
                      ).pack(fill="x", pady=2, ipady=8)

    frame_mascota = ctk.CTkFrame(sidebar, fg_color="transparent")
    frame_mascota.pack(side="bottom", fill="x", pady=(0, 10), padx=15)

    ruta_drago = os.path.join("assets", "drago.png")
    if os.path.exists(ruta_drago):
        try:
            img_raw   = Image.open(ruta_drago)
            img_drago = ctk.CTkImage(light_image=img_raw, size=(125, 125))
            _img_refs["drago"] = img_drago
            ctk.CTkLabel(frame_mascota, image=img_drago, text="",
                         fg_color="transparent").pack(anchor="w")
        except Exception:
            ctk.CTkLabel(frame_mascota, text="🐉", font=("Segoe UI", 40),
                         text_color="white").pack(anchor="w")
    else:
        ctk.CTkLabel(frame_mascota, text="🐉", font=("Segoe UI", 40),
                     text_color="white").pack(anchor="w")

    ctk.CTkLabel(frame_mascota, text="v3.0 UROBOROS.System",
                 font=("Segoe UI", 11), text_color="#E0B6BB").pack(anchor="w", pady=(4, 0))


def build_main_container(root):
    main_container = ctk.CTkFrame(root, fg_color="transparent", corner_radius=0)
    main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
    main_container.grid_rowconfigure(1, weight=1)
    main_container.grid_columnconfigure(0, weight=1)

    header_label = ctk.CTkLabel(main_container, text="Panel de Control",
                                 font=("Segoe UI", 24, "bold"),
                                 text_color=COLORS["texto_principal"])
    header_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

    content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
    content_frame.grid(row=1, column=0, sticky="nsew")
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=1)

    return header_label, content_frame


def show_login_screen(root):
    """
    Muestra la pantalla de inicio de sesión.
    Al presionar 'Iniciar Sesión' se reproduce sonido_login() antes de
    destruir el frame y revelar el panel de control.
    """
    login_frame = ctk.CTkFrame(root, fg_color=COLORS["primario"], corner_radius=0)
    login_frame.place(x=0, y=0, relwidth=1, relheight=1)
    login_frame.lift()

    center = ctk.CTkFrame(login_frame, fg_color="transparent")
    center.place(relx=0.5, rely=0.5, anchor="center")

    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        try:
            logo_raw = Image.open(logo_path)
            logo_img = ctk.CTkImage(light_image=logo_raw, size=(110, 110))
            _img_refs["login_logo"] = logo_img
            ctk.CTkLabel(center, image=logo_img, text="", fg_color="transparent").pack(pady=(0, 24))
        except Exception:
            ctk.CTkLabel(center, text="🐉", font=("Segoe UI", 72), text_color="white").pack(pady=(0, 24))
    else:
        ctk.CTkLabel(center, text="🐉", font=("Segoe UI", 72), text_color="white").pack(pady=(0, 24))

    ctk.CTkLabel(center, text="UROBOROS",
                 font=("Impact", 52, "bold"), text_color="white").pack(pady=(0, 48))

    def al_iniciar():
        """
        Reproduce la fanfare de bienvenida y luego destruye la pantalla de login.
        El sonido se ejecuta en un hilo separado para no retrasar la transición.
        """
        sonido_login()          # ← Fanfare de bienvenida al iniciar sesión
        login_frame.destroy()   # Revela el panel de control

    ctk.CTkButton(center, text="Iniciar Sesión",
                  fg_color="#C5B9B9",
                  text_color=COLORS["primario"],
                  hover_color="#29768A",
                  font=("Segoe UI", 16, "bold"),
                  width=220, height=54, corner_radius=10,
                  command=al_iniciar).pack()


# ══════════════════════════════════════════════════════════════════════════════
#  SECCIÓN 10 — PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

def main():
    generar_datos_simulados()

    app = ctk.CTk()
    app.title("UROBOROS - Panel de Control Interactivo")
    app.geometry("1250x700")
    app.minsize(1000, 650)
    app.configure(fg_color=COLORS["fondo_entorno"])

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)

    setup_styles(app)

    header_label, content_frame = build_main_container(app)
    build_sidebar(app, header_label, content_frame)

    show_inicio(content_frame, app)
    show_login_screen(app)

    app.mainloop()


if __name__ == "__main__":
    main()