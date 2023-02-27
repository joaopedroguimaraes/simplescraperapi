# Simple Scraper API
_File scraper API for Simple Energy selection process._

API de extrator de arquivos para o processo seletivo da 
Simple Energy.

```Versão do Python: 3.10```

## Sobre

O desafio dessa aplicação foi o desenvolvimento de um webscraper que
obtivesse as informações de um link previamente estabelecido. As
informações consistiam em um código a ser utilizado na busca e a
plataforma-alvo retorna os arquivos existentes para aquele código.

Para melhor entendimento do contexto, você pode utilizar o link e os
códigos abaixo para testar:


|[Teste - simpleenergy.com.br](https://simpleenergy.com.br/teste/)|
|---|
|Códigos de teste: **321465** e **98465**|

Com isso, o webscraper tem a finalidade de receber um código, acessar
o site e obter as informações listadas, além dos arquivos disponíveis
para download através do clique em seus respectivos nomes.

## Informações iniciais sobre segurança

Algumas credenciais estão _mockadas_ no código, ainda que
separadamente, para permitir que qualquer usuário clone o repositório
e possa testar a aplicação sem a necessidade de ter acesso às 
ferramentas terceiras utilizadas na aplicação, o MongoDB e o AWS S3.

Essa decisão foi tomada de forma consciente e acreditando em uma
facilidade maior para a entrega funcional da aplicação. Para 
incrementar a maturidade e a segurança da aplicação, o _deploy_ 
contaria com variáveis de ambiente nas quais haveria a injeção dos
valores das credenciais utilizadas.

## A solução

### Webscraper / raspador

O desenvolvimento teve por foco inicial o webscraper utilizando o
**Scrapy** como _framework_ para extrair as informações e os arquivos. A
escolha dá-se pela possibilidade de escalabilidade, facilidade de 
raspagem, utilização de _pipelines_ para inserção de informações em um
banco de dados **MongoDB** e _upload_ dos arquivos no **AWS S3**.

Subir as informações raspadas pelo _CodeSpider_, o webscraper, em um
banco de dados e depois obter e fazer o _upload_ dos arquivos em um
servidor de arquivos foi uma estratégia para tornar independentes as
informações adquiridas pelo webscraper, não havendo a necessidade de
rodar o webscraper a cada necessidade de ter informações e arquivos de
acordo com o código. Claro que, uma vez que nas regras de negócio haja
a possibilidade de mudança de informações e arquivos, essa estratégia
pode ser rápida e facilmente adaptada. A estratégia também foi 
escolhida por tratar-se de um processo seletivo, para que houvesse 
demonstração de conhecimentos e tecnologias.

### Banco de dados

O MongoDB foi a escolha de banco de dados justamente pela facilidade
de integração com o Python e pelo formato das informações que se
obtém, fazendo com que um banco de dados não-relacional seja a melhor
escolha.

O banco foi nomeado como ```simpleapi_db``` e a _collection_ foi
nomeada como ```codes```. O formato do _document_ é exemplificado
no dicionário abaixo:

```
{
    "_id":{"$oid": "63fac8e2126e99250ded45f6"},
    "code_number": "98465",
    "file_infos":[
        {
            "file_title": "Arquivo 1",
            "file_names": 
                ["arquivo1-98465.txt","arquivo1-98465.pdf"]
        },
        {
            "file_title": "Arquivo 2",
            "file_names":
            ["arquivo2-98465.txt","arquivo2-98465.pdf"]
        }
    ]
}
```

A plataforma utilizada para o banco de dados foi o 
[MongoDB Atlas](https://www.mongodb.com/pt-br/atlas), que 
oferece um serviço totalmente gerenciado na infraestrutura confiável e
globalmente escalonável do Google. Com o Atlas, é possível gerenciar
bancos de dados de maneira simples, com apenas alguns cliques na IU ou
ao chamar a API. Além disso, com algumas limitações, é possível 
utilizá-la de forma gratuita.

### Armazenamento de arquivos

Para o servidor de armazenamento de arquivos optei por uma instância 
[AWS S3](https://aws.amazon.com/pt/s3/) (Amazon Simple Storage 
Service, ou Amazon S3), um serviço de armazenamento de objetos que 
oferece escalabilidade, disponibilidade de dados, segurança e 
performance líderes do setor. Além disso, a biblioteca **boto3** 
oferece ao projeto uma fácil integração do Python com o serviço, além
de existir também a integração do **Scrapy** com o **S3** através da
_pipeline_ _FilesPipeline_, executada ao final da extração dos dados e 
realizando de forma automática o upload para o _bucket_ criado.

### API

Também desenvolvi, utilizando o 
[Flask](https://flask.palletsprojects.com/en/2.2.x/) e bibliotecas
adjacentes como o
[Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/), uma 
API para que o webscraper fosse chamado e executado e houvesse
integração também ao banco de dados e ao servidor de arquivos para que
o usuário final conseguisse utilizar a aplicação de forma mais 
padronizada e não dependesse de comandos executados no terminal, além 
de oferecer possibilidade para integrar essa aplicação a outras.

A API possui basicamente 2 endpoints de interesse para o usuário:

```http
  POST /api/codes/<code_number>
  Retorna as informações de arquivos dado o código.
  
  GET /api/download/<code_number>/<filename>
  Retorna o arquivo para download dado o código e o nome do arquivo.
```

#### Validação da API
A API faz uma validação no primeiro _endpoint_ sobre a já existência
das informações daquele **código** dentro do banco de dados. Caso ele
já tenha sido consultado, então suas informações já constam no banco
e seus arquivos já estão no servidor de arquivos; ou seja, a API 
acessa essas informações e as retorna para o usuário.

Caso a API consulte o banco de dados e valide que o **código** ainda
não consta lá (ou seja, primeira tentativa de consulta daquele 
**código**), então aciona o **Scrapy** e inicia o _CodeSpider_, que 
rapidamente fará a consulta na aplicação terceira, salvará as 
informações e os arquivos e logo retornará como resposta do 
_endpoint_.

#### TODO: Swagger
Uma possibilidade bastante interessante poderia ser utilizar o 
[Swagger](https://swagger.io/) para a documentação da API.

#### TODO: Validações dos endpoints
Para agilizar a entrega da aplicação não implementei validações e os
fluxos de exceção para os endpoints mencionados, mas desenvolvê-las
facilitaria a legibilidade da resposta em caso de erro no fluxo
(arquivo inexistente, código não encontrado, etc).

### Aplicação Web

Tanto para tornar a aplicação mais _user-friendly_ como para facilitar
os testes, seja durante o desenvolvimento ou na avaliação, criei uma
interface web que pode ser acessada através do seguinte endpoint:

```http
  GET /
  Acesso à interface web.
```

A interface permite ao usuário a busca por um **código** e retorna
na página a lista de arquivos raspados daquele **código**, 
possibilitando também que o usuário faça o download de um arquivo à
sua escolha dentre os listados.

## Executando

É possível executar a aplicação de duas formas: manualmente ou através
do Docker.

### Execução manual
Após clonar este repositório e ter a versão do Python compatível
instalada, é necessário ativar o _venv_.

Em seguida, execute o comando abaixo para instalar as bibliotecas 
necessárias:

```
pip install -r requirements.txt
```

O _pip_ se encarregará de instalar as bibliotecas nas versões
especificadas pelo arquivo _requirements.txt_.

Para rodar a aplicação, você deverá executar o seguinte comando no seu 
terminal.

Lembre-se: é necessário ter o `venv` habilitado e seu terminal estar 
apontando para o diretório raiz do projeto.

```
Terminal:

Windows
python .\simplescraper\tests_run.py

Linux
python /simplescraper/tests_run.py
```

Ao rodar, deve aparecer o seguinte:

```
Terminal:

> python /simplescraper/tests_run.py
 * Serving Flask app 'flask_app.settings'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 211-836-288
```

Deixei a _flag_ `DEBUG=True` ao rodar o Flask para que eventuais
exceções sejam mais facilmente captadas. Em um ambiente de deploy em 
produção seria necessário desativar a _flag_ e configurar o servidor
WSGI. Pode-se utilizar, por exemplo, o `gunicorn`.

Com a aplicação em execução, pode-se utilizar os _endpoints_ da API
ou ir direto para a interface web acessando o `http://127.0.0.1:5000/`
localmente.

### Execução pelo Docker

Para executar a aplicação pelo Docker, você deve tê-lo previamente
instalado e configurado e, em seguida, pelo terminal e estando na
raiz do projeto, execute sequencialmente os comandos:

```
docker image build -t simpleapi .

docker run -p 5000:5000 -d simpleapi
```

Com isso, você poderá acessar a aplicação através do link:

```
http://localhost:5000/
```

## Contato

Você pode me contatar através dos seguintes links:

- [Whatsapp](https://api.whatsapp.com/send?phone=5519981119478)
- [Email](mailto:joaopedroguimaraes96@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/joaopedroguimaraes)