import os
import subprocess
from groq import Groq
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Inicialização do cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "your_api_key"))

def extrair_elementos_principais(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)  # Aguarde o carregamento da página

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    elementos_importantes = []

    for tag in soup.select("input, button, form"):
        elementos_importantes.append({
            "tag": tag.name,
            "id": tag.get("id"),
            "class": tag.get("class"),
            "name": tag.get("name"),
            "placeholder": tag.get("placeholder"),
            "text": tag.get_text(strip=True)
        })

    return elementos_importantes

def agente_automatizador(descricao_inicial, dominio, email, senha):
    elementos_html = extrair_elementos_principais(dominio)
    descricao_elementos = "\n".join([
        f"Tag: {elem['tag']}, ID: {elem['id']}, Classe: {elem['class']}, Name: {elem['name']}, Placeholder: {elem['placeholder']}, Texto: {elem['text']}"
        for elem in elementos_html if elem['id'] or elem['class'] or elem['name'] or elem['placeholder'] or elem['text']
    ])

    descricao_teste = (
        f"{descricao_inicial}. Use apenas esses elementos HTML e seletores exatos para o código:\n{descricao_elementos}\n"
        f"Domain: {dominio}, Email: {email}, Password: {senha}"
    )

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

    resposta_codigo = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert in test development."},
            {"role": "user", "content": f"Generate the python Selenium code for the test case, using only the provided IDs, classes, and selectors without guessing or creating new selectors. Do not mention what programming language you are using, do not surround it with ´´´, and do not add comments or additional text, starting from imports: {caso_teste}"}
        ],
        model="llama-3.1-70b-versatile",
    )
    codigo_selenium = resposta_codigo.choices[0].message.content
    print("Código Selenium:\n", codigo_selenium)

    with open("teste_login_selenium.py", "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(codigo_selenium)

    print("Executando o teste Selenium e gerando relatório:")
    resultado_execucao = subprocess.run(["python", "teste_login_selenium.py"], capture_output=True, text=True)
    print("Resultado do Teste:\n")
    print(resultado_execucao.stdout)

    if resultado_execucao.stderr:
        print("Erros durante a execução:\n", resultado_execucao.stderr)

    print("---------------------------------------------------------")

# Parâmetros de execução do agente automatizador
descricao = "Login com e-mail e senha válidos no site de exemplo OpenCart"
dominio = "https://www.opencartbrasil.com.br/conta/acessar"
email = "duduaugustoabc@gmail.com"
senha = "Dudu2510"
agente_automatizador(descricao, dominio, email, senha)
