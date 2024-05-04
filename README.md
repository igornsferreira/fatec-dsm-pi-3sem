# EcoShare | PI do 3º semestre de 2024 | DSM - Fatec Araras

A aplicação "EcoShare" é uma plataforma desenvolvida em Django com o objetivo de facilitar o processo de doação de materiais recicláveis e recebimento de alimentos em troca. Através da plataforma, os usuários podem se cadastrar e acessar uma dashboard intuitiva.

## Participantes

<p align="center">
  <a href="https://github.com/igornsferreira">
    <img src="https://avatars.githubusercontent.com/igornsferreira" width="15%">
  </a>
  <a href="https://github.com/beamclive">
    <img src="https://avatars.githubusercontent.com/beamclive" width="15%">
  </a>
  <a href="https://github.com/Brubzie">
    <img src="https://avatars.githubusercontent.com/Brubzie" width="15%">
  </a>
  <a href="https://github.com/Eduguinho">
    <img src="https://avatars.githubusercontent.com/Eduguinho" width="15%">
  </a>
  <a href="https://github.com/EndrewFatec">
    <img src="https://avatars.githubusercontent.com/EndrewFatec" width="15%">
  </a>
</p>

## Configuração do Ambiente e Execução do Projeto

Este projeto foi desenvolvido utilizando Python, Django e MongoDB. Siga as instruções abaixo para configurar o ambiente de desenvolvimento e executar o projeto.

### Pré-requisitos

- Python
- Django
- MongoDB

### Configuração do Ambiente e Execução (Windows)

1. Clone o repositório do projeto:
    ```bash
    git clone https://github.com/igornsferreira/fatec-dsm-pi-3sem.git
    ```
2. Navegue até o diretório do projeto.

3. Crie um ambiente virtual Python e ative-o:
    ```bash
    python -m venv venv
    venv\Scripts\activate.bat
    ```
4. Instale as dependências do projeto:
    ```bash
    pip install -r requeriments.txt
    ```
5. Use o MongoDB Compass para conectar-se ao localhost. Utilize o nome 'ecoshare_database' na criação do banco de dados e na coleção 'ecoshare'.

6. Aplique as migrações do Django:
    ```bash
    python manage.py migrate
    ```

8. Inicie o servidor Django:
    ```bash
    python manage.py runserver
    ```
Agora, você deve ser capaz de acessar o projeto.
