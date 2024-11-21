import os
from groq import Groq
import subprocess

# Inicialização do cliente Groq, que age como um agente de IA aqui
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

def agente_automatizador(descricao_inicial, dominio, email, senha):
    # Etapa 1: Gerar caso de teste
    resposta_teste = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a QA expert."},
            {"role": "user", "content": f"Generate a detailed test case to: {descricao_inicial} on the domain {dominio}, and with this email {email} and this password {senha}"}
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

    #Tratamento de erros
    if resultado_execucao.stderr:
        print("Erros durante a execução:\n", resultado_execucao.stderr)

    print("---------------------------------------------------------")

# Para garantir que o agente compreenda o domínio, o e-mail e a senha, você os passa explicitamente como parâmetros na função 
# Descrição inicial do teste
descricao = "Login com e-mail e senha válidos no site de exemplo OpenCart"
dominio = "https://www.opencartbrasil.com.br/conta/acessar"
email = "duduaugustoabc@gmail.com"
senha = "Dudu2510"
agente_automatizador(descricao, dominio, email, senha)

# Feito apenas com chamadas para a API do Groq, sem uso de LLama Index ou LangChain