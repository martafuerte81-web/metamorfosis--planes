from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor

W, H = A4

EM_DARK    = HexColor('#064E3B')
EM_MID     = HexColor('#059669')
EM_BRIGHT  = HexColor('#34D399')
EM_PALE    = HexColor('#ECFDF5')
EM_LIGHT   = HexColor('#A7F3D0')
WHITE      = HexColor('#FFFFFF')
BG_ALT     = HexColor('#F4FBF8')
BG_METRIC  = HexColor('#F0FAF6')
LINE_COLOR = HexColor('#D1FAE5')
TEXT_DARK  = HexColor('#064E3B')
TEXT_MAIN  = HexColor('#1A2E25')
TEXT_SUB   = HexColor('#374151')
TEXT_MUTED = HexColor('#6B7280')
CAT_A_BG   = HexColor('#FEF3C7'); CAT_A_TX = HexColor('#78350F')
CAT_B_BG   = HexColor('#DBEAFE'); CAT_B_TX = HexColor('#1E3A8A')
CAT_C_BG   = HexColor('#EDE9FE')
CAT_D_BG   = HexColor('#ECFDF5'); CAT_D_TX = HexColor('#064E3B')

CW = 470.0

def S(name, **kw):
    return ParagraphStyle(name, **kw)

H1   = S('h1',  fontName='Helvetica-Bold', fontSize=20, leading=26, textColor=TEXT_DARK, spaceAfter=6)
H2   = S('h2',  fontName='Helvetica-Bold', fontSize=12, leading=17, textColor=EM_DARK, spaceBefore=10, spaceAfter=4)
H3   = S('h3',  fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=EM_MID, spaceBefore=7, spaceAfter=3)
LMOD = S('lmod',fontName='Helvetica-Bold', fontSize=9,  leading=13, textColor=EM_MID, spaceAfter=2)
BODY = S('body',fontName='Helvetica',      fontSize=9,  leading=15, textColor=TEXT_MAIN, spaceAfter=5, alignment=TA_JUSTIFY)
SMALL= S('small',fontName='Helvetica',     fontSize=8,  leading=12, textColor=TEXT_SUB)
BULL = S('bull',fontName='Helvetica',      fontSize=8,  leading=14, textColor=TEXT_MAIN, leftIndent=10, spaceAfter=2)
MVVAL= S('mvval',fontName='Helvetica-Bold',fontSize=18, leading=22, textColor=EM_DARK, alignment=TA_CENTER)
MVLBL= S('mvlbl',fontName='Helvetica',     fontSize=8,  leading=12, textColor=TEXT_SUB, alignment=TA_CENTER)
TH   = S('th',  fontName='Helvetica-Bold', fontSize=8,  leading=12, textColor=WHITE, alignment=TA_CENTER)
THL  = S('thl', fontName='Helvetica-Bold', fontSize=8,  leading=12, textColor=WHITE)
TD   = S('td',  fontName='Helvetica',      fontSize=8,  leading=13, textColor=TEXT_MAIN)
TDB  = S('tdb', fontName='Helvetica-Bold', fontSize=8,  leading=13, textColor=TEXT_DARK)
TDC  = S('tdc', fontName='Helvetica',      fontSize=8,  leading=13, textColor=TEXT_MAIN, alignment=TA_CENTER)
TDS  = S('tds', fontName='Helvetica',      fontSize=7,  leading=11, textColor=TEXT_SUB)

def cover_canvas(c, doc):
    c.saveState()
    c.setFillColor(WHITE); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(EM_DARK); c.rect(0, H*0.45, W, H*0.55, fill=1, stroke=0)
    c.setFillColor(EM_MID); c.rect(0, H*0.45-4, W, 8, fill=1, stroke=0)
    c.setFillColor(EM_MID); c.rect(0, 0, 5, H, fill=1, stroke=0)
    c.setFillColor(HexColor('#0A6B52')); c.circle(W-30*mm, H*0.78, 50, fill=1, stroke=0)
    c.setFillColor(HexColor('#0D8A69')); c.circle(W-30*mm, H*0.78, 34, fill=1, stroke=0)
    c.setStrokeColor(EM_BRIGHT); c.setLineWidth(1.2)
    c.circle(W-30*mm, H*0.78, 60, fill=0, stroke=1)
    c.setStrokeColor(EM_LIGHT); c.setLineWidth(0.6)
    c.rect(W-40*mm, 10*mm, 28*mm, 28*mm, fill=0, stroke=1)
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
    t = Table([[Paragraph(text, S('nt', fontName='Helvetica', fontSize=8, leading=13, textColor=TEXT_DARK))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), EM_PALE),
        ('LINEBEFORE',(0,0),(0,-1), 3, EM_MID),
        ('BOX',(0,0),(-1,-1), 0.5, EM_LIGHT),
        ('TOPPADDING',(0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
        ('RIGHTPADDING',(0,0),(-1,-1), 10),
    ]))
    return t

def info_box(title, text):
    t = Table([[
        Paragraph(f'<b>{title}</b>', S('ibt', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, leading=12)),
        Paragraph(text, S('ibb', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, leading=13)),
    ]], colWidths=[100, CW-100])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), BG_METRIC),
        ('BOX',(0,0),(-1,-1), 0.5, EM_LIGHT),
        ('TOPPADDING',(0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
        ('RIGHTPADDING',(0,0),(-1,-1), 8),
        ('VALIGN',(0,0),(-1,-1), 'TOP'),
    ]))
    return t

def metric_cards(items):
    cells = [[Paragraph(v, MVVAL), Paragraph(l, MVLBL)] for v,l in items]
    cw = CW / len(items)
    t = Table([cells], colWidths=[cw]*len(items))
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), BG_METRIC),
        ('BOX',(0,0),(-1,-1), 1, EM_LIGHT),
        ('LINEAFTER',(0,0),(-2,-1), 0.5, EM_LIGHT),
        ('TOPPADDING',(0,0),(-1,-1), 10),
        ('BOTTOMPADDING',(0,0),(-1,-1), 10),
        ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
    ]))
    return t

def base_ts():
    return [
        ('BACKGROUND',(0,0),(-1,0), EM_DARK),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE, BG_ALT]),
        ('TOPPADDING',(0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LEFTPADDING',(0,0),(-1,-1), 6),
        ('RIGHTPADDING',(0,0),(-1,-1), 6),
        ('GRID',(0,0),(-1,-1), 0.4, LINE_COLOR),
        ('VALIGN',(0,0),(-1,-1), 'TOP'),
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
        f'<font color="{col}"><b>|</b></font>  <b>{nom}</b>  <font size="8" color="#4A5568">{sub}</font>',
        S('glb'+nom[:4], fontName='Helvetica', fontSize=9, textColor=TEXT_DARK, leading=13, spaceAfter=3))

def get_exercises(nivel, equipo, grupo):
    ejercicios = {
        'Pecho': {
            'Gimnasio completo':  [('Press de banca con barra','Banco plano, rack'), ('Aperturas pec deck','Maquina o mancuernas')],
            'Home gym basico':    [('Press mancuernas en banco','Mancuernas + banco plano'), ('Press con banda elastica','Anclaje bajo, simula aperturas')],
            'Solo peso corporal': [('Flexiones standard','Manos a anchura hombros'), ('Flexiones diamante','Manos juntas')],
            'Mixto':              [('Press mancuernas banco','Banco plano'), ('Aperturas pec deck','Si tienes maquina')],
        },
        'Espalda': {
            'Gimnasio completo':  [('Jalon al pecho en polea','Agarre prono ancho'), ('Remo en maquina','Agarre neutro')],
            'Home gym basico':    [('Remo con mancuerna un brazo','Apoyo en banco'), ('Jalon con banda elastica','Anclaje alto en puerta o barra')],
            'Solo peso corporal': [('Dominadas','Agarre prono o neutro'), ('Remo australiano','Barra a altura cintura')],
            'Mixto':              [('Jalon al pecho en polea','Si tienes polea'), ('Remo con mancuerna','Apoyo en banco')],
        },
        'Hombros': {
            'Gimnasio completo':  [('Press militar barra','Sentado con respaldo'), ('Elevaciones laterales','Mancuernas de pie')],
            'Home gym basico':    [('Press militar con mancuernas','Sentado en banco o de pie'), ('Elevaciones laterales con mancuernas','Control total, codos ligeramente flexionados')],
            'Solo peso corporal': [('Pike push-up','Cuerpo en V invertida'), ('Elevaciones laterales','Con botellas de agua')],
            'Mixto':              [('Press militar mancuernas','Sentado o de pie'), ('Elevaciones laterales','Mancuernas de pie')],
        },
        'Triceps': {
            'Gimnasio completo':  [('Fondos en paralelas','Peso corporal o lastrado'), ('Extension polea alta','Cuerda o barra recta')],
            'Home gym basico':    [('Fondos en banco o silla','Manos en el borde, codos atras'), ('Extension de triceps con banda','Banda anclada arriba, codos fijos')],
            'Solo peso corporal': [('Fondos en silla','Manos en borde de silla'), ('Flexiones cerradas','Codos pegados al cuerpo')],
            'Mixto':              [('Fondos en paralelas','O en silla si no hay'), ('Extension polea alta','O con banda elastica')],
        },
        'Biceps': {
            'Gimnasio completo':  [('Curl barra Z','De pie'), ('Curl martillo','Mancuernas alterno')],
            'Home gym basico':    [('Curl de biceps con mancuernas','De pie, alterno, codos fijos'), ('Curl martillo con mancuernas','Agarre neutro, pulgar arriba')],
            'Solo peso corporal': [('Curl con mochila','Sentado en suelo'), ('Curl con toalla','En barra o poste')],
            'Mixto':              [('Curl mancuernas','De pie alterno'), ('Curl martillo','Mancuernas alterno')],
        },
        'Cuadriceps': {
            'Gimnasio completo':  [('Sentadilla con barra','Rack con barra libre'), ('Extension cuadriceps','Maquina sentado')],
            'Home gym basico':    [('Goblet squat con mancuerna','Mancuerna cogida vertical al pecho'), ('Zancada andando con mancuernas','Un paso al frente, rodilla trasera casi al suelo')],
            'Solo peso corporal': [('Sentadilla sumo','Pies separados puntas fuera'), ('Zancada andando','Peso corporal')],
            'Mixto':              [('Goblet squat','Mancuerna o kettlebell'), ('Extension cuadriceps','Si hay maquina')],
        },
        'Femoral': {
            'Gimnasio completo':  [('Peso muerto rumano','Barra libre'), ('Curl femoral maquina','Tumbado o sentado')],
            'Home gym basico':    [('Peso muerto rumano con mancuernas','Bisagra de cadera, espalda neutra'), ('Curl femoral con banda elastica','Tumbado boca abajo, banda en tobillo')],
            'Solo peso corporal': [('Buenos dias','Manos en nuca, bisagra cadera'), ('Curl nordico','Rodillas fijas en suelo')],
            'Mixto':              [('Peso muerto rumano','Mancuernas o barra'), ('Curl femoral maquina','Si hay maquina')],
        },
        'Gluteo': {
            'Gimnasio completo':  [('Hip thrust con barra','Apoyado en banco'), ('Prensa piernas','Pies altos y separados')],
            'Home gym basico':    [('Hip thrust con mancuerna en banco','Hombros apoyados en banco, mancuerna en cadera'), ('Puente de gluteo con mancuerna','En suelo, mancuerna sobre caderas, aprieta arriba')],
            'Solo peso corporal': [('Hip thrust peso corporal','Series largas 15-20 rep'), ('Patada trasera de pie','En cuadrupedia o de pie')],
            'Mixto':              [('Hip thrust con mancuerna','Apoyado en banco'), ('Prensa piernas','Si hay maquina')],
        },
    }
    nivel_norm = nivel.lower().strip()
    if 'principiante' in nivel_norm:
        series = '2 x 12-15'
    elif 'intermedio' in nivel_norm:
        series = '3 x 8-12'
    else:
        series = '3-4 x 6-10'
    descanso = '90 seg' if grupo in ['Cuadriceps','Femoral','Gluteo'] else '75 seg'
    # Normalizar equipamiento con valores exactos del formulario
    equipo_norm = equipo.lower().strip()
    if any(x in equipo_norm for x in ['gym en casa', 'home', 'casa', 'basico']):
        equipo_key = 'Home gym basico'
    elif any(x in equipo_norm for x in ['solo peso', 'peso corporal', 'calistenia']):
        equipo_key = 'Solo peso corporal'
    elif 'mixto' in equipo_norm:
        equipo_key = 'Mixto'
    else:
        equipo_key = 'Gimnasio completo'
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

    sexo_norm = sexo.lower().strip()
    if 'hombre' in sexo_norm or 'masculino' in sexo_norm:
        tmb = round(10*peso + 6.25*altura - 5*edad + 5)
    else:
        tmb = round(10*peso + 6.25*altura - 5*edad - 161)

    trabajo_norm = trabajo.lower().strip()
    if 'sedent' in trabajo_norm:
        factor = 1.2
    elif 'modera' in trabajo_norm:
        factor = 1.375
    elif 'activo' in trabajo_norm:
        factor = 1.55
    else:
        factor = 1.375
    tdee   = round(tmb * (factor + dias*0.02))

    obj_norm = objetivo.lower().strip()
    if any(x in obj_norm for x in ['grasa', 'perder']):
        cal_obj = tdee - 400
        prot = round(peso * 1.8)
        carbs_entreno  = round((cal_obj * 0.38) / 4)
        carbs_descanso = round((cal_obj * 0.22) / 4)
        grasas = round((cal_obj * 0.27) / 9)
    elif any(x in obj_norm for x in ['musculo', 'ganar']):
        cal_obj = tdee + 250
        prot = round(peso * 2.0)
        carbs_entreno  = round((cal_obj * 0.42) / 4)
        carbs_descanso = round((cal_obj * 0.30) / 4)
        grasas = round((cal_obj * 0.25) / 9)
    elif 'ambos' in obj_norm:
        cal_obj = tdee
        prot = round(peso * 1.9)
        carbs_entreno  = round((cal_obj * 0.38) / 4)
        carbs_descanso = round((cal_obj * 0.25) / 4)
        grasas = round((cal_obj * 0.27) / 9)
    else:  # Salud y longevidad
        cal_obj = tdee
        prot = round(peso * 1.7)
        carbs_entreno  = round((cal_obj * 0.38) / 4)
        carbs_descanso = round((cal_obj * 0.28) / 4)
        grasas = round((cal_obj * 0.27) / 9)

    imc = round(peso / ((altura/100)**2), 1)
    return dict(tmb=tmb, tdee=tdee, cal_obj=cal_obj, proteina=prot,
                grasas=grasas, carbs_entreno=carbs_entreno,
                carbs_descanso=carbs_descanso, imc=imc)

def menu_semanal(cal_obj, proteina, dieta, excluir, num_comidas=3):
    """Menu semanal sin gramajes. Solo alimentos. Sin calorias por toma."""
    dieta_norm = dieta.lower().strip()
    es_veg  = any(x in dieta_norm for x in ['vegetariano', 'vegano'])
    sin_lac = 'lactosa' in dieta_norm
    sin_glu = 'gluten' in dieta_norm

    lac   = 'Bebida vegetal' if sin_lac else 'Yogur griego natural'
    prot1 = 'Tofu' if es_veg else 'Pechuga de pollo'
    prot2 = 'Legumbres' if es_veg else 'Merluza o bacalao'
    prot3 = 'Legumbres' if es_veg else 'Salmon'
    prot4 = 'Legumbres' if es_veg else 'Ternera magra'

    usar_merienda = num_comidas >= 4

    dias = [
        ('Lunes (entreno)',
         f'{lac} + avena + platano',
         f'{prot1} + arroz cocido + verduras + AOVE',
         'Fruta + nueces' if usar_merienda else None,
         f'{prot3} + patata cocida + verduras + AOVE'),

        ('Martes (entreno)',
         'Huevos revueltos + tostada integral',
         f'{prot2} + patata cocida + brocoli + AOVE',
         f'{lac} + fruta' if usar_merienda else None,
         f'{prot4} + arroz + ensalada + AOVE'),

        ('Miercoles (descanso)',
         f'{lac} + avena + arandanos',
         f'{prot1} + quinoa + espinacas + AOVE',
         'Fruta + nueces' if usar_merienda else None,
         f'{prot3} + verduras salteadas + aguacate'),

        ('Jueves (entreno)',
         'Huevos revueltos + tostada integral',
         f'{prot1} + arroz cocido + judias verdes + AOVE',
         f'{lac} + fruta' if usar_merienda else None,
         f'{prot3} + boniato + ensalada + AOVE'),

        ('Viernes (entreno)',
         f'{lac} + granola + fruta',
         f'{prot2} + arroz cocido + verduras + AOVE',
         'Fruta + nueces' if usar_merienda else None,
         f'{prot4} + patata + ensalada + AOVE'),

        ('Sabado (movilidad)',
         'Tortitas de avena y huevo + platano + miel',
         f'Legumbres + verduras + AOVE',
         f'{lac} + fruta' if usar_merienda else None,
         f'{prot1} + ensalada grande + aguacate + pan integral'),

        ('Domingo (descanso)',
         f'{lac} + avena + fruta variada',
         'Libre — elige bien',
         'Fruta + nueces' if usar_merienda else None,
         f'Huevos + {prot2} + verduras + AOVE'),
    ]
    return dias


def generar_pdf(datos, output_path):
    n = datos
    nut = calcular_nutricion(datos)
    nivel    = n.get('nivel', 'Intermedio')
    equipo   = n.get('equipo', 'Gimnasio completo')
    nombre   = n.get('nombre', 'Cliente')
    objetivo = n.get('objetivo', 'Perder grasa')
    estres   = int(n.get('nivelEstres', 3) or 3)
    sueno    = float(n.get('horasSueno', 7) or 7)
    dias_p   = n.get('diasPreferidos', 'Lunes, Martes, Jueves, Viernes')

    story = []

    class CoverTpl(PageTemplate):
        def __init__(self):
            f = Frame(22*mm, 16*mm, W-38*mm, H-32*mm, id='cover')
            super().__init__(id='cover', frames=[f], onPage=cover_canvas)

    class InnerTpl(PageTemplate):
        def __init__(self):
            f = Frame(22*mm, 18*mm, W-36*mm, H-32*mm, id='inner')
            super().__init__(id='inner', frames=[f], onPage=inner_canvas)

    from reportlab.platypus import NextPageTemplate, PageBreak
    doc = BaseDocTemplate(output_path, pagesize=A4,
                          leftMargin=22*mm, rightMargin=14*mm,
                          topMargin=16*mm, bottomMargin=18*mm)
    doc.addPageTemplates([CoverTpl(), InnerTpl()])

    # ═══════════════════════════════════════════════════
    # PORTADA
    # ═══════════════════════════════════════════════════
    story.append(Spacer(1, 8*mm))
    badge = Table([[Paragraph('<b>PLAN PERSONALIZADO — METAMORFOSIS PREMIUM</b>',
                    S('bg', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK,
                      alignment=TA_CENTER, leading=11))]], colWidths=[200])
    badge.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), EM_BRIGHT),
        ('TOPPADDING',(0,0),(-1,-1), 5), ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',(0,0),(-1,-1), 10), ('RIGHTPADDING',(0,0),(-1,-1), 10),
    ]))
    story.append(badge)
    story.append(Spacer(1, 12))
    story.append(Paragraph('Plan de', S('t1', fontName='Helvetica-Bold', fontSize=42, textColor=WHITE, leading=50)))
    story.append(Paragraph(nombre.split()[0], S('t2', fontName='Helvetica-Bold', fontSize=42, textColor=EM_BRIGHT, leading=50, spaceAfter=14)))
    story.append(Paragraph(f'Objetivo: {objetivo}  |  Nivel: {nivel}',
        S('sub', fontSize=11, textColor=WHITE, leading=18, spaceAfter=6)))
    story.append(HRFlowable(width='35%', thickness=2, color=EM_BRIGHT, spaceBefore=4, spaceAfter=14))
    bs = S('bs', fontSize=10, textColor=WHITE, leading=20)
    for item in [
        f'Calorias objetivo: {nut["cal_obj"]} kcal/dia',
        f'Proteina diaria: {nut["proteina"]}g/dia',
        f'Peso actual: {n.get("peso","?")}kg  |  Objetivo: {n.get("pesoObjetivo","?")}kg',
        f'Entreno: {n.get("diasEntreno","?")} dias/semana  |  {equipo}',
    ]:
        story.append(Paragraph(f'<font color="#34D399"><b>-&gt;</b></font>  {item}', bs))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width='100%', thickness=0.5, color=LINE_COLOR, spaceAfter=8))
    story.append(Paragraph(f'Generado el {n.get("fechaEnvio","hoy")}  |  Programa de 16 semanas',
        S('ft', fontSize=8, textColor=TEXT_MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate('inner'))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # MODULO 0: RESUMEN DEL PERFIL
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('Tu perfil', LMOD))
    story.append(Paragraph('Resumen y punto de partida', H1))
    story.append(hr_em())
    story.append(metric_cards([
        (str(n.get('peso','?'))+'kg', 'Peso actual'),
        (str(n.get('altura','?'))+'cm', 'Altura'),
        (str(nut['imc']), 'IMC'),
        (str(n.get('pesoObjetivo','?'))+'kg', 'Peso objetivo'),
    ]))
    story.append(Spacer(1, 8))
    story.append(metric_cards([
        (str(nut['cal_obj']), 'Calorias/dia'),
        (str(nut['proteina'])+'g', 'Proteina/dia'),
        (str(nut['tdee']), 'Mantenimiento'),
        (str(abs(nut['cal_obj']-nut['tdee'])), 'Deficit/superavit'),
    ]))
    story.append(Spacer(1, 10))
    perfil_data = [
        hrow('Dato', 'Valor', 'Dato', 'Valor'),
        [Paragraph('Nivel', TDB), Paragraph(nivel, TD), Paragraph('Equipamiento', TDB), Paragraph(equipo, TD)],
        [Paragraph('Dias entreno', TDB), Paragraph(str(n.get('diasEntreno','?'))+' dias/semana', TD),
         Paragraph('Horario', TDB), Paragraph(n.get('horario','Flexible'), TD)],
        [Paragraph('Nivel estres', TDB), Paragraph(str(estres)+'/5', TD),
         Paragraph('Horas de sueño', TDB), Paragraph(str(sueno)+'h/noche', TD)],
        [Paragraph('Dieta', TDB), Paragraph(n.get('dieta','Ninguna'), TD),
         Paragraph('Trabajo', TDB), Paragraph(n.get('tipoTrabajo',''), TD)],
    ]
    pt = Table(perfil_data, colWidths=[70, CW/2-70, 70, CW/2-70])
    pt.setStyle(TableStyle(base_ts()))
    story.append(pt)
    if n.get('lesiones') and str(n.get('lesiones')).lower() not in ['no','ninguna','']:
        story.append(Spacer(1,6))
        story.append(note_box(f'<b>Lesiones/limitaciones:</b> {n.get("lesiones")}'))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # MODULO 1: ENTRENAMIENTO
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('Modulo 1', LMOD))
    story.append(Paragraph('Plan de Entrenamiento Personalizado', H1))
    story.append(hr_em())

    story.append(Paragraph('Rutina A — Tren superior', H2))
    story.append(Paragraph(f'Dias: {dias_p}  |  Orden: compuestos grandes primero', SMALL))
    story.append(Spacer(1,6))

    claves_sup = {
        'Pecho':   ['Omoplatos retraidos. Codos a 75 grados. Bajada 2 seg controlada.',
                    'Movimiento en arco. No bloquees codos arriba. Siente el pectoral.'],
        'Espalda': ['Ligera inclinacion hacia atras. Barra toca el pecho alto. Retrae omoplatos.',
                    'Espalda neutra. Tira del codo hacia la cadera. Aprieta al final.'],
        'Hombros': ['Core activo. No arquees lumbar. Bajada controlada 2 segundos.',
                    'Codos ligeramente flexionados. Sube hasta la linea del hombro.'],
        'Triceps': ['Torso ligeramente inclinado. Para si hay molestia en el codo.',
                    'Codos pegados al cuerpo. Extension completa sin hiperextender.'],
        'Biceps':  ['Codos fijos pegados al cuerpo. No te balancees. Supina la muneca.',
                    'Agarre neutro, pulgar arriba. Bajada lenta y controlada 2 seg.'],
    }
    for grupo, color, sub in [('Pecho','#1E3A8A','empuje horizontal'),('Espalda','#059669','traccion'),
                               ('Hombros','#3B0764','empuje vertical'),('Triceps','#78350F','extension'),
                               ('Biceps','#064E3B','flexion')]:
        story.append(glb(color, grupo, sub))
        exs, series, descanso = get_exercises(nivel, equipo, grupo)
        rows = [[ex_cell(ex, mod), Paragraph(series, TDC), Paragraph(descanso, TDC),
                 Paragraph(claves_sup[grupo][i], TD)] for i,(ex,mod) in enumerate(exs)]
        story.append(ex_table(rows))
        story.append(Spacer(1,5))

    story.append(note_box('<b>Calentamiento Rutina A (5 min):</b> Rotaciones de hombro con banda elastica '
        '(10 rep cada lado), 10 remos con banda ligera, movilidad toracica en el suelo.'))
    story.append(PageBreak())

    story.append(Paragraph('Rutina B — Tren inferior', H2))
    story.append(Paragraph('Descansos mas largos — grupos musculares grandes, mayor demanda metabolica', SMALL))
    story.append(Spacer(1,6))

    claves_inf = {
        'Cuadriceps': ['Pies a anchura de hombros. Rodillas siguen la linea del pie. Hasta paralelo.',
                       'Extension completa arriba. Bajada lenta 3 segundos. Sin impulso.'],
        'Femoral':    ['Bisagra de cadera, no flexion de rodilla. Para al notar tension isquiotibial.',
                       'Rango completo. Aprieta femoral al final. Bajada muy controlada.'],
        'Gluteo':     ['Empuja con los talones. Aprieta gluteo en la parte alta. No hiperextiendas.',
                       'Pies en parte alta. No bloquees rodillas. Descenso controlado 2 seg.'],
    }
    for grupo, color, sub in [('Cuadriceps','#78350F','extension de rodilla'),
                               ('Femoral','#064E3B','flexion de rodilla'),
                               ('Gluteo','#3B0764','extension de cadera')]:
        story.append(glb(color, grupo, sub))
        exs, series, descanso = get_exercises(nivel, equipo, grupo)
        rows = [[ex_cell(ex, mod), Paragraph(series, TDC), Paragraph(descanso, TDC),
                 Paragraph(claves_inf[grupo][i], TD)] for i,(ex,mod) in enumerate(exs)]
        story.append(ex_table(rows))
        story.append(Spacer(1,5))

    story.append(note_box('<b>Calentamiento Rutina B (5 min):</b> 10 puentes de gluteo con pausa arriba, '
        'movilidad de cadera (circulos y apertura lateral), 10 sentadillas sin peso con pausa en el fondo.'))

    story.append(Spacer(1,10))
    story.append(Paragraph('Como organizar tus sesiones semanales', H2))
    story.append(Paragraph(
        'Intercala siempre la Rutina A y la Rutina B — nunca hagas la misma dos dias seguidos. '
        'El dia que no entrenas es cuando el musculo crece y se recupera. '
        'Respeta siempre al menos un dia de descanso entre sesiones del mismo tipo.', BODY))
    story.append(Spacer(1,6))

    dias = int(n.get('diasEntreno', 3) or 3)
    if dias <= 3:
        ejemplo = [
            hrow('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'),
            [Paragraph('<b>Rutina A</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12)),
             Paragraph('<b>Rutina B</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12)),
             Paragraph('<b>Rutina A</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12))],
        ]
    elif dias == 4:
        ejemplo = [
            hrow('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'),
            [Paragraph('<b>Rutina A</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('<b>Rutina B</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12)),
             Paragraph('<b>Rutina A</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('<b>Rutina B</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12))],
        ]
    else:
        ejemplo = [
            hrow('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'),
            [Paragraph('<b>Rutina A</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('<b>Rutina B</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12)),
             Paragraph('<b>Rutina A</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('<b>Rutina B</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('<b>Rutina A</b>', S('tvc', fontName='Helvetica-Bold', fontSize=8, textColor=EM_DARK, alignment=1, leading=12)),
             Paragraph('Descanso', S('tvd', fontName='Helvetica', fontSize=8, textColor=TEXT_SUB, alignment=1, leading=12))],
        ]

    cw_sem = [CW/7]*7
    sem_t = Table(ejemplo, colWidths=cw_sem)
    sem_ts = list(base_ts())
    sem_ts.append(('BACKGROUND',(0,1),(-1,-1), BG_ALT))
    # colorear dias de entreno en verde
    for col in range(7):
        pass
    sem_t.setStyle(TableStyle(sem_ts))
    story.append(sem_t)
    story.append(Spacer(1,6))
    story.append(note_box(
        '<b>Regla de oro:</b> Nunca hagas Rutina A dos dias seguidos ni Rutina B dos dias seguidos. '
        'Siempre intercala. Si un dia no puedes entrenar, no pasa nada — '
        'retoma donde lo dejaste sin intentar recuperar la sesion perdida.'))

    story.append(PageBreak())


    # ═══════════════════════════════════════════════════
    # MODULO CELULITIS PREMIUM (solo mujeres)
    # ═══════════════════════════════════════════════════
    if 'mujer' in n.get('sexo','').lower():
        story.append(Paragraph('Modulo Extra', LMOD))
        story.append(Paragraph('Celulitis: lo que funciona en tu caso especifico', H1))
        story.append(hr_em())

        story.append(Paragraph('Por que aparece y como actua tu programa sobre ella', H2))
        story.append(Paragraph(
        'La celulitis afecta al 85-90% de las mujeres independientemente de su peso. '
        'Es la acumulacion de grasa subcutanea que empuja contra el tejido conectivo, '
        'creando el aspecto de piel de naranja. Factores como la genetica, el estrogeno, '
        'la circulacion y la composicion corporal determinan su intensidad. '
        'Tu plan esta disenado especificamente para atacarla desde varios frentes a la vez.', BODY))
        story.append(Spacer(1,6))

        # Tabla estrategias personalizadas
        cel_h = hrow('Estrategia', 'Como actua', 'En tu plan')
        cel_r = [
        [Paragraph('<b>Fuerza tren inferior</b>', TDB),
        Paragraph('Aumenta la masa muscular bajo la piel mejorando la firmeza en gluteos y muslos', TD),
        Paragraph('Rutina B — Hip thrust, peso muerto rumano, sentadilla sumo', TD)],
        [Paragraph('<b>Deficit moderado</b>', TDB),
        Paragraph('Reduce la grasa total sin sacrificar musculo, mejorando el aspecto de la piel', TD),
        Paragraph(f'Tu deficit de {abs(nut["cal_obj"]-nut["tdee"])} kcal/dia es el ideal', TD)],
        [Paragraph('<b>Nutricion antiinflamatoria</b>', TDB),
        Paragraph('Reducir azucar y sodio disminuye la retencion de liquidos que empeora la apariencia', TD),
        Paragraph('Tu menu semanal elimina ultraprocesados y prioriza alimentos antiinflamatorios', TD)],
        [Paragraph('<b>Hidratacion</b>', TDB),
        Paragraph('Mejora la circulacion y reduce la retencion de liquidos en zonas afectadas', TD),
        Paragraph(f'Objetivo: {round(float(n.get("peso",75) or 75) * 0.035, 1)}L/dia — ajustado a tu peso', TD)],
        [Paragraph('<b>Cardio LISS</b>', TDB),
        Paragraph('Mejora la circulacion sanguinea local y favorece la eliminacion de toxinas', TD),
        Paragraph('2x semana en dias de descanso — incluido en tu plan de cardio', TD)],
        ]
        cel_t = Table([cel_h]+cel_r, colWidths=[100, 190, CW-290])
        cel_t.setStyle(TableStyle(base_ts()))
        story.append(cel_t)
        story.append(Spacer(1,8))

        story.append(note_box(
        '<b>Expectativas reales:</b> Con 8-12 semanas de constancia siguiendo este plan, '
        'la mayoria de mujeres notan una mejora visible en la firmeza y la apariencia de la celulitis. '
        'No desaparece al 100% — ningun metodo lo consigue — pero se reduce de forma significativa '
        'y la piel gana firmeza real gracias al aumento de masa muscular.'))
        story.append(PageBreak())


    # ═══════════════════════════════════════════════════
    # MODULO 2: NUTRICION
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('Modulo 2', LMOD))
    story.append(Paragraph('Plan Nutricional con Gramajes Reales', H1))
    story.append(hr_em())

    story.append(Paragraph('Tus numeros exactos', H2))
    story.append(metric_cards([
        (str(nut['cal_obj']), 'Calorias objetivo'),
        (str(nut['proteina'])+'g', 'Proteina/dia'),
        (str(nut['carbs_entreno'])+'g', 'Carbos entreno'),
        (str(nut['carbs_descanso'])+'g', 'Carbos descanso'),
    ]))
    story.append(Spacer(1,8))

    story.append(Paragraph('Distribucion de macros', H2))
    macro_h = hrow('Macro', 'Dia entreno', 'Dia descanso', 'Fuentes recomendadas')
    macro_r = [
        [Paragraph('<b>Proteina</b>', TDB),
         Paragraph(f'{nut["proteina"]}g  ({round(nut["proteina"]*4)} kcal)', TDC),
         Paragraph(f'{nut["proteina"]}g — igual siempre', TDC),
         Paragraph('Pollo, huevos, pescado, legumbres, yogur griego, whey', TD)],
        [Paragraph('<b>Carbohidratos</b>', TDB),
         Paragraph(f'{nut["carbs_entreno"]}g  ({round(nut["carbs_entreno"]*4)} kcal)', TDC),
         Paragraph(f'{nut["carbs_descanso"]}g  (reducidos)', TDC),
         Paragraph('Arroz, avena, patata, boniato, pan integral, fruta', TD)],
        [Paragraph('<b>Grasas</b>', TDB),
         Paragraph(f'{nut["grasas"]}g  ({round(nut["grasas"]*9)} kcal)', TDC),
         Paragraph(f'{nut["grasas"]}g — igual siempre', TDC),
         Paragraph('AOVE, aguacate, nueces, salmon, yema de huevo', TD)],
    ]
    mt = Table([macro_h]+macro_r, colWidths=[70, 100, 115, CW-285])
    mts = base_ts()
    mts[1] = ('ROWBACKGROUNDS',(0,1),(-1,-1),[CAT_B_BG, CAT_C_BG, CAT_A_BG])
    mt.setStyle(TableStyle(mts))
    story.append(mt)
    story.append(Spacer(1,8))

    story.append(Paragraph('Menu semanal — 4 comidas, gramajes exactos para ' + str(nut['cal_obj']) + ' kcal/dia', H2))
    dieta_v   = n.get('dieta', 'Ninguna')
    excluir_v = n.get('alimentosExcluir', '')
    num_comidas = 4
    menu = menu_semanal(nut['cal_obj'], nut['proteina'], dieta_v, excluir_v, num_comidas)

    usar_merienda = num_comidas >= 4
    if usar_merienda:
        menu_h = hrow('Dia', 'Desayuno', 'Comida', 'Merienda', 'Cena')
    else:
        menu_h = hrow('Dia', 'Desayuno', 'Comida', 'Cena')
    menu_rows = []
    for entry in menu:
        dia, desa, comi, meri, cena = entry
        if usar_merienda:
            menu_rows.append([
                Paragraph(f'<b>{dia}</b>', TDS),
                Paragraph(desa or '', TDS),
                Paragraph(comi or '', TDS),
                Paragraph(meri or '', TDS),
                Paragraph(cena or '', TDS),
            ])
        else:
            menu_rows.append([
                Paragraph(f'<b>{dia}</b>', TDS),
                Paragraph(desa or '', TDS),
                Paragraph(comi or '', TDS),
                Paragraph(cena or '', TDS),
            ])
    if usar_merienda:
        cw_m = [55, (CW-55)/4, (CW-55)/4, (CW-55)/4, (CW-55)/4]
    else:
        cw_m = [55, (CW-55)/3, (CW-55)/3, (CW-55)/3]
    mt2 = Table([menu_h]+menu_rows, colWidths=cw_m, repeatRows=1)
    mt2.setStyle(TableStyle(base_ts()))
    story.append(mt2)
    story.append(Spacer(1,6))
    story.append(note_box(
        f'<b>Como calcular tus porciones:</b> Usa MyFitnessPal (gratis) para pesar y registrar '
        f'cada alimento hasta alcanzar las calorias de cada toma. Tu objetivo diario es '
        f'{nut["cal_obj"]} kcal con {nut["proteina"]}g de proteina. '
        f'En dias de entreno prioriza mas carbohidratos. En dias de descanso reducellos un 30%.'))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # MODULO 3: SUPLEMENTACION
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('Modulo 3', LMOD))
    story.append(Paragraph('Suplementacion Recomendada', H1))
    story.append(hr_em())

    supp_h = hrow('Suplemento', 'Dosis', 'Momento', 'Por que lo necesitas')
    supp_r = [
        [Paragraph('<b>Proteina de suero (Whey)</b>', TDB), Paragraph('20-25g', TDC),
         Paragraph('Post-entreno o entre comidas', TD),
         Paragraph(f'Herramienta para alcanzar {nut["proteina"]}g/dia sin comer pollo 5 veces.', TD)],
        [Paragraph('<b>Creatina monohidrato</b>', TDB), Paragraph('3-5g diarios', TDC),
         Paragraph('Cualquier momento del dia', TD),
         Paragraph('El suplemento mas estudiado. Aumenta fuerza 5-15% y mejora recuperacion entre series.', TD)],
        [Paragraph('<b>Vitamina D3 + K2</b>', TDB), Paragraph('2000-4000 UI D3', TDC),
         Paragraph('Con la comida principal', TD),
         Paragraph('Mas del 80% de adultos tiene deficiencia. Clave para testosterona, inmunidad y huesos.', TD)],
        [Paragraph('<b>Omega-3 (EPA+DHA)</b>', TDB), Paragraph('2-3g diarios', TDC),
         Paragraph('Con las comidas', TD),
         Paragraph('Reduce inflamacion, mejora recuperacion muscular y salud cardiovascular.', TD)],
    ]
    if estres >= 4:
        supp_r.append([Paragraph('<b>Magnesio bisglicinato</b>', TDB), Paragraph('300-400mg', TDC),
            Paragraph('Antes de dormir', TD),
            Paragraph(f'Tu nivel de estres es {estres}/5. El magnesio mejora el sueño y reduce el cortisol nocturno.', TD)])
    st = Table([supp_h]+supp_r, colWidths=[110, 60, 105, CW-275])
    st.setStyle(TableStyle(base_ts()))
    story.append(st)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # MODULO 4: CARDIO
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('Modulo 4', LMOD))
    story.append(Paragraph('Cardio Complementario', H1))
    story.append(hr_em())

    cardio_h = hrow('Tipo', 'Frecuencia', 'Duracion', 'Cuando', 'Beneficio')
    cardio_r = [
        [Paragraph('<b>LISS</b>\n(baja intensidad)', TDB), Paragraph('2x semana', TDC),
         Paragraph('30-40 min', TDC), Paragraph('Dias de descanso del entrenamiento de fuerza', TD),
         Paragraph('Quema grasa sin afectar al musculo ni agotar el sistema nervioso.', TD)],
        [Paragraph('<b>HIIT</b>\n(intervalos)', TDB), Paragraph('1x semana MAX', TDC),
         Paragraph('20-25 min', TDC), Paragraph('Despues del entrenamiento de fuerza, nunca antes', TD),
         Paragraph('Mejora capacidad cardiovascular y sube el metabolismo basal.', TD)],
        [Paragraph('<b>Pasos diarios</b>', TDB), Paragraph('Diario', TDC),
         Paragraph('7.000-10.000 pasos', TDC), Paragraph('A lo largo del dia, de forma acumulada', TD),
         Paragraph('El habito de movimiento mas sencillo y efectivo para quemar calorias sin fatiga.', TD)],
    ]
    ct = Table([cardio_h]+cardio_r, colWidths=[75, 65, 60, 130, CW-330])
    ct.setStyle(TableStyle(base_ts()))
    story.append(ct)
    story.append(Spacer(1,6))
    story.append(note_box('<b>Regla de oro:</b> La fuerza es la prioridad. El cardio es el complemento. '
        'Nunca hagas cardio intenso antes de una sesion de fuerza. Siempre despues o en dia separado.'))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # MODULO 5: GESTION DEL ESTRES Y SUENO
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('Modulo 5', LMOD))
    story.append(Paragraph('Gestion del Estres y Descanso', H1))
    story.append(hr_em())

    prior_color = CAT_A_TX if estres >= 4 else (CAT_B_TX if estres >= 3 else CAT_D_TX)
    prior_bg    = CAT_A_BG if estres >= 4 else (CAT_B_BG if estres >= 3 else CAT_D_BG)
    prioridad   = 'ALTA' if estres >= 4 else ('MEDIA' if estres >= 3 else 'BAJA')

    prior_t = Table([[
        Paragraph(f'Nivel de estres: <b>{estres}/5</b> — Prioridad <b>{prioridad}</b>',
                  S('pr', fontName='Helvetica-Bold', fontSize=10, textColor=prior_color, leading=14)),
        Paragraph(f'Horas de sueño: <b>{sueno}h</b> — Objetivo: <b>7-9h</b>',
                  S('ps', fontName='Helvetica-Bold', fontSize=10, textColor=TEXT_DARK, leading=14, alignment=TA_CENTER)),
    ]], colWidths=[CW/2, CW/2])
    prior_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0), prior_bg), ('BACKGROUND',(1,0),(1,0), BG_METRIC),
        ('BOX',(0,0),(-1,-1), 0.5, EM_LIGHT),
        ('TOPPADDING',(0,0),(-1,-1), 10), ('BOTTOMPADDING',(0,0),(-1,-1), 10),
        ('LEFTPADDING',(0,0),(-1,-1), 12), ('RIGHTPADDING',(0,0),(-1,-1), 12),
        ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
    ]))
    story.append(prior_t)
    story.append(Spacer(1,8))

    estres_h = hrow('Tecnica', 'Cuando', 'Duracion', 'Como hacerlo')
    estres_r = [
        [Paragraph('<b>Respiracion 4-4-6</b>', TDB), Paragraph('Al despertar y al dormir', TD),
         Paragraph('5 min', TDC), Paragraph('Inhala 4 seg, retiene 4 seg, exhala 6 seg. 5 ciclos minimo.', TD)],
        [Paragraph('<b>Ducha fria final</b>', TDB), Paragraph('Despues de la ducha normal', TD),
         Paragraph('60-90 seg', TDC), Paragraph('Agua fria los ultimos 60-90 segundos. Reduce cortisol y mejora el animo.', TD)],
        [Paragraph('<b>Desconexion digital</b>', TDB), Paragraph('30 min antes de dormir', TD),
         Paragraph('30 min diarios', TDC), Paragraph('Sin pantallas. Lectura, movilidad suave o silencio activo.', TD)],
        [Paragraph('<b>Rutina de sueño</b>', TDB), Paragraph('Todos los dias, mismo horario', TD),
         Paragraph('Habito diario', TDC),
         Paragraph(f'Actualmente duermes {sueno}h. Objetivo: 7-8h. Acuestate 20 min antes esta semana.', TD)],
    ]
    et = Table([estres_h]+estres_r, colWidths=[115, 110, 55, CW-280])
    et.setStyle(TableStyle(base_ts()))
    story.append(et)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # MODULO 6: FUNDAMENTOS
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('Modulo 6', LMOD))
    story.append(Paragraph('Fundamentos — Por que funciona este sistema', H1))
    story.append(hr_em())

    story.append(Paragraph('Por que el entrenamiento de fuerza es prioritario', H2))
    story.append(Paragraph(
        'El entrenamiento de fuerza es la herramienta mas poderosa que existe para transformar tu cuerpo '
        'despues de los 35 anos. Cuando entrenas con carga, provocas un dano muscular controlado. '
        'Durante la recuperacion, el cuerpo repara ese tejido y lo hace mas grande y fuerte. '
        'Pero hay un beneficio mas importante a largo plazo: el musculo es metabolicamente activo. '
        'Cada kilo de musculo que ganas quema entre 13 y 20 calorias adicionales cada dia en reposo. '
        'Esto significa que con mas masa muscular puedes comer mas, perder grasa con mayor facilidad '
        'y mantener los resultados sin pasar hambre.', BODY))
    story.append(Spacer(1,6))

    fund_data = [
        hrow('Principio', 'Que significa', 'Como lo aplicamos'),
        [Paragraph('<b>Sobrecarga progresiva</b>', TDB),
         Paragraph('Cada semana el estimulo debe ser ligeramente mayor que el anterior', TD),
         Paragraph('Aumenta peso, reps o series cada 1-2 semanas. El cuerpo se adapta y crece.', TD)],
        [Paragraph('<b>Especificidad</b>', TDB),
         Paragraph('El cuerpo mejora en aquello para lo que lo entrenas', TD),
         Paragraph('Rutinas A y B con ejercicios multiarticulares que trabajan todo el cuerpo.', TD)],
        [Paragraph('<b>Recuperacion</b>', TDB),
         Paragraph('El crecimiento muscular ocurre fuera del gimnasio, no dentro', TD),
         Paragraph('Dias de descanso obligatorios, sueño de 7-8h y nutricion adecuada.', TD)],
        [Paragraph('<b>Consistencia</b>', TDB),
         Paragraph('Los resultados son la suma de sesiones a lo largo del tiempo', TD),
         Paragraph('3-5 dias/semana durante 16 semanas supera cualquier programa perfecto de 3 semanas.', TD)],
    ]
    ft = Table(fund_data, colWidths=[110, 160, CW-270])
    ft.setStyle(TableStyle(base_ts()))
    story.append(ft)
    story.append(Spacer(1,10))

    story.append(Paragraph('Por que la proteina lo cambia todo', H2))
    story.append(Paragraph(
        'La proteina es el macronutriente mas importante cuando el objetivo es cambiar la composicion corporal. '
        'Sus aminoacidos son la materia prima con la que el cuerpo construye y repara el tejido muscular. '
        f'Tu objetivo de {nut["proteina"]}g/dia puede parecer mucho, pero es la cantidad minima necesaria '
        'para maximizar la sintesis proteica muscular despues del entrenamiento. '
        'Ademas, la proteina tiene el mayor efecto termico de los tres macros: el cuerpo gasta entre un '
        '20-30% de las calorias de la proteina solo en digerirla. Esto significa que con una dieta alta '
        'en proteina quemas mas calorias sin hacer nada adicional.', BODY))
    story.append(Spacer(1,6))

    prot_data = [
        hrow('Fuente', 'Proteina/100g', 'Calorias/100g', 'Cuando usarla'),
        [Paragraph('Pechuga de pollo', TD), Paragraph('31g', TDC), Paragraph('165 kcal', TDC), Paragraph('Comidas principales. Versatil y barata.', TD)],
        [Paragraph('Claras de huevo', TD), Paragraph('11g', TDC), Paragraph('52 kcal', TDC), Paragraph('Desayuno. Muy bajas en calorias.', TD)],
        [Paragraph('Huevo entero', TD), Paragraph('13g', TDC), Paragraph('155 kcal', TDC), Paragraph('Desayuno y cenas. Rico en micronutrientes.', TD)],
        [Paragraph('Merluza / bacalao', TD), Paragraph('20g', TDC), Paragraph('90 kcal', TDC), Paragraph('Comidas ligeras. Muy bajo en calorias.', TD)],
        [Paragraph('Salmon', TD), Paragraph('20g', TDC), Paragraph('140 kcal', TDC), Paragraph('2x semana. Aporta Omega-3 esencial.', TD)],
        [Paragraph('Yogur griego natural', TD), Paragraph('10g', TDC), Paragraph('95 kcal', TDC), Paragraph('Desayuno y snacks. Facil y rapido.', TD)],
        [Paragraph('Proteina de suero (whey)', TD), Paragraph('80g', TDC), Paragraph('380 kcal', TDC), Paragraph('Post-entreno. La forma mas eficiente.', TD)],
        [Paragraph('Legumbres (lentejas)', TD), Paragraph('9g', TDC), Paragraph('116 kcal', TDC), Paragraph('Fuente vegetal rica en carbos y fibra.', TD)],
    ]
    prt = Table(prot_data, colWidths=[115, 80, 80, CW-275])
    prt.setStyle(TableStyle(base_ts()))
    story.append(prt)
    story.append(Spacer(1,10))

    story.append(Paragraph('Los carbohidratos no son el enemigo', H2))
    story.append(Paragraph(
        'Los carbohidratos son el combustible preferido del musculo durante el entrenamiento. '
        'Reducirlos en exceso perjudica el rendimiento, la recuperacion y el estado de animo. '
        'La clave no es eliminarlos sino elegir los correctos y consumirlos en el momento adecuado. '
        'Los carbohidratos de calidad —arroz, avena, patata, fruta— te dan energia sostenida y '
        'rellenan el glucogeno muscular para que el siguiente entreno sea igual de bueno. '
        'La diferencia entre un dia de entreno y uno de descanso en cuanto a carbos no es capricho: '
        'en los dias de entreno necesitas mas energia, en los de descanso el cuerpo requiere menos.', BODY))
    story.append(Spacer(1,6))

    carb_data = [
        hrow('Fuente', 'Carbos/100g', 'Calorias/100g', 'Cuando usarla'),
        [Paragraph('Arroz blanco o integral cocido', TD), Paragraph('28g', TDC), Paragraph('130 kcal', TDC), Paragraph('Comidas pre y post-entreno. De referencia.', TD)],
        [Paragraph('Avena', TD), Paragraph('60g', TDC), Paragraph('379 kcal', TDC), Paragraph('Desayuno. Absorcion lenta, energia sostenida.', TD)],
        [Paragraph('Patata cocida', TD), Paragraph('17g', TDC), Paragraph('80 kcal', TDC), Paragraph('Comidas principales. Saciante y digestiva.', TD)],
        [Paragraph('Boniato / batata', TD), Paragraph('20g', TDC), Paragraph('90 kcal', TDC), Paragraph('Alternativa a la patata. Rico en betacarotenos.', TD)],
        [Paragraph('Pan integral', TD), Paragraph('41g', TDC), Paragraph('250 kcal', TDC), Paragraph('Desayuno y cenas. Elige siempre integral.', TD)],
        [Paragraph('Fruta (platano)', TD), Paragraph('23g', TDC), Paragraph('89 kcal', TDC), Paragraph('Pre-entreno. Energia rapida y potasio.', TD)],
    ]
    crt = Table(carb_data, colWidths=[130, 70, 80, CW-280])
    crt.setStyle(TableStyle(base_ts()))
    story.append(crt)
    story.append(Spacer(1,10))

    story.append(Paragraph('Las grasas saludables y su papel hormonal', H2))
    story.append(Paragraph(
        'Las grasas son fundamentales para la produccion de hormonas, incluyendo la testosterona. '
        'Una dieta muy baja en grasas puede reducir los niveles de testosterona hasta un 15%, '
        'lo que afecta directamente a la capacidad de ganar musculo y perder grasa. '
        'El secreto esta en elegir las grasas correctas: aceite de oliva virgen extra, aguacate, '
        'nueces, salmon y yema de huevo. Evita las grasas trans presentes en productos ultraprocesados.', BODY))
    story.append(Spacer(1,6))

    gras_data = [
        hrow('Fuente', 'Grasas/100g', 'Calorias/100g', 'Beneficio principal'),
        [Paragraph('AOVE (aceite de oliva)', TD), Paragraph('100g', TDC), Paragraph('884 kcal', TDC), Paragraph('Antiinflamatorio. Base de la dieta mediterranea.', TD)],
        [Paragraph('Aguacate', TD), Paragraph('15g', TDC), Paragraph('160 kcal', TDC), Paragraph('Rico en potasio y vitamina E. Muy saciante.', TD)],
        [Paragraph('Nueces', TD), Paragraph('65g', TDC), Paragraph('654 kcal', TDC), Paragraph('Omega-3 vegetal. Buenas para el sistema nervioso.', TD)],
        [Paragraph('Salmon', TD), Paragraph('13g', TDC), Paragraph('140 kcal', TDC), Paragraph('EPA y DHA directos. Los mejores Omega-3.', TD)],
        [Paragraph('Yema de huevo', TD), Paragraph('27g', TDC), Paragraph('322 kcal', TDC), Paragraph('Vitaminas liposolubles A, D, E, K y colina.', TD)],
    ]
    grt = Table(gras_data, colWidths=[120, 70, 80, CW-270])
    grt.setStyle(TableStyle(base_ts()))
    story.append(grt)
    story.append(PageBreak())

    story.append(Paragraph('Como funciona la perdida de grasa de verdad', H2))
    story.append(Paragraph(
        'La perdida de grasa no ocurre porque "quemes calorias durante el ejercicio". '
        'Un entreno de 60 minutos quema entre 300 y 500 calorias, lo mismo que una hamburguesa. '
        'El entrenamiento de fuerza funciona porque eleva el metabolismo basal durante 24-48 horas '
        'despues de la sesion (efecto EPOC) y porque cada kilo de musculo ganado consume entre '
        '13 y 20 calorias adicionales cada dia en reposo. '
        'La perdida de grasa real es el resultado de un deficit calorico mantenido en el tiempo. '
        f'Tu deficit actual es de {abs(nut["cal_obj"]-nut["tdee"])} kcal/dia, lo que equivale '
        f'a entre 200 y 400 gramos de grasa pura perdida por semana. Lento pero permanente.', BODY))
    story.append(Spacer(1,6))
    story.append(note_box(
        '<b>Regla de las 4 semanas:</b> Las primeras 2 semanas perdes principalmente agua y glucogeno. '
        'La grasa real empieza a moverse a partir de la semana 3-4. No abandones antes de ver resultados reales.'))
    story.append(Spacer(1,10))

    story.append(Paragraph('La hormona que lo controla todo: el cortisol', H2))
    story.append(Paragraph(
        'El cortisol es la hormona del estres. En niveles normales es util: te da energia por la manana, '
        'moviliza grasa como combustible y regula la inflamacion. El problema aparece cuando el estres '
        'es cronico y el cortisol permanece elevado. En ese estado el cuerpo entra en modo supervivencia: '
        'almacena grasa abdominal, degrada musculo para obtener energia rapida y aumenta el apetito. '
        f'Tu nivel de estres es {estres}/5. '
        + ('Este es un factor critico que hay que gestionar activamente.' if estres >= 4
           else 'Estas en un nivel manejable, pero siempre hay margen de mejora.'), BODY))
    story.append(Spacer(1,6))
    cortisol_data = [
        hrow('Eleva el cortisol', 'Reduce el cortisol'),
        [Paragraph('Dormir menos de 6 horas', TD), Paragraph('Dormir 7-8 horas de forma consistente', TD)],
        [Paragraph('Cardio excesivo (mas de 5h semanales)', TD), Paragraph('Entrenamiento de fuerza moderado', TD)],
        [Paragraph('Deficit calorico muy agresivo (-800 kcal)', TD), Paragraph('Deficit moderado como el tuyo (-400 kcal)', TD)],
        [Paragraph('Estres laboral o personal cronico', TD), Paragraph('Respiracion diafragmatica diaria', TD)],
        [Paragraph('Cafeina en exceso (mas de 400mg/dia)', TD), Paragraph('Magnesio bisglicinato antes de dormir', TD)],
        [Paragraph('Pantallas y redes sociales nocturnas', TD), Paragraph('Desconexion digital 30 min antes de dormir', TD)],
    ]
    cort = Table(cortisol_data, colWidths=[CW/2, CW/2])
    cort.setStyle(TableStyle(base_ts()))
    story.append(cort)
    story.append(Spacer(1,10))

    story.append(Paragraph('Progresion: el principio mas ignorado en el gimnasio', H2))
    story.append(Paragraph(
        'El mayor error en el gimnasio es hacer siempre lo mismo. '
        'El cuerpo se adapta en 2-3 semanas a cualquier estimulo. Cuando eso ocurre, deja de progresar. '
        'La sobrecarga progresiva es la solucion: cada semana, el estimulo debe ser ligeramente mayor. '
        'No hace falta subir peso en cada sesion — hay multiples formas de progresar:', BODY))
    story.append(Spacer(1,4))
    prog_data = [
        hrow('Forma de progresar', 'Ejemplo practico', 'Cuando usarla'),
        [Paragraph('<b>Aumentar el peso</b>', TDB),
         Paragraph('Pasar de 60kg a 62.5kg en press de banca', TD),
         Paragraph('Cuando completas todas las series con las reps previstas', TD)],
        [Paragraph('<b>Aumentar las repeticiones</b>', TDB),
         Paragraph('Pasar de 3x8 a 3x10 con el mismo peso', TD),
         Paragraph('Cuando el peso esta fijo y hay margen de reps', TD)],
        [Paragraph('<b>Aumentar las series</b>', TDB),
         Paragraph('Pasar de 3 a 4 series en un ejercicio', TD),
         Paragraph('Cuando no puedes subir peso ni reps todavia', TD)],
        [Paragraph('<b>Reducir el descanso</b>', TDB),
         Paragraph('Pasar de 90 a 75 segundos entre series', TD),
         Paragraph('Para aumentar la densidad del entrenamiento', TD)],
        [Paragraph('<b>Mejorar la tecnica</b>', TDB),
         Paragraph('Mayor rango de movimiento, contraccion mas intensa', TD),
         Paragraph('Especialmente en las primeras semanas del programa', TD)],
    ]
    progt = Table(prog_data, colWidths=[110, 170, CW-280])
    progt.setStyle(TableStyle(base_ts()))
    story.append(progt)
    story.append(Spacer(1,10))

    story.append(Paragraph('Hidratacion: el nutriente mas olvidado', H2))
    story.append(Paragraph(
        'El agua no tiene calorias pero tiene un impacto enorme en el rendimiento y la composicion corporal. '
        'Una deshidratacion del 2% reduce la fuerza muscular hasta un 10% y el rendimiento cognitivo un 20%. '
        'El agua es necesaria para transportar nutrientes a las celulas musculares, eliminar desechos '
        'metabolicos y el funcionamiento optimo del higado, organo clave en la oxidacion de grasas. '
        'Sin suficiente agua, el higado dedica capacidad a funciones del rinon, reduciendo la quema de grasa.', BODY))
    story.append(Spacer(1,4))
    story.append(note_box(
        f'<b>Tu objetivo de hidratacion:</b> {round(float(n.get("peso",75) or 75) * 0.035, 1)} litros/dia en reposo. '
        'En dias de entreno añade 0.5-1 litro adicional. '
        'Señal de hidratacion correcta: orina de color amarillo palido, nunca oscura.'))
    story.append(Spacer(1,10))

    story.append(Paragraph('Por que el musculo protege tu salud a largo plazo', H2))
    story.append(Paragraph(
        'Mas alla de la estetica, el musculo esqueletico es el mayor organo metabolico del cuerpo. '
        'La sarcopenia (perdida de masa muscular con la edad) empieza alrededor de los 30 años y '
        'se acelera despues de los 40 si no se trabaja para frenarla. '
        'Una persona sedentaria puede perder hasta el 3-5% de masa muscular cada decada. '
        'Esto reduce la sensibilidad a la insulina, eleva la presion arterial, debilita los huesos '
        'y reduce la capacidad funcional en la vejez. '
        'El entrenamiento de fuerza es la unica intervencion que frena y revierte este proceso.', BODY))
    story.append(Spacer(1,6))
    longevidad_data = [
        hrow('Beneficio a largo plazo', 'Mecanismo', 'Evidencia cientifica'),
        [Paragraph('<b>Prevencion diabetes tipo 2</b>', TDB),
         Paragraph('El musculo consume glucosa sin insulina durante el ejercicio', TD),
         Paragraph('Reduce el riesgo hasta un 35% en personas con historial familiar', TD)],
        [Paragraph('<b>Salud cardiovascular</b>', TDB),
         Paragraph('Mejora el perfil lipidico y reduce la presion arterial en reposo', TD),
         Paragraph('Tan efectivo como el cardio en reduccion de presion arterial', TD)],
        [Paragraph('<b>Densidad osea</b>', TDB),
         Paragraph('La tension mecanica del entreno estimula la formacion de hueso nuevo', TD),
         Paragraph('Previene y revierte la osteoporosis en adultos mayores', TD)],
        [Paragraph('<b>Salud mental</b>', TDB),
         Paragraph('Libera BDNF, dopamina y serotonina. Reduce cortisol cronicamente', TD),
         Paragraph('Tan efectivo como los antidepresivos en depresion leve-moderada', TD)],
        [Paragraph('<b>Longevidad</b>', TDB),
         Paragraph('La fuerza muscular es el mejor predictor de mortalidad por todas las causas', TD),
         Paragraph('Las personas con mayor fuerza viven mas y con mayor calidad de vida', TD)],
    ]
    longt = Table(longevidad_data, colWidths=[120, 175, CW-295])
    longt.setStyle(TableStyle(base_ts()))
    story.append(longt)
    story.append(PageBreak())

    story.append(Paragraph('El sueño como herramienta de entrenamiento', H2))
    story.append(Paragraph(
        'El sueño es donde ocurre el 80% de la recuperacion muscular. Durante el sueño profundo '
        'el organismo libera hormona de crecimiento, repara el tejido muscular danado en el entreno '
        'y consolida los patrones de movimiento aprendidos. Dormir menos de 6 horas durante mas de '
        'tres dias consecutivos reduce la testosterona hasta un 10-15% y eleva el cortisol, '
        'la hormona del estres que favorece el almacenamiento de grasa abdominal. '
        f'Tu objetivo son 7-8 horas. Actualmente duermes {sueno}h.', BODY))
    story.append(Spacer(1,6))

    sueno_data = [
        hrow('Habito', 'Por que funciona'),
        [Paragraph('<b>Mismo horario todos los dias</b>', TDB),
         Paragraph('El ritmo circadiano se regula con la constancia. Los fines de semana tambien.', TD)],
        [Paragraph('<b>Temperatura de la habitacion 17-19 C</b>', TDB),
         Paragraph('El descenso de temperatura corporal es la senal biologica de inicio del sueño.', TD)],
        [Paragraph('<b>Sin pantallas 30-60 min antes</b>', TDB),
         Paragraph('La luz azul suprime la melatonina hasta 3 horas. No hay pastilla que lo compense.', TD)],
        [Paragraph('<b>Oscuridad total en la habitacion</b>', TDB),
         Paragraph('Cualquier luz, por pequeña que sea, interrumpe los ciclos de sueño profundo.', TD)],
        [Paragraph('<b>Magnesio bisglicinato antes de dormir</b>', TDB),
         Paragraph('Reduce el tiempo para conciliar el sueño y mejora la calidad del sueño profundo.', TD)],
    ]
    st2 = Table(sueno_data, colWidths=[160, CW-160])
    st2.setStyle(TableStyle(base_ts()))
    story.append(st2)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════
    # MODULO 7: PRIMEROS PASOS
    # ═══════════════════════════════════════════════════
    story.append(Paragraph('Modulo 7', LMOD))
    story.append(Paragraph('Primeros Pasos — Las proximas 48 horas', H1))
    story.append(hr_em())

    actions = [
        ('1','Hoy','Guarda este plan en tu movil',
         'Tenlo siempre accesible. Lo que no se ve, se olvida y lo que se olvida no se hace.'),
        ('2','Hoy','Haz la lista de la compra del menu semanal',
         'Pollo, huevos, yogur griego, arroz, avena, verduras, AOVE, nueces. Sin excusas nutricionales.'),
        ('3','Hoy','Compra creatina monohidrato y vitamina D3',
         'Los dos suplementos con mayor evidencia cientifica. Precio bajo, impacto alto.'),
        ('4','Manana','Completa tu primera sesion de entrenamiento',
         f'Rutina A con {equipo.lower()}. No busques la perfeccion — la primera sesion solo tiene que existir.'),
        ('5','Esta semana','Registra tus metricas de inicio',
         'Peso en ayunas, foto frontal y lateral, medida de cintura. Son tu punto de referencia real.'),
    ]

    for num, when, title, body in actions:
        left = Paragraph(f'<b>{num}</b><br/><font size="7">{when}</font>',
            S('an'+num, fontName='Helvetica-Bold', fontSize=15, textColor=WHITE, alignment=TA_CENTER, leading=19))
        rt = Table([[Paragraph(f'<b>{title}</b>',
                     S('at'+num, fontName='Helvetica-Bold', fontSize=9, textColor=TEXT_DARK, leading=13))],
                    [Paragraph(body, S('ab'+num, fontSize=8, textColor=TEXT_SUB, leading=12))]],
                   colWidths=[CW-50])
        rt.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
                                ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
        act = Table([[left, rt]], colWidths=[48, CW-50])
        act.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(0,-1), EM_DARK), ('BACKGROUND',(1,0),(1,-1), WHITE),
            ('BOX',(0,0),(-1,-1), 0.5, LINE_COLOR),
            ('TOPPADDING',(0,0),(-1,-1), 9), ('BOTTOMPADDING',(0,0),(-1,-1), 9),
            ('LEFTPADDING',(0,0),(-1,-1), 7), ('RIGHTPADDING',(0,0),(-1,-1), 8),
            ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
        ]))
        story.append(act)
        story.append(Spacer(1,5))

    story.append(Spacer(1,10))
    story.append(note_box(
        f'<b>Este plan es tuyo.</b> Disenado para {nombre.split()[0]}, {n.get("edad","?")} anos, '
        f'{n.get("peso","?")}kg, objetivo: {objetivo}. '
        f'16 semanas de consistencia superan cualquier programa perfecto seguido 3 semanas. '
        f'Si tienes dudas, responde al email directamente.'))

    # Pagina final
    story.append(PageBreak())
    story.append(Spacer(1, 40*mm))
    story.append(HRFlowable(width='22%', thickness=3, color=EM_MID, spaceAfter=16))
    story.append(Paragraph('Metamorfosis',
        S('ff', fontName='Helvetica-Bold', fontSize=20, textColor=TEXT_DARK, leading=26, alignment=TA_CENTER)))
    story.append(Paragraph('Plan Personalizado Premium',
        S('fs', fontSize=10, textColor=TEXT_MUTED, leading=15, alignment=TA_CENTER, spaceAfter=16)))
    story.append(Paragraph('Tu programa. Tus resultados.',
        S('fm', fontName='Helvetica-BoldOblique', fontSize=14, textColor=EM_MID, leading=20, alignment=TA_CENTER)))

    doc.build(story)
    print(f'PDF generado: {output_path}')

if __name__ == '__main__':
    datos_prueba = {
        'nombre':'Roberto Andres','email':'robertoandrees12@gmail.com',
        'edad':'22','sexo':'Hombre','peso':'88','altura':'178',
        'pesoObjetivo':'77','objetivo':'Perder grasa','nivel':'Intermedio',
        'equipo':'Gimnasio completo','diasEntreno':'3',
        'diasPreferidos':'Jueves, Viernes, Domingo','horario':'Tarde',
        'lesiones':'no','nivelEstres':'3','horasSueno':'8',
        'tipoTrabajo':'Moderadamente activo','dieta':'Sin lactosa',
        'alimentosExcluir':'marisco','comentarios':'','fechaEnvio':'12/04/2026',
    }
    generar_pdf(datos_prueba, '/mnt/user-data/outputs/Plan_Personalizado_Ejemplo.pdf')