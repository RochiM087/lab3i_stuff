# ![Python](https://img.icons8.com/color/48/000000/python--v1.png) Catálogo de Itens Lab3i ![SQLite](https://img.icons8.com/color/48/000000/sqlite.png)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-8.6-brightgreen)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.22-orange)

Este projeto é um aplicativo de gerenciamento de itens em um laboratório, desenvolvido em Python utilizando Tkinter para a interface gráfica e SQLAlchemy para interagir com um banco de dados SQLite. O aplicativo permite adicionar, remover e gerenciar itens, além de registrar empréstimos e devoluções.

## Table of Contents
- [Catálogo de Itens Lab3i](#catálogo-de-itens-lab3i)
  - [Table of Contents](#table-of-contents)
  - [Instalação](#instalação)
  - [Importando Bibliotecas](#importando-bibliotecas)
  - [Funcionalidades](#funcionalidades)
  - [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
  - [Licença](#licença)

## Instalação

Para instalar e executar este projeto, siga os passos abaixo:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu_usuario/nome_do_repositorio.git
   cd nome_do_repositorio
   
2. **Instale as dependências:**

```bash
   pip install sqlalchemy pillow
```
3. **Execute o aplicativo**
```bash
   python3 main.py
```

## Importando Bibliotecas
```python
import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Item  # Modelos de banco de dados
```
## Funcionalidades
- `Adicionar Item`: Permite ao usuário adicionar novos itens ao catálogo, especificando nome, descrição, categoria e quantidade.
- `Remover Item`: Possibilita a remoção de itens do catálogo usando o ID do item.
- `Marcar como Emprestado`: Permite registrar o empréstimo de um item, especificando a quantidade emprestada e o nome da pessoa que está pegando o item.
- `Marcar como Devolvido`: Registra a devolução de um item e atualiza a quantidade disponível.
- `Marcar como Em Uso`: Permite marcar um item como "em uso".
- `Buscar Item`: Permite buscar itens pelo nome ou ID.
- `Listar Itens`: Exibe todos os itens cadastrados no catálogo com suas informações.

## Estrutura do Banco de Dados
- `id`: Identificador único do item (inteiro).
- `nome`: Nome do item (texto).
- `descricao`: Descrição do item (texto).
- `categoria`: Categoria do item (texto).
- `quantidade`: Quantidade disponível do item (inteiro).
- `emprestado`: Status se o item está emprestado (booleano).
- `em_uso`: Status se o item está em uso (booleano).
- `horario_emprestimo`: Horário em que o item foi emprestado (datetime).
- `pessoa_emprestou`: Nome da pessoa que pegou o item emprestado (texto).

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para discutir melhorias e correções.

## Licença
Esse projeto é licenciado em MIT License. Veja o arquivo de [Licença](LICENSE) para mais detalhes.

## Contato
Para dúvidas ou sugestões, entre em contato:
- Bruno: brunohr@cbpf.br

