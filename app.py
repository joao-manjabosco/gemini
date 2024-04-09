from flask import Flask, render_template, request # Importa Flask para criar a aplicação web, render_template para renderizar modelos HTML e request para lidar com requisições HTTP
from flask_wtf import FlaskForm # Importa FlaskForm para criar formulários com Flask
from wtforms import StringField, TextAreaField, SubmitField # Importa os tipos de campos de formulário StringField, TextAreaField e SubmitField do WTForms
from wtforms.validators import DataRequired # Importa o validador DataRequired do WTForms para validar campos de formulário
import google.generativeai as genai # Importa a biblioteca generativeai do Google
from key import key # Importa a chave de API do arquivo key.py
from prompt import tag, prompt # Importa as funções tag e prompt do arquivo prompt.py

app = Flask(__name__) # Cria uma instância da aplicação Flask
app.secret_key = '04b49f7c740b5763f9a4b79ad07623e0' # Define a chave secreta para a aplicação Flask

# Define uma classe para o formulário de clientes que herda de FlaskForm
class FormClientes(FlaskForm):
    # Define um campo de texto para o briefing comercial com validação de dados obrigatórios
    briefing = StringField("Briefing Comercial", validators=[DataRequired()])
    # Define um botão de envio para o formulário
    botao_confirmacao = SubmitField("Enviar")
    # Define um campo de texto grande para exibir a resposta da API, tornando-o somente leitura
    resposta_api = TextAreaField("Resposta da API", render_kw={"readonly": True})  # Campo somente leitura

# Define a rota principal da aplicação, que pode lidar com os métodos GET e POST
@app.route('/', methods=["GET", "POST"])
def index(): 
    # Cria uma instância do formulário FormClientes
    form = FormClientes()
    # Verifica se a requisição é do tipo POST
    if request.method == 'POST':
        # Verifica se o formulário foi validado com sucesso
        if form.validate_on_submit():
            # Obtém o briefing comercial do formulário
            briefing = form.briefing.data
            # Cria o prompt para a API de IA usando o briefing comercial
            promp = f"{tag} Briefing comercial:{briefing} {prompt}"
            # Configura a chave da API da biblioteca generativeai
            genai.configure(api_key=key)
            # Cria uma instância do modelo de IA
            model = genai.GenerativeModel('gemini-pro')
            # Gera o conteúdo com base no prompt usando o modelo de IA
            response = model.generate_content(promp)
            # Atribui a resposta da API ao campo de resposta do formulário
            form.resposta_api.data = response.text  # Atribui a resposta ao campo do formulário
    # Renderiza o template 'index.html', passando o formulário como contexto
    return render_template('index.html', form=form)

if __name__ == '__main__':
    # Executa a aplicação Flask em modo de depuração quando o script é executado diretamente
    app.run(debug=True)
