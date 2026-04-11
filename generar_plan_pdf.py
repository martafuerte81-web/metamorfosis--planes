from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
import json, sys, os

W, H = A4

# ── PALETA VERDE ESMERALDA ───────────────────────────────────────────────────
EM_DARK   = HexColor('#064E3B')
EM_MID    = HexColor('#059669')
EM_BRIGHT = HexColor('#34D399')
EM_PALE   = HexColor('#ECFDF5')
EM_LIGHT  = HexColor('#A7F3D0')
WHITE     = HexColor('#FFFFFF')
BG_ALT    = HexColor('#F4FBF8')
BG_METRIC = HexColor('#F0FAF6')
LINE_COLOR= HexColor('#D1FAE5')
TEXT_DARK = HexColor('#064E3B')
TEXT_MAIN = HexColor('#1A2E25')
TEXT_SUB  = HexColor('#374151')
TEXT_MUTED= HexColor('#6B7280')
CAT_A_BG  = HexColor('#FEF3C7'); CAT_A_TX = HexColor('#78350F')
CAT_B_BG  = HexColor('#DBEAFE'); CAT_B_TX = HexColor('#1E3A8A')
CAT_C_BG  = HexColor('#EDE9FE'); CAT_C_TX = HexColor('#3B0764')
CAT_D_BG  = HexColor('#ECFDF5'); CAT_D_TX = HexColor('#064E3B')

CW = 470.0

def S(name, **kw):
    return ParagraphStyle(name, **kw)

BODY  = S('body',  fontName='Helvetica',      fontSize=9,  leading=15, textColor=TEXT_MAIN, spaceAfter=6, alignment=TA_JUSTIFY)
SMALL = S('small', fontName='Helvetica',      fontSize=8,  leading=12, textColor=TEXT_SUB)
H1    = S('h1',    fontName='Helvetica-Bold', fontSize=20, leading=26, textColor=TEXT_DARK, spaceAfter=6)
H2    = S('h2',    fontName='Helvetica-Bold', fontSize=12, leading=17, textColor=EM_DARK,   spaceBefore=10, spaceAfter=4)
H3    = S('h3',    fontName='Helvetica-Bold', fontSize=10, leading=15, textColor=TEXT_DARK, spaceBefore=6,  spaceAfter=3)
LMOD  = S('lmod',  fontName='Helvetica-Bold', fontSize=9,  leading=13, textColor=EM_MID,    spaceAfter=2)
MVVAL = S('mvval', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=EM_DARK,   alignment=TA_CENTER)
MVLBL = S('mvlbl', fontName='Helvetica',      fontSize=8,  leading=12, textColor=TEXT_SUB,  alignment=TA_CENTER)
TH    = S('th',    fontName='Helvetica-Bold', fontSize=8,  leading=12, textColor=WHITE,     alignment=TA_CENTER)
THL   = S('thl',   fontName='Helvetica-Bold', fontSize=8,  leading=12, textColor=WHITE)
TD    = S('td',    fontName='Helvetica',      fontSize=8,  leading=13, textColor=TEXT_MAIN)
TDB   = S('tdb',   fontName='Helvetica-Bold', fontSize=8,  leading=13, textColor=TEXT_DARK)
TDC   = S('tdc',   fontName='Helvetica',      fontSize=8,  leading=13, textColor=TEXT_MAIN, alignment=TA_CENTER)
TDS   = S('tds',   fontName='Helvetica',      fontSize=7,  leading=11, textColor=TEXT_SUB)

def cover_canvas(c, doc):
    c.saveState()
    # Fondo blanco total
    c.setFillColor(WHITE); c.rect(0,0,W,H,fill=1,stroke=0)
    # Bloque verde oscuro ocupa 55% SUPERIOR
    c.setFillColor(EM_DARK); c.rect(0, H*0.45, W, H*0.55, fill=1, stroke=0)
    # Franja separadora
    c.setFillColor(EM_MID); c.rect(0, H*0.45-4, W, 8, fill=1, stroke=0)
    # Barra izquierda
    c.setFillColor(EM_MID); c.rect(0, 0, 5, H, fill=1, stroke=0)
    # Circulos zona verde
    c.setFillColor(HexColor('#0A6B52')); c.circle(W-30*mm, H*0.78, 50, fill=1, stroke=0)
    c.setFillColor(HexColor('#0D8A69')); c.circle(W-30*mm, H*0.78, 34, fill=1, stroke=0)
    c.setStrokeColor(EM_BRIGHT); c.setLineWidth(1.2)
    c.circle(W-30*mm, H*0.78, 60, fill=0, stroke=1)
    # Decorativo zona blanca
    c.setStrokeColor(EM_LIGHT); c.setLineWidth(0.6)
    c.rect(W-40*mm, 10*mm, 28*mm, 28*mm, fill=0, stroke=1)
    c.rect(W-36*mm, 14*mm, 20*mm, 20*mm, fill=0, stroke=1)
    c.setFont('Helvetica-Bold', 140)
    c.setFillColor(HexColor('#F0FAF6')); c.drawString(W-110, 5*mm, 'P')
    c.restoreState()

def inner_canvas(c, doc):
    c.saveState()
    c.setFillColor(EM_MID); c.rect(0,0,5,H,fill=1,stroke=0)
    c.setFillColor(EM_MID); c.rect(0,H-8*mm,W,2,fill=1,stroke=0)
    c.setFillColor(LINE_COLOR); c.rect(10*mm,12*mm,W-20*mm,0.5,fill=1,stroke=0)
    c.setFont('Helvetica',7); c.setFillColor(TEXT_MUTED)
    c.drawString(22*mm, 7*mm, 'Metamorfosis — Plan Personalizado')
    c.drawRightString(W-16*mm, 7*mm, f'Pagina {doc.page}')
    c.restoreState()

def hr_em(spa=8):
    return HRFlowable(width='100%', thickness=2, color=EM_MID, spaceBefore=2, spaceAfter=spa)

def note_box(text):
    t = Table([[Paragraph(text, S('nt', fontName='Helvetica', fontSize=8,
                leading=13, textColor=TEXT_DARK))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), EM_PALE),
        ('LINEBEFORE',    (0,0),(0,-1),  3, EM_MID),
        ('BOX',           (0,0),(-1,-1), 0.5, EM_LIGHT),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 10),
    ]))
    return t

def metric_cards(items):
    cells = [[Paragraph(v, MVVAL), Paragraph(l, MVLBL)] for v,l in items]
    cw = CW / len(items)
    t = Table([cells], colWidths=[cw]*len(items))
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), BG_METRIC),
        ('BOX',           (0,0),(-1,-1), 1, EM_LIGHT),
        ('LINEAFTER',     (0,0),(-2,-1), 0.5, EM_LIGHT),
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ]))
    return t

def base_ts():
    return [
        ('BACKGROUND',    (0,0),(-1,0),  EM_DARK),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE, BG_ALT]),
        ('TOPPADDING',    (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING',   (0,0),(-1,-1), 6),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
        ('GRID',          (0,0),(-1,-1), 0.4, LINE_COLOR),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ]

def hrow(*cols):
    return [Paragraph(f'<b>{c}</b>', THL if i==0 else TH) for i,c in enumerate(cols)]

def ex_cell(name, mod=''):
    txt = f'<b>{name}</b>'
    if mod: txt += f'<br/><font size="7" color="#374151">{mod}</font>'
    return Paragraph(txt, S('exc', fontName='Helvetica-Bold', fontSize=8, textColor=TEXT_DARK, leading=12))

def ex_table(rows):
    h = hrow('Ejercicio', 'Series x Reps', 'Descanso', 'Clave tecnica')
    t = Table([h]+rows, colWidths=[120, 65, 52, CW-237], repeatRows=1)
    t.setStyle(TableStyle(base_ts()))
    return t

def glb(col, nom, sub):
    return Paragraph(
        f'<font color="{col}"><b>|</b></font>  <b>{nom}</b>  '
        f'<font size="8" color="#4A5568">{sub}</font>',
        S('glb'+nom[:4], fontName='Helvetica', fontSize=9,
          textColor=TEXT_DARK, leading=13, spaceAfter=3))

def get_exercises(nivel, equipo, grupo):
    """Selecciona ejercicios según nivel y equipamiento"""
    ejercicios = {
        'Pecho': {
            'Gimnasio completo':  [('Press de banca con barra','Banco plano, rack'), ('Aperturas pec deck','Maquina o mancuernas')],
            'Home gym basico':    [('Press mancuernas banco','Banco plano'), ('Aperturas mancuernas','Banco plano')],
            'Solo peso corporal': [('Flexiones standard','Manos a anchura hombros'), ('Flexiones diamante','Manos juntas, triceps')],
            'Mixto':              [('Press mancuernas banco','Banco plano'), ('Aperturas pec deck','Si tienes maquina')],
        },
        'Espalda': {
            'Gimnasio completo':  [('Jalon al pecho en polea','Agarre prono ancho'), ('Remo en maquina','Agarre neutro')],
            'Home gym basico':    [('Remo con mancuerna','Apoyo en banco'), ('Jalon con banda','Anclaje alto')],
            'Solo peso corporal': [('Dominadas','Agarre prono o neutro'), ('Remo australiano','Barra a altura cintura')],
            'Mixto':              [('Jalon al pecho en polea','Si tienes polea'), ('Remo con mancuerna','Apoyo en banco')],
        },
        'Hombros': {
            'Gimnasio completo':  [('Press militar barra','Sentado con respaldo'), ('Elevaciones laterales','Mancuernas de pie')],
            'Home gym basico':    [('Press militar mancuernas','Sentado o de pie'), ('Elevaciones laterales','Mancuernas de pie')],
            'Solo peso corporal': [('Pike push-up','Cuerpo en V invertida'), ('Elevaciones laterales','Con botellas de agua')],
            'Mixto':              [('Press militar mancuernas','Sentado o de pie'), ('Elevaciones laterales','Mancuernas de pie')],
        },
        'Triceps': {
            'Gimnasio completo':  [('Fondos en paralelas','Peso corporal o lastrado'), ('Extension polea alta','Cuerda o barra recta')],
            'Home gym basico':    [('Fondos en silla','Manos en borde de silla'), ('Extension sobre cabeza','Mancuerna a dos manos')],
            'Solo peso corporal': [('Fondos en silla','Manos en borde de silla'), ('Flexiones cerradas','Codos pegados al cuerpo')],
            'Mixto':              [('Fondos en paralelas','O en silla si no hay'), ('Extension polea alta','O con banda elastica')],
        },
        'Biceps': {
            'Gimnasio completo':  [('Curl barra Z','De pie'), ('Curl martillo','Mancuernas alterno')],
            'Home gym basico':    [('Curl mancuernas','De pie alterno'), ('Curl martillo','Mancuernas alterno')],
            'Solo peso corporal': [('Curl con mochila','Sentado en suelo'), ('Curl con toalla','En barra o poste')],
            'Mixto':              [('Curl mancuernas','De pie alterno'), ('Curl martillo','Mancuernas alterno')],
        },
        'Cuadriceps': {
            'Gimnasio completo':  [('Sentadilla con barra','Rack con barra libre'), ('Extension cuadriceps','Maquina sentado')],
            'Home gym basico':    [('Goblet squat','Mancuerna o kettlebell'), ('Zancada andando','Mancuernas o sin peso')],
            'Solo peso corporal': [('Sentadilla sumo','Pies separados puntas fuera'), ('Zancada andando','Peso corporal')],
            'Mixto':              [('Goblet squat','Mancuerna o kettlebell'), ('Extension cuadriceps','Si hay maquina')],
        },
        'Femoral': {
            'Gimnasio completo':  [('Peso muerto rumano','Barra libre'), ('Curl femoral maquina','Tumbado o sentado')],
            'Home gym basico':    [('Peso muerto rumano','Mancuernas'), ('Curl femoral con banda','Tumbado boca abajo')],
            'Solo peso corporal': [('Buenos dias','Manos en nuca, bisagra cadera'), ('Curl nórdico','Rodillas fijas en suelo')],
            'Mixto':              [('Peso muerto rumano','Mancuernas o barra'), ('Curl femoral maquina','Si hay maquina')],
        },
        'Gluteo': {
            'Gimnasio completo':  [('Hip thrust con barra','Apoyado en banco'), ('Prensa piernas','Pies altos y separados')],
            'Home gym basico':    [('Hip thrust con mancuerna','Apoyado en sofa o banco'), ('Puente gluteo lastrado','En suelo con mancuerna')],
            'Solo peso corporal': [('Hip thrust peso corporal','Series largas 15-20 rep'), ('Patada trasera de pie','En cuadrupedia o de pie')],
            'Mixto':              [('Hip thrust con mancuerna','Apoyado en banco'), ('Prensa piernas','Si hay maquina')],
        },
    }

    # Ajuste por nivel
    series = '2 x 10-12' if nivel == 'Principiante' else ('3 x 8-12' if nivel == 'Intermedio' else '3-4 x 6-10')
    descanso = '90 seg' if grupo in ['Cuadriceps','Femoral','Gluteo'] else '75 seg'

    equipo_key = equipo if equipo in ejercicios[grupo] else 'Gimnasio completo'
    exs = ejercicios[grupo].get(equipo_key, ejercicios[grupo]['Gimnasio completo'])
    return exs, series, descanso

def calcular_nutricion(datos):
    peso   = float(datos.get('peso', 75) or 75)
    altura = float(datos.get('altura', 170) or 170)
    edad   = int(datos.get('edad', 40) or 40)
    sexo   = datos.get('sexo', 'Hombre')
    objetivo = datos.get('objetivo', 'Perder grasa').lower()
    trabajo  = datos.get('tipoTrabajo', 'Sedentario').lower()
    dias     = int(datos.get('diasEntreno', 4) or 4)

    if 'hombre' in sexo.lower():
        tmb = round(10*peso + 6.25*altura - 5*edad + 5)
    else:
        tmb = round(10*peso + 6.25*altura - 5*edad - 161)

    factor = 1.2 if 'sedent' in trabajo else (1.375 if 'modera' in trabajo else 1.55)
    tdee   = round(tmb * (factor + dias*0.02))

    if 'grasa' in objetivo or 'perder' in objetivo:
        cal_obj = tdee - 400
        prot = round(peso * 1.8)
        carbs_dia_entreno = round((cal_obj * 0.35) / 4)
        carbs_dia_descanso = round((cal_obj * 0.20) / 4)
        grasas = round((cal_obj * 0.25) / 9)
    elif 'musculo' in objetivo or 'ganar' in objetivo:
        cal_obj = tdee + 250
        prot = round(peso * 2.0)
        carbs_dia_entreno = round((cal_obj * 0.40) / 4)
        carbs_dia_descanso = round((cal_obj * 0.30) / 4)
        grasas = round((cal_obj * 0.25) / 9)
    else:
        cal_obj = tdee
        prot = round(peso * 1.7)
        carbs_dia_entreno = round((cal_obj * 0.35) / 4)
        carbs_dia_descanso = round((cal_obj * 0.25) / 4)
        grasas = round((cal_obj * 0.25) / 9)

    imc = round(peso / ((altura/100)**2), 1)
    return {
        'tmb': tmb, 'tdee': tdee, 'cal_obj': cal_obj,
        'proteina': prot, 'grasas': grasas,
        'carbs_entreno': carbs_dia_entreno,
        'carbs_descanso': carbs_dia_descanso,
        'imc': imc,
    }

def menu_semanal(cal_obj, proteina, dieta, excluir):
    """Genera menu semanal con gramajes reales"""
    es_vegetariano = 'vegetariano' in dieta.lower() or 'vegano' in dieta.lower()
    sin_lactosa = 'lactosa' in dieta.lower()
    excluir_lista = [x.strip().lower() for x in excluir.split(',') if x.strip()]

    proteina_fuente = 'Tofu 150g' if es_vegetariano else 'Pechuga de pollo 180g'
    proteina2 = 'Legumbres 200g' if es_vegetariano else 'Merluza 180g'
    lacteo = 'Bebida vegetal 200ml' if sin_lactosa else 'Yogur griego 200g'

    dias_menu = [
        ('Lunes (entreno)',
         f'Desayuno: {lacteo} + avena 60g + platano\nComida: {proteina_fuente} + arroz 80g cocido + ensalada grande\nCena: Huevos 3 uds + verduras salteadas + pan integral 40g'),
        ('Martes (entreno)',
         f'Desayuno: Tortilla 3 huevos + tostada integral 40g + cafe\nComida: {proteina2} + patata 150g + brocoli\nCena: {lacteo} + fruta + nueces 30g'),
        ('Miercoles (descanso)',
         f'Desayuno: {lacteo} + avena 40g\nComida: Lentejas 200g cocidas + verduras + AOVE\nCena: {proteina_fuente.replace("180g","150g")} + ensalada grande + aguacate 60g'),
        ('Jueves (entreno)',
         f'Desayuno: Tortilla 3 huevos + tostada 40g\nComida: {proteina_fuente} + quinoa 70g + espinacas\nCena: Salmon 150g + calabacin + patata pequeña 100g'),
        ('Viernes (entreno)',
         f'Desayuno: {lacteo} + granola 40g + arandanos\nComida: {proteina2} + arroz 80g + judias verdes\nCena: Ternera magra 160g + ensalada + pan integral 30g'),
        ('Sabado (movilidad)',
         f'Desayuno: Tortitas avena 3 huevos + platano\nComida: Garbanzos 200g + verduras + AOVE\nCena: {proteina_fuente.replace("180g","150g")} + ensalada + fruta'),
        ('Domingo (descanso)',
         f'Desayuno: {lacteo} + fruta variada\nComida: Libre dentro del objetivo calorico\nCena: Huevos 2 uds + {proteina2.replace("180g","120g")} + verduras'),
    ]
    return dias_menu

def generar_pdf(datos, output_path):
    n = datos
    nutricion = calcular_nutricion(datos)
    nivel  = n.get('nivel', 'Intermedio')
    equipo = n.get('equipo', 'Gimnasio completo')
    nombre = n.get('nombre', 'Cliente')
    objetivo = n.get('objetivo', 'Perder grasa')
    estres = int(n.get('nivelEstres', 3) or 3)
    sueno  = float(n.get('horasSueno', 7) or 7)
    dias_pref = n.get('diasPreferidos', 'Lunes, Martes, Jueves, Viernes')

    story = []

    class CoverTpl(PageTemplate):
        def __init__(self):
            f = Frame(22*mm, 16*mm, W-38*mm, H-32*mm, id='cover')
            super().__init__(id='cover', frames=[f], onPage=cover_canvas)

    class InnerTpl(PageTemplate):
        def __init__(self):
            f = Frame(22*mm, 18*mm, W-36*mm, H-32*mm, id='inner')
            super().__init__(id='inner', frames=[f], onPage=inner_canvas)

    from reportlab.platypus import NextPageTemplate
    doc = BaseDocTemplate(output_path, pagesize=A4,
                          leftMargin=22*mm, rightMargin=14*mm,
                          topMargin=16*mm, bottomMargin=18*mm)
    doc.addPageTemplates([CoverTpl(), InnerTpl()])

    # ── PORTADA ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    badge = Table([[Paragraph('<b>PLAN PERSONALIZADO — METAMORFOSIS PREMIUM</b>',
                    S('bg', fontName='Helvetica-Bold', fontSize=8,
                      textColor=EM_DARK, alignment=TA_CENTER, leading=11))]],
                  colWidths=[180])
    badge.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), EM_BRIGHT),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 10),
    ]))
    story.append(badge)
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'Plan de',
        S('t1', fontName='Helvetica-Bold', fontSize=42, textColor=WHITE, leading=50, spaceAfter=0)))
    story.append(Paragraph(nombre.split()[0],
        S('t2', fontName='Helvetica-Bold', fontSize=42, textColor=EM_BRIGHT, leading=50, spaceAfter=14)))
    story.append(Paragraph(f'Objetivo: {objetivo}  ·  Nivel: {nivel}',
        S('sub', fontSize=11, textColor=WHITE, leading=18, spaceAfter=6)))
    story.append(HRFlowable(width='35%', thickness=2, color=EM_BRIGHT, spaceBefore=4, spaceAfter=14))

    # Resumen en portada — zona verde, texto blanco
    bs = S('bs', fontSize=10, textColor=WHITE, leading=20)
    for item in [
        f'Calorias objetivo: {nutricion["cal_obj"]} kcal/dia',
        f'Proteina diaria: {nutricion["proteina"]}g/dia',
        f'Peso: {n.get("peso","?")}kg  objetivo: {n.get("pesoObjetivo","?")}kg',
        f'Entreno: {n.get("diasEntreno","?")} dias/semana  {equipo}',
    ]:
        story.append(Paragraph(f'<font color="#34D399"><b>-&gt;</b></font>  {item}', bs))

    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width='100%', thickness=0.5, color=LINE_COLOR, spaceAfter=8))
    story.append(Paragraph(
        f'Generado el {n.get("fechaEnvio","hoy")}  ·  Programa de 16 semanas',
        S('ft', fontSize=8, textColor=TEXT_MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate('inner'))
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    # ── RESUMEN DEL PERFIL ────────────────────────────────────────────────────
    story.append(Paragraph('Tu perfil', LMOD))
    story.append(Paragraph('Resumen y punto de partida', H1))
    story.append(hr_em())
    story.append(metric_cards([
        (str(n.get('peso','?'))+'kg',   'Peso actual'),
        (str(n.get('altura','?'))+'cm', 'Altura'),
        (str(nutricion['imc']),         'IMC'),
        (str(n.get('pesoObjetivo','?'))+'kg', 'Peso objetivo'),
    ]))
    story.append(Spacer(1, 8))
    story.append(metric_cards([
        (str(nutricion['cal_obj']),  'Calorias/dia'),
        (str(nutricion['proteina'])+'g', 'Proteina/dia'),
        (str(nutricion['tdee']),     'Mantenimiento'),
        (str(abs(nutricion['cal_obj']-nutricion['tdee'])), 'Deficit/superavit'),
    ]))
    story.append(Spacer(1, 10))

    # Info adicional
    perfil_data = [
        hrow('Dato', 'Valor', 'Dato', 'Valor'),
        [Paragraph('Nivel', TDB), Paragraph(nivel, TD),
         Paragraph('Equipamiento', TDB), Paragraph(equipo, TD)],
        [Paragraph('Dias entreno', TDB), Paragraph(str(n.get('diasEntreno','?'))+' dias/semana', TD),
         Paragraph('Horario', TDB), Paragraph(n.get('horario','Flexible'), TD)],
        [Paragraph('Nivel estres', TDB), Paragraph(str(estres)+'/5', TD),
         Paragraph('Horas sueno', TDB), Paragraph(str(sueno)+'h/noche', TD)],
        [Paragraph('Dieta', TDB), Paragraph(n.get('dieta','Ninguna'), TD),
         Paragraph('Trabajo', TDB), Paragraph(n.get('tipoTrabajo',''), TD)],
    ]
    pt = Table(perfil_data, colWidths=[70, CW/2-70, 70, CW/2-70])
    pt.setStyle(TableStyle(base_ts()))
    story.append(pt)

    if n.get('lesiones'):
        story.append(Spacer(1,6))
        story.append(note_box(f'<b>Lesiones/limitaciones a tener en cuenta:</b> {n.get("lesiones")}'))

    story.append(PageBreak())

    # ── ENTRENAMIENTO ─────────────────────────────────────────────────────────
    story.append(Paragraph('Modulo 1', LMOD))
    story.append(Paragraph('Plan de Entrenamiento Personalizado', H1))
    story.append(hr_em())

    story.append(Paragraph('Rutina A — Tren superior completo', H2))
    story.append(Paragraph(f'Dias: segun preferencia ({dias_pref})  |  Compuestos grandes primero', SMALL))
    story.append(Spacer(1,6))

    grupos_sup = [
        ('Pecho',    '#1E3A8A', 'empuje horizontal'),
        ('Espalda',  '#059669', 'traccion'),
        ('Hombros',  '#3B0764', 'empuje vertical'),
        ('Triceps',  '#78350F', 'extension de codo'),
        ('Biceps',   '#064E3B', 'flexion de codo'),
    ]
    claves = {
        'Pecho':   ['Omoplatos retraidos. Codos a 75. Rango completo. Bajada 2 seg.',
                    'Movimiento en arco. No bloquees codos. Siente el estiramiento.'],
        'Espalda': ['Ligera inclinacion atras. Barra al pecho alto. Retrae omoplatos.',
                    'Espalda recta. Tira hacia abdomen. Aprieta al final.'],
        'Hombros': ['Core activo. No arquees la lumbar. Bajada controlada 2 seg.',
                    'Codos ligeramente flexionados. Sube a la linea del hombro.'],
        'Triceps': ['Torso inclinado. No bajes mas de 90 si hay molestia.',
                    'Codos pegados al cuerpo. Extension completa.'],
        'Biceps':  ['Codos fijos. No balancees la espalda. Supina muneca al subir.',
                    'Agarre neutro pulgar arriba. Bajada lenta y controlada.'],
    }

    for grupo, color, sub in grupos_sup:
        story.append(glb(color, grupo, sub))
        exs, series, descanso = get_exercises(nivel, equipo, grupo)
        rows = []
        for i, (ex, mod) in enumerate(exs):
            rows.append([ex_cell(ex, mod), Paragraph(series, TDC),
                         Paragraph(descanso, TDC), Paragraph(claves[grupo][i], TD)])
        story.append(ex_table(rows))
        story.append(Spacer(1,6))

    story.append(note_box(
        '<b>Calentamiento Rutina A (5 min):</b> Rotaciones hombro con banda (10 rep cada lado), '
        '10 remos con banda ligera, movilidad toracica. Activa el manguito rotador.'))

    story.append(PageBreak())

    story.append(Paragraph('Rutina B — Tren inferior completo', H2))
    story.append(Paragraph('Descansos mas largos — grupos musculares grandes', SMALL))
    story.append(Spacer(1,6))

    grupos_inf = [
        ('Cuadriceps', '#78350F', 'extension de rodilla'),
        ('Femoral',    '#064E3B', 'flexion de rodilla'),
        ('Gluteo',     '#3B0764', 'extension de cadera'),
    ]
    claves_inf = {
        'Cuadriceps': ['Pies a anchura hombros. Rodillas siguen pies. Hasta paralelo. Espalda neutra.',
                       'Extension completa arriba. Bajada lenta 3 seg. Sin impulso.'],
        'Femoral':    ['Bisagra de cadera no flexion. Barra roza piernas. Para al notar tension.',
                       'Rango completo. Aprieta femoral al final. Bajada controlada 2-3 seg.'],
        'Gluteo':     ['Empuja con talones. Aprieta gluteo arriba. Rodillas a 90. No hiperextiendas.',
                       'Pies en parte alta plataforma. No bloquees rodillas. Descenso controlado.'],
    }

    for grupo, color, sub in grupos_inf:
        story.append(glb(color, grupo, sub))
        exs, series, descanso = get_exercises(nivel, equipo, grupo)
        rows = []
        for i, (ex, mod) in enumerate(exs):
            rows.append([ex_cell(ex, mod), Paragraph(series, TDC),
                         Paragraph(descanso, TDC), Paragraph(claves_inf[grupo][i], TD)])
        story.append(ex_table(rows))
        story.append(Spacer(1,6))

    story.append(note_box(
        '<b>Calentamiento Rutina B (5 min):</b> 10 puentes de gluteo con pausa arriba, '
        'movilidad de cadera, 10 sentadillas sin peso con pausa en el fondo.'))

    story.append(PageBreak())

    # ── NUTRICION ─────────────────────────────────────────────────────────────
    story.append(Paragraph('Modulo 2', LMOD))
    story.append(Paragraph('Plan Nutricional Personalizado', H1))
    story.append(hr_em())

    story.append(Paragraph('Tus numeros exactos', H2))
    story.append(metric_cards([
        (str(nutricion['cal_obj']),  'Calorias objetivo'),
        (str(nutricion['proteina'])+'g', 'Proteina/dia'),
        (str(nutricion['carbs_entreno'])+'g', 'Carbos dia entreno'),
        (str(nutricion['carbs_descanso'])+'g', 'Carbos dia descanso'),
    ]))
    story.append(Spacer(1,8))

    # Distribucion macros
    story.append(Paragraph('Distribucion de macros', H2))
    macro_h = hrow('Macro', 'Dia de entreno', 'Dia de descanso', 'Fuentes principales')
    macro_r = [
        [Paragraph('<b>Proteina</b>', TDB),
         Paragraph(f'{nutricion["proteina"]}g ({round(nutricion["proteina"]*4)} kcal)', TDC),
         Paragraph(f'{nutricion["proteina"]}g — igual siempre', TDC),
         Paragraph('Pollo, huevos, pescado, legumbres, yogur griego', TD)],
        [Paragraph('<b>Carbohidratos</b>', TDB),
         Paragraph(f'{nutricion["carbs_entreno"]}g ({round(nutricion["carbs_entreno"]*4)} kcal)', TDC),
         Paragraph(f'{nutricion["carbs_descanso"]}g (reducidos 30%)', TDC),
         Paragraph('Arroz, avena, patata, pan integral, fruta', TD)],
        [Paragraph('<b>Grasas</b>', TDB),
         Paragraph(f'{nutricion["grasas"]}g ({round(nutricion["grasas"]*9)} kcal)', TDC),
         Paragraph(f'{nutricion["grasas"]}g — igual siempre', TDC),
         Paragraph('AOVE, aguacate, nueces, salmon, yema huevo', TD)],
    ]
    mt = Table([macro_h]+macro_r, colWidths=[70, 100, 120, CW-290])
    mts = base_ts()
    mts[1] = ('ROWBACKGROUNDS',(0,1),(-1,-1),[CAT_B_BG, CAT_C_BG, CAT_A_BG])
    mt.setStyle(TableStyle(mts))
    story.append(mt)
    story.append(Spacer(1,8))

    # Menu semanal
    story.append(Paragraph('Menu semanal con gramajes', H2))
    dieta  = n.get('dieta', 'Ninguna')
    excluir = n.get('alimentosExcluir', '')
    menu = menu_semanal(nutricion['cal_obj'], nutricion['proteina'], dieta, excluir)

    menu_h = hrow('Dia', 'Desayuno', 'Comida', 'Cena')
    menu_rows = []
    for dia, comidas in menu:
        partes = comidas.split('\n')
        desayuno = partes[0].replace('Desayuno: ','') if len(partes)>0 else ''
        comida   = partes[1].replace('Comida: ','')   if len(partes)>1 else ''
        cena     = partes[2].replace('Cena: ','')     if len(partes)>2 else ''
        menu_rows.append([
            Paragraph(f'<b>{dia}</b>', TDS),
            Paragraph(desayuno, TDS),
            Paragraph(comida,   TDS),
            Paragraph(cena,     TDS),
        ])
    cw_menu = [70, (CW-70)/3, (CW-70)/3, (CW-70)/3]
    mt2 = Table([menu_h]+menu_rows, colWidths=cw_menu, repeatRows=1)
    mt2.setStyle(TableStyle(base_ts()))
    story.append(mt2)
    story.append(Spacer(1,6))
    story.append(note_box(
        f'<b>Regla 80/20:</b> Come segun este menu el 80% del tiempo. El 20% restante '
        f'puedes comer fuera del patron sin culpa. Prioriza siempre la proteina en cada comida.'))

    story.append(PageBreak())

    # ── SUPLEMENTACION ────────────────────────────────────────────────────────
    story.append(Paragraph('Modulo 3', LMOD))
    story.append(Paragraph('Suplementacion Recomendada', H1))
    story.append(hr_em())

    supp_h = hrow('Suplemento', 'Dosis', 'Cuando', 'Por que lo necesitas')
    supp_r = [
        [Paragraph('<b>Proteina de suero (Whey)</b>', TDB),
         Paragraph('20-25g por toma', TDC),
         Paragraph('Post-entreno o entre comidas', TD),
         Paragraph(f'Para alcanzar tu objetivo de {nutricion["proteina"]}g/dia de forma practica.', TD)],
        [Paragraph('<b>Creatina monohidrato</b>', TDB),
         Paragraph('3-5g diarios', TDC),
         Paragraph('Cualquier momento, con agua', TD),
         Paragraph('Aumenta fuerza 5-15% y mejora recuperacion entre series. Tarda 3-4 semanas en notarse.', TD)],
        [Paragraph('<b>Vitamina D3 + K2</b>', TDB),
         Paragraph('2000-4000 UI de D3', TDC),
         Paragraph('Con la comida principal', TD),
         Paragraph('Regula testosterona, sistema inmune y absorcion de calcio. 80% adultos tienen deficiencia.', TD)],
    ]
    if estres >= 4:
        supp_r.append([
            Paragraph('<b>Magnesio bisglicinato</b>', TDB),
            Paragraph('300-400mg', TDC),
            Paragraph('Antes de dormir', TD),
            Paragraph(f'Tu nivel de estres es {estres}/5. El magnesio mejora el sueno y reduce el cortisol.', TD),
        ])
    st = Table([supp_h]+supp_r, colWidths=[105, 65, 110, CW-280])
    st.setStyle(TableStyle(base_ts()))
    story.append(st)

    story.append(PageBreak())

    # ── CARDIO ────────────────────────────────────────────────────────────────
    story.append(Paragraph('Modulo 4', LMOD))
    story.append(Paragraph('Cardio Complementario', H1))
    story.append(hr_em())

    story.append(Paragraph('Protocolo semanal integrado con tu entrenamiento', H2))
    cardio_h = hrow('Tipo', 'Frecuencia', 'Duracion', 'Cuando hacerlo', 'Beneficio')
    cardio_r = [
        [Paragraph('<b>LISS</b>\n(cardio suave)', TDB),
         Paragraph('2x semana', TDC), Paragraph('30-40 min', TDC),
         Paragraph('Dias de descanso del entreno de fuerza', TD),
         Paragraph('Quema grasa sin afectar al musculo ni al SNC.', TD)],
        [Paragraph('<b>HIIT</b>\n(intervalos)', TDB),
         Paragraph('1x semana MAX', TDC), Paragraph('20-25 min', TDC),
         Paragraph('Despues del entreno de fuerza o dia separado', TD),
         Paragraph('Mejora capacidad cardiovascular y metabolismo.', TD)],
    ]
    ct = Table([cardio_h]+cardio_r, colWidths=[75, 65, 55, 140, CW-335])
    ct.setStyle(TableStyle(base_ts()))
    story.append(ct)
    story.append(Spacer(1,6))
    story.append(note_box(
        '<b>Regla de oro:</b> El entrenamiento de fuerza es la prioridad. '
        'El cardio es el complemento. Si tienes que elegir entre uno y otro, '
        'elige siempre la sesion de fuerza.'))

    story.append(PageBreak())

    # ── GESTION DEL ESTRES ────────────────────────────────────────────────────
    story.append(Paragraph('Modulo 5', LMOD))
    story.append(Paragraph('Gestion del Estres y Sueno', H1))
    story.append(hr_em())

    prioridad = 'ALTA' if estres >= 4 else ('MEDIA' if estres >= 3 else 'BAJA')
    color_prior = CAT_A_TX if estres >= 4 else (CAT_B_TX if estres >= 3 else CAT_D_TX)
    bg_prior = CAT_A_BG if estres >= 4 else (CAT_B_BG if estres >= 3 else CAT_D_BG)

    prior_t = Table([[
        Paragraph(f'Tu nivel de estres: <b>{estres}/5</b> — Prioridad <b>{prioridad}</b>',
                  S('pr', fontName='Helvetica-Bold', fontSize=10, textColor=color_prior, leading=14)),
        Paragraph(f'Horas de sueno actuales: <b>{sueno}h</b> — Objetivo: <b>7-9h</b>',
                  S('ps', fontName='Helvetica-Bold', fontSize=10, textColor=TEXT_DARK, leading=14,
                    alignment=TA_CENTER)),
    ]], colWidths=[CW/2, CW/2])
    prior_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(0,0), bg_prior),
        ('BACKGROUND',    (1,0),(1,0), BG_METRIC),
        ('BOX',           (0,0),(-1,-1), 0.5, EM_LIGHT),
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
        ('RIGHTPADDING',  (0,0),(-1,-1), 12),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ]))
    story.append(prior_t)
    story.append(Spacer(1,8))

    estres_h = hrow('Tecnica', 'Cuando', 'Duracion', 'Como hacerlo')
    estres_r = [
        [Paragraph('<b>Respiracion diafragmatica</b>', TDB),
         Paragraph('Al despertar y antes de dormir', TD),
         Paragraph('5 min', TDC),
         Paragraph('Inhala 4 seg, retiene 4 seg, exhala 6 seg. 5 ciclos cada vez.', TD)],
        [Paragraph('<b>Ducha fria al final</b>', TDB),
         Paragraph('Despues de la ducha normal', TD),
         Paragraph('60-90 seg', TDC),
         Paragraph('Agua fria los ultimos 60-90 segundos. Reduce cortisol y mejora animo.', TD)],
        [Paragraph('<b>Desconexion digital</b>', TDB),
         Paragraph('30 min antes de dormir', TD),
         Paragraph('30 min diarios', TDC),
         Paragraph('Sin pantallas. Lectura, movilidad suave o simplemente no hacer nada.', TD)],
    ]
    if sueno < 7:
        estres_r.append([
            Paragraph('<b>Protocolo de sueno</b>', TDB),
            Paragraph('Todos los dias, mismo horario', TD),
            Paragraph('Habito diario', TDC),
            Paragraph(f'Actualmente duermes {sueno}h. Objetivo: 7-8h. Acuestate 30 min antes esta semana.', TD),
        ])

    et = Table([estres_h]+estres_r, colWidths=[120, 110, 55, CW-285])
    et.setStyle(TableStyle(base_ts()))
    story.append(et)

    story.append(PageBreak())

    # ── PRIMEROS PASOS ────────────────────────────────────────────────────────
    story.append(Paragraph('Modulo 6', LMOD))
    story.append(Paragraph('Primeros Pasos — Las proximas 48 horas', H1))
    story.append(hr_em())

    actions = [
        ('1', 'Hoy',        'Imprime o guarda este plan',
         'Tenlo accesible en tu movil o impreso. Lo que no se ve, se olvida.'),
        ('2', 'Hoy',        'Compra los suplementos basicos',
         f'Proteina whey y creatina monohidrato. Con {nutricion["proteina"]}g de proteina al dia los necesitaras.'),
        ('3', 'Hoy',        'Haz la lista de la compra del menu',
         'Semana 1: pollo, huevos, yogur griego, arroz, avena, brocoli, aguacate. Sin excusas nutricionales.'),
        ('4', 'Manana',     'Completa tu primera Rutina A',
         f'Con {equipo.lower()}. Sin perfeccion — la primera sesion solo tiene que existir.'),
        ('5', 'Esta semana','Registra tus metricas de inicio',
         'Peso, medidas y una foto. Sin comparaciones — es tu punto de partida personal.'),
    ]

    for num, when, title, body in actions:
        left = Paragraph(
            f'<b>{num}</b><br/><font size="7">{when}</font>',
            S('an'+num, fontName='Helvetica-Bold', fontSize=15,
              textColor=WHITE, alignment=TA_CENTER, leading=19))
        right_t = Table([
            [Paragraph(f'<b>{title}</b>',
                       S('at'+num, fontName='Helvetica-Bold', fontSize=9, textColor=TEXT_DARK, leading=13))],
            [Paragraph(body, S('ab'+num, fontSize=8, textColor=TEXT_SUB, leading=12))],
        ], colWidths=[CW-50])
        right_t.setStyle(TableStyle([
            ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ]))
        act = Table([[left, right_t]], colWidths=[48, CW-50])
        act.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,-1), EM_DARK),
            ('BACKGROUND',(1,0),(1,-1), WHITE),
            ('BOX',(0,0),(-1,-1), 0.5, LINE_COLOR),
            ('TOPPADDING',(0,0),(-1,-1), 9),
            ('BOTTOMPADDING',(0,0),(-1,-1), 9),
            ('LEFTPADDING',(0,0),(-1,-1), 7),
            ('RIGHTPADDING',(0,0),(-1,-1), 8),
            ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
        ]))
        story.append(act)
        story.append(Spacer(1,5))

    story.append(Spacer(1,10))
    story.append(note_box(
        f'<b>Recuerda:</b> Este plan esta disenado especificamente para ti — '
        f'{nombre.split()[0]}, {n.get("edad","?")} anos, {n.get("peso","?")}kg, objetivo: {objetivo}. '
        f'La consistencia importa mas que la perfeccion. Si tienes dudas responde a este email directamente.'))

    # Pagina final
    story.append(PageBreak())
    story.append(Spacer(1, 40*mm))
    story.append(HRFlowable(width='22%', thickness=3, color=EM_MID, spaceAfter=16))
    story.append(Paragraph('Metamorfosis',
        S('ff', fontName='Helvetica-Bold', fontSize=20, textColor=TEXT_DARK,
          leading=26, alignment=TA_CENTER)))
    story.append(Paragraph('Plan Personalizado Premium',
        S('fs', fontSize=10, textColor=TEXT_MUTED, leading=15,
          alignment=TA_CENTER, spaceAfter=16)))
    story.append(Paragraph('Tu programa. Tus resultados.',
        S('fm', fontName='Helvetica-BoldOblique', fontSize=14,
          textColor=EM_MID, leading=20, alignment=TA_CENTER)))

    doc.build(story)
    print(f'PDF generado: {output_path}')

# ── EJECUTAR ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Datos de prueba para verificar el PDF
    datos_prueba = {
        'nombre':           'Roberto Andres',
        'email':            'robertoandrees12@gmail.com',
        'edad':             '22',
        'sexo':             'Hombre',
        'peso':             '88',
        'altura':           '178',
        'pesoObjetivo':     '77',
        'objetivo':         'Perder grasa',
        'nivel':            'Intermedio',
        'equipo':           'Gimnasio completo',
        'diasEntreno':      '3',
        'diasPreferidos':   'Jueves, Miercoles, Domingo',
        'horario':          'Tarde',
        'lesiones':         'no',
        'nivelEstres':      '4',
        'horasSueno':       '7',
        'tipoTrabajo':      'Moderadamente activo',
        'dieta':            'Sin lactosa',
        'alimentosExcluir': 'pescado',
        'comentarios':      '',
        'fechaEnvio':       '11/04/2026',
    }
    generar_pdf(datos_prueba, '/mnt/user-data/outputs/Plan_Personalizado_Ejemplo.pdf')
