# 🧾 Gerador de Certificados em PDF

Script em **Python** para gerar certificados personalizados a partir de um **modelo PDF**, usando fontes elegantes (**Great Vibes** e **Montserrat**).  
O programa insere automaticamente o **nome do participante**, **nome do workshop**, **datas** e **carga horária** — tudo centralizado e com formatação personalizada.

---

## 🚀 Funcionalidades

- Gera certificados em PDF com base em um modelo pré-existente.  
- Permite inserir:
  - Nome do participante  
  - Nome do workshop  
  - Data do evento  
  - Data da assinatura  
  - Carga horária  
- Ajusta automaticamente o tamanho da fonte do nome (para caber no layout).  
- Usa fontes personalizadas (**Great Vibes** e **Montserrat**).  
- Suporte a páginas no formato **A4 paisagem (landscape)**.

---

## 📦 Requisitos

Antes de rodar o projeto, instale:

- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (gerenciador de pacotes do Python)
- `git` (para clonar o repositório)

---

### 1️. Clone o repositório

Abra seu terminal e clone o projeto:

```bash
git clone https://github.com/massarrahelenna/GeradorDeCertificado.git
cd GeradorDeCertificado
```
---

### 2. Instale as dependências

```bash
pip install reportlab PyPDF2
```
---

### 3. Rode o código

```bash
python gerador.py
```
---
