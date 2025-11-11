from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape 
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os

CAMINHO_MODELO_PDF = "CertificadoModelo.pdf"


# Caminhos corretos das fontes
pasta_fontes_greatvibes = "Great_Vibes"
pasta_fontes_montserrat = "Montserrat"

fonte_greatvibes = os.path.join(pasta_fontes_greatvibes, "GreatVibes-Regular.ttf")
fonte_montserrat_regular = os.path.join(pasta_fontes_montserrat, "Montserrat-VariableFont_wght.ttf")
fonte_montserrat_bold = os.path.join(pasta_fontes_montserrat, "static", "Montserrat-Bold.ttf")

#verifica as pontes
for caminho in [fonte_greatvibes, fonte_montserrat_regular, fonte_montserrat_bold]:
    if not os.path.exists(caminho):
        print(f"Fonte não encontrada: {caminho}")
        exit(1)

#registro das fontes
pdfmetrics.registerFont(TTFont("GreatVibes", fonte_greatvibes))
pdfmetrics.registerFont(TTFont("MontserratRegular", fonte_montserrat_regular))
pdfmetrics.registerFont(TTFont("MontserratBold", fonte_montserrat_bold))


def gerar_certificado(nome, workshop, data_evento, data_assinatura, carga_horaria, modelo_pdf):
    packet = BytesIO()
    largura_pagina, altura_pagina = landscape(A4)
    can = canvas.Canvas(packet, pagesize=landscape(A4)) 
    
    can.setFillColor(black)
    center_x = largura_pagina / 2

    #NOME 
    tamanho_fonte_nome = 50 if len(nome) <= 28 else 38
    can.setFont("GreatVibes", tamanho_fonte_nome)
    can.drawCentredString(center_x, 310, nome)

    # TEXTO PRINCIPA 
    texto_parte1 = f'Participou do workshop "'
    texto_parte2 = f'" realizado no dia {data_evento} com carga horária total de {carga_horaria} horas.'
    texto_completo = texto_parte1 + workshop + texto_parte2

    # margem e largura útil
    margem_esq = 80
    margem_dir = 80
    largura_util = largura_pagina - (margem_esq + margem_dir)

    palavras = texto_completo.split(" ")
    linhas = []
    linha_atual = ""
    fonte_base = "MontserratRegular"
    tamanho_fonte = 15

    for palavra in palavras:
        teste = (linha_atual + " " + palavra).strip()
        largura_teste = pdfmetrics.stringWidth(teste, fonte_base, tamanho_fonte)
        if largura_teste <= largura_util:
            linha_atual = teste
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)

    #linhas centralizadas
    y_texto = 250
    for i, linha in enumerate(linhas):
        if workshop in linha:
            partes = linha.split(workshop)
            can.setFont("MontserratRegular", tamanho_fonte)
            largura_inicio = pdfmetrics.stringWidth(partes[0], "MontserratRegular", tamanho_fonte)
            largura_work = pdfmetrics.stringWidth(workshop, "MontserratBold", tamanho_fonte)
            largura_total = pdfmetrics.stringWidth(linha, "MontserratRegular", tamanho_fonte)

            x_inicio = center_x - (largura_total / 2)
            can.drawString(x_inicio, y_texto - (i * 20), partes[0])

            can.setFont("MontserratBold", tamanho_fonte)
            can.drawString(x_inicio + largura_inicio, y_texto - (i * 20), workshop)

            if len(partes) > 1:
                can.setFont("MontserratRegular", tamanho_fonte)
                can.drawString(x_inicio + largura_inicio + largura_work, y_texto - (i * 20), partes[1])
        else:
            can.setFont("MontserratRegular", tamanho_fonte)
            can.drawCentredString(center_x, y_texto - (i * 20), linha)

    #DATA
    can.setFont("MontserratRegular", 14)
    can.drawCentredString(center_x, 200, data_assinatura)

    can.save()
    packet.seek(0)

    #junta com o modelo
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

    print(f"Certificado gerado: {nome_arquivo}")


print("GERADOR DE CERTIFICADOS EM LOTE\n")

modelo_pdf = CAMINHO_MODELO_PDF

if not os.path.exists(modelo_pdf):
    print(f"Arquivo de modelo não encontrado: {modelo_pdf}")
    exit(1)

arquivo_nomes = input("Digite o nome do arquivo .txt com os nomes (ex: nomes.txt): ")

if not os.path.exists(arquivo_nomes):
    print("Arquivo de nomes não encontrado.")
    exit(1)

workshop = input("Nome do workshop: ")
data_evento = input("Data do evento: ")
data_assinatura = input("Data da assinatura: ")
carga_horaria = input("Carga horária: ")

with open(arquivo_nomes, "r", encoding="utf-8") as f:
    nomes = [linha.strip() for linha in f if linha.strip()]

print(f"\nGerando certificados para {len(nomes)} participantes...\n")

for nome in nomes:
    gerar_certificado(nome, workshop, data_evento, data_assinatura, carga_horaria, modelo_pdf)

print("\nTodos os certificados foram gerados\n")

