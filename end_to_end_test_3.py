import os
import subprocess
from groq import Groq
from selenium import webdriver
from bs4 import BeautifulSoup
import time

#Nessa versão, de fato as id´s do html são recuperadas e informadas ao código para que ele o faça de forma ótima
# Inicialização do cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "your_api_key"))

def extrair_elementos_principais(url):
    driver = webdriver.Chrome() 
    driver.get(url)
    time.sleep(3)  # Aguarde o carregamento da página

    # Obtém o HTML da página
    html_content = driver.page_source
    driver.quit()

    # Analisa o HTML com BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    elementos_importantes = []

    # Extraí os principais elementos HTML que geralmente são utilizados em testes de login
    for tag in soup.select("input, button, form, a"):
        elementos_importantes.append({
            "tag": tag.name,
            "id": tag.get("id"),
            "class": tag.get("class"),
            "placeholder": tag.get("placeholder"),
            "text": tag.get_text(strip=True)
        })

    return elementos_importantes

def agente_automatizador(descricao_inicial, dominio, email, senha):
    # Extrai as IDs e outras informações importantes dos elementos HTML
    elementos_html = extrair_elementos_principais(dominio)
    descricao_elementos = "\n".join([
        f"Tag: {elem['tag']}, ID: {elem['id']}, Classe: {elem['class']}, Placeholder: {elem['placeholder']}, Texto: {elem['text']}"
        for elem in elementos_html if elem['id'] or elem['class'] or elem['placeholder'] or elem['text']
    ])

    # Passa a descrição dos elementos ao agente para ajudar a gerar o código Selenium otimizado
    descricao_teste = (
        f"{descricao_inicial}. Use these HTML element details for accuracy:\n{descricao_elementos}\n"
        f"Domain: {dominio}, Email: {email}, Password: {senha}"
    )

    # Etapa 1: Gerar caso de teste
    resposta_teste = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a QA expert."},
            {"role": "user", "content": f"Generate a detailed test case to: {descricao_teste}"}
        ],
        model="llama-3.1-70b-versatile",
    )
    caso_teste = resposta_teste.choices[0].message.content
    print("Caso de Teste:\n", caso_teste)
    print("---------------------------------------------------------")

    # Etapa 2: Gerar código Selenium
    resposta_codigo = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert in test development."},
            {"role": "user", "content": f"Generate the python Selenium code for the test case, without mentioning what programming language you are using, do not surround it with ´´´, and do not do comments and additional texts, starting from imports and do not quote it: {caso_teste}"}
        ],
        model="llama-3.1-70b-versatile",
    )
    codigo_selenium = resposta_codigo.choices[0].message.content
    print("Código Selenium:\n", codigo_selenium)

    # Salvar o código Selenium em um arquivo para execução
    with open("teste_login_selenium.py", "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(codigo_selenium)

    # Etapa 3: Executar o código Selenium e gerar relatório
    print("Executando o teste Selenium e gerando relatório:")
    resultado_execucao = subprocess.run(["python", "teste_login_selenium.py"], capture_output=True, text=True)
    print("Resultado do Teste:\n")
    print(resultado_execucao.stdout)  # Mostra o output do código Selenium

    # Tratamento de erros
    if resultado_execucao.stderr:
        print("Erros durante a execução:\n", resultado_execucao.stderr)

    print("---------------------------------------------------------")

# Parâmetros de execução do agente automatizador
descricao = "Login com e-mail e senha válidos no site de exemplo OpenCart, e depois adicionar à lista de desejos o módulo botão flutuante do WhatsApp"
dominio = "https://www.opencartbrasil.com.br/conta/acessar"
email = "duduaugustoabc@gmail.com"
senha = "Dudu2510"
agente_automatizador(descricao, dominio, email, senha)
