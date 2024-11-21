import os
from groq import Groq
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time

# Configurar a chave de API do Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "your_api_key"))

def gerar_caso_de_teste_e_codigo(descricao):
    # 1. Gerar o caso de teste a partir da descrição
    resposta_teste = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Você é um especialista em QA."},
            {"role": "user", "content": f"Baseado nos passos fornecidos, gere um caso de teste para uma aplicação de login. Passos: {descricao}"}
        ],
        model="llama-3.1-70b-versatile",
    )
    
    # Extrair o caso de teste gerado
    caso_teste = resposta_teste.choices[0].message.content
    print("Caso de Teste Gerado:\n", caso_teste)
    print("---------------------------------------------------------")

    # 2. Gerar o código Selenium a partir do caso de teste gerado
    resposta_codigo = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Você é um assistente de desenvolvimento."},
            {"role": "user", "content": f"Gere um código Selenium para automatizar o seguinte caso de teste: {caso_teste}"}
        ],
        model="llama-3.1-70b-versatile",
    )

    # Extrair o código Selenium gerado
    codigo_selenium = resposta_codigo.choices[0].message.content
    print("Código Selenium Gerado:\n", codigo_selenium)
    print("---------------------------------------------------------")

    return caso_teste, codigo_selenium

# Exemplo de descrição do caso de teste
descricao_caso_teste = """
Abra o navegador e acesse a página de login do site.
Digite um e-mail e senha válidos nos campos de login.
Clique no botão de login.
Verifique se o usuário foi redirecionado para a página inicial e se o login foi realizado com sucesso.
"""

# Executar a função para gerar o caso de teste e o código Selenium
caso_de_teste, codigo_selenium = gerar_caso_de_teste_e_codigo(descricao_caso_teste)

# Classe de teste automatizado com Selenium e unittest
class TesteLoginSelenium(unittest.TestCase):

    def setUp(self):
        # Configurar o WebDriver (certifique-se de que o driver está no PATH)
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.opencartbrasil.com.br/conta/acessar")

    def test_login_valido(self):
        driver = self.driver
        # Seguindo os passos fornecidos pelo código Selenium gerado
        driver.find_element(By.ID, "input-email").send_keys("duduaugustoabc@gmail.com")
        driver.find_element(By.ID, "input-password").send_keys("Dudu2510")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        time.sleep(2)  # Espera pelo carregamento da página
        meus_dados = driver.find_element(By.LINK_TEXT, "Meus dados")
        self.assertTrue(meus_dados.is_displayed(), "O link 'Meus dados' não está visível após o login.")
    
    def tearDown(self):
        self.driver.quit()

# Executar o teste com um relatório
if __name__ == "__main__":
    print("Executando o teste de login com Selenium:")
    unittest.main(verbosity=2)
