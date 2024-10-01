from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk

# Configuração do Banco de Dados
Base = declarative_base()

class Item(Base):
    __tablename__ = 'itens'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    categoria = Column(String)
    quantidade = Column(Integer, default=1)
    emprestado = Column(Boolean, default=False)
    em_uso = Column(Boolean, default=False)
    horario_emprestimo = Column(DateTime)
    pessoa_emprestou = Column(String)

# Conexão com o banco de dados SQLite
engine = create_engine('sqlite:///catalogo.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Funções para gerenciar itens no banco de dados
def adicionar_item(nome, descricao, categoria, quantidade):
    item = Item(nome=nome, descricao=descricao, categoria=categoria, quantidade=quantidade)
    session.add(item)
    session.commit()

def listar_itens():
    return session.query(Item).all()

def buscar_item(nome=None, item_id=None):
    if item_id:
        return session.query(Item).filter_by(id=item_id).first()
    elif nome:
        return session.query(Item).filter(Item.nome.like(f"%{nome}%")).all()
    return []

def remover_item(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        session.delete(item)
        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

def marcar_emprestado(item_id, quantidade, pessoa):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        if item.quantidade >= quantidade:
            item.quantidade -= quantidade
            if item.quantidade == 0:
                item.emprestado = True
            item.horario_emprestimo = datetime.now()
            item.pessoa_emprestou = pessoa
            session.commit()
        else:
            messagebox.showerror("Erro", "Quantidade insuficiente!")
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

def marcar_devolvido(item_id, quantidade):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        item.quantidade += quantidade
        item.emprestado = False
        item.horario_emprestimo = None
        item.pessoa_emprestou = None
        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

def marcar_em_uso(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        item.em_uso = True
        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

def listar_itens_interface():
    lista.delete(0, tk.END)
    itens = listar_itens()
    for item in itens:
        status_emprestado = "Emprestado" if item.emprestado else "Disponível"
        status_em_uso = "Em Uso" if item.em_uso else "Não em Uso"
        horario = item.horario_emprestimo.strftime('%Y-%m-%d %H:%M:%S') if item.horario_emprestimo else "N/A"
        pessoa = item.pessoa_emprestou if item.pessoa_emprestou else "N/A"
        lista.insert(tk.END, f'ID: {item.id} - {item.nome} ({item.categoria}): {status_emprestado} | {status_em_uso} | Quantidade: {item.quantidade} | Emprestado por: {pessoa} às {horario}')

# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Catálogo de Itens Lab3i")
root.geometry("1024x700")  # Resolução base
root.configure(background="#166ba9")
root.resizable(True, True)  # Torna a janela redimensionável

# Função para adicionar item via interface
def adicionar_item_interface():
    nome = nome_entry.get()
    descricao = descricao_entry.get()
    categoria = categoria_entry.get()
    quantidade = quantidade_entry.get()

    if nome and quantidade.isdigit():
        adicionar_item(nome, descricao, categoria, int(quantidade))
        listar_itens_interface()
    else:
        messagebox.showerror("Erro", "Nome e quantidade são obrigatórios!")

# Função para remover item via interface
def remover_item_interface():
    item_id = id_entry.get()
    if item_id.isdigit():
        remover_item(int(item_id))
        listar_itens_interface()
    else:
        messagebox.showerror("Erro", "ID inválido!")

# Função para marcar item como emprestado via interface
def marcar_emprestado_interface():
    item_id = id_entry.get()
    quantidade = quantidade_entry.get()
    pessoa = pessoa_entry.get()
    if item_id.isdigit() and quantidade.isdigit() and pessoa:
        marcar_emprestado(int(item_id), int(quantidade), pessoa)
        listar_itens_interface()
    else:
        messagebox.showerror("Erro", "ID, quantidade e nome da pessoa são obrigatórios!")

# Função para marcar item como devolvido via interface
def marcar_devolvido_interface():
    item_id = id_entry.get()
    quantidade = quantidade_entry.get()
    if item_id.isdigit() and quantidade.isdigit():
        marcar_devolvido(int(item_id), int(quantidade))
        listar_itens_interface()
    else:
        messagebox.showerror("Erro", "ID e quantidade inválidos!")

# Função para marcar item como em uso via interface
def marcar_em_uso_interface():
    item_id = id_entry.get()
    if item_id.isdigit():
        marcar_em_uso(int(item_id))
        listar_itens_interface()
    else:
        messagebox.showerror("Erro", "ID inválido!")

# Função para buscar itens pelo nome ou ID
def buscar_item_interface():
    nome = nome_entry.get()
    item_id = id_entry.get()
    
    lista.delete(0, tk.END)
    if item_id.isdigit():
        item = buscar_item(item_id=int(item_id))
        if item:
            status_emprestado = "Emprestado" if item.emprestado else "Disponível"
            status_em_uso = "Em Uso" if item.em_uso else "Não em Uso"
            horario = item.horario_emprestimo.strftime('%Y-%m-%d %H:%M:%S') if item.horario_emprestimo else "N/A"
            pessoa = item.pessoa_emprestou if item.pessoa_emprestou else "N/A"
            lista.insert(tk.END, f'ID: {item.id} - {item.nome} ({item.categoria}): {status_emprestado} | {status_em_uso} | Quantidade: {item.quantidade} | Emprestado por: {pessoa} às {horario}')
        else:
            lista.insert(tk.END, "Item não encontrado!")
    elif nome:
        itens = buscar_item(nome=nome)
        for item in itens:
            status_emprestado = "Emprestado" if item.emprestado else "Disponível"
            status_em_uso = "Em Uso" if item.em_uso else "Não em Uso"
            horario = item.horario_emprestimo.strftime('%Y-%m-%d %H:%M:%S') if item.horario_emprestimo else "N/A"
            pessoa = item.pessoa_emprestou if item.pessoa_emprestou else "N/A"
            lista.insert(tk.END, f'ID: {item.id} - {item.nome} ({item.categoria}): {status_emprestado} | {status_em_uso} | Quantidade: {item.quantidade} | Emprestado por: {pessoa} às {horario}')
    else:
        messagebox.showerror("Erro", "Preencha o campo de busca!")

# Configuração do layout ajustável
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(11, weight=1)

# Labels e Campos de Entrada
tk.Label(root, text="Nome", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=0, column=0, padx=10, pady=5, sticky="ew")
tk.Label(root, text="Descrição", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=1, column=0, padx=10, pady=5, sticky="ew")
tk.Label(root, text="Categoria", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=2, column=0, padx=10, pady=5, sticky="ew")
tk.Label(root, text="Quantidade", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=3, column=0, padx=10, pady=5, sticky="ew")
tk.Label(root, text="ID (para empréstimo/remover)", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=4, column=0, padx=10, pady=5, sticky="ew")
tk.Label(root, text="Pessoa", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=5, column=0, padx=10, pady=5, sticky="ew")

nome_entry = tk.Entry(root)
nome_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

descricao_entry = tk.Entry(root)
descricao_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

categoria_entry = tk.Entry(root)
categoria_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

quantidade_entry = tk.Entry(root)
quantidade_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

id_entry = tk.Entry(root)
id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

pessoa_entry = tk.Entry(root)
pessoa_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

# Botões
tk.Button(root, text='Adicionar Item', font=("Verdana", 14), command=adicionar_item_interface, bg="#4CAF50", fg="white").grid(row=6, column=0, padx=10, pady=10, sticky="ew")
tk.Button(root, text='Remover Item', font=("Verdana", 14), command=remover_item_interface, bg="#F44336", fg="white").grid(row=6, column=1, padx=10, pady=10, sticky="ew")
tk.Button(root, text='Marcar como Emprestado', font=("Verdana", 14), command=marcar_emprestado_interface, bg="#235da3", fg="white").grid(row=7, column=0, padx=10, pady=10, sticky="ew")
tk.Button(root, text='Marcar como Devolvido', font=("Verdana", 14), command=marcar_devolvido_interface, bg="#235da3", fg="white").grid(row=7, column=1, padx=10, pady=10, sticky="ew")
tk.Button(root, text='Marcar como Em Uso', font=("Verdana", 14), command=marcar_em_uso_interface, bg="#235da3", fg="white").grid(row=8, column=0, padx=10, pady=10, sticky="ew")
tk.Button(root, text='Buscar Item', font=("Verdana", 14), command=buscar_item_interface, bg="#235da3", fg="white").grid(row=8, column=1, padx=10, pady=10, sticky="ew")

# Lista de Itens
lista = tk.Listbox(root, width=80, height=10)
lista.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Botão para listar itens
tk.Button(root, text='Listar Todos os Itens', font=("Verdana", 14), command=listar_itens_interface, bg="#235da3", fg="white").grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Iniciar a interface
listar_itens_interface()
root.mainloop()


