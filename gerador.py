from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape 
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth 
from reportlab.lib.colors import black
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os

# --- CONFIGURAÇÃO DO CAMINHO DO MODELO DE PDF ---
CAMINHO_MODELO_PDF = "/workspaces/GeradorDeCertificado/CertificadoModelo.pdf"
# -----------------------------------------------

# Caminhos das fontes
pasta_fontes = "Great_Vibes,Montserrat" 

pdfmetrics.registerFont(TTFont('GreatVibes', os.path.join(pasta_fontes, 'Great_Vibes', 'GreatVibes-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat', os.path.join(pasta_fontes, 'Montserrat', 'Montserrat-VariableFont_wght.ttf')))

# Parâmetros do certificado
def gerar_certificado(nome, workshop, data_evento, data_assinatura, carga_horaria, modelo_pdf):
    packet = BytesIO()
    
    largura_pagina, altura_pagina = landscape(A4)
    can = canvas.Canvas(packet, pagesize=landscape(A4)) 
    
    can.setFillColor(black)
    can.setStrokeColor(black)

    center_x = largura_pagina / 2

    # --- LÓGICA DO NOME ---
    tamanho_fonte_nome = 42 
    if len(nome) > 28:
        tamanho_fonte_nome = 32
    can.setFont("GreatVibes", tamanho_fonte_nome)
    can.drawCentredString(center_x, 320, nome) 
    # --- Fim da Lógica ---

    # === Textos do workshop e data ===
    can.setFont("Montserrat", 12)
    
    # Você definiu 1.5 aqui, isso vai deixar o texto bem grosso
    can.setLineWidth(1.5) 
    can._textRenderMode = 2
    
    texto_workshop = f'Participou do workshop "{workshop}" realizado no dia {data_evento} com carga horária total de {carga_horaria} horas.'
    
    can.drawCentredString(center_x, 260, texto_workshop) 
    can.drawCentredString(center_x, 230, data_assinatura) 

    can._textRenderMode = 0
    
    can.save()
    packet.seek(0)

    novo_pdf = PdfReader(packet)
    with open(modelo_pdf, "rb") as base_file:
        modelo = PdfReader(base_file)
        output = PdfWriter()

        pagina_base = modelo.pages[0]
        pagina_base.merge_page(novo_pdf.pages[0])
        output.add_page(pagina_base)

        nome_arquivo = f"certificado_{nome.replace(' ', '_')}.pdf"
        with open(nome_arquivo, "wb") as output_stream:
            output.write(output_stream)

    print(f"\n✅ Certificado gerado com sucesso: {nome_arquivo}\n")

# === Terminal ===
print("GERADOR DE CERTIFICADOS\n")

modelo_pdf = CAMINHO_MODELO_PDF

# Verificação simples se o caminho foi preenchido
if modelo_pdf == "SEU_CAMINHO_COMPLETO_AQUI.pdf":
    print("ERRO: Por favor, abra o arquivo .py e defina o 'CAMINHO_MODELO_PDF' na linha 13.")
else:
    nome = input("Nome do participante: ")
    workshop = input("Nome do workshop: ")
    data_evento = input("Data do evento: ")
    data_assinatura = input("Data da assinatura: ")
    carga_horaria = input("Carga horária: ")

    gerar_certificado(nome, workshop, data_evento, data_assinatura, carga_horaria, modelo_pdf)