from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import messagebox

# Configuração do Banco de Dados
Base = declarative_base()

class Item(Base):
    __tablename__ = 'itens'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    categoria = Column(String)
    emprestado = Column(Boolean, default=False)

# Conexão com o banco de dados SQLite
engine = create_engine('sqlite:///catalogo.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Funções para gerenciar itens no banco de dados
def adicionar_item(nome, descricao, categoria):
    item = Item(nome=nome, descricao=descricao, categoria=categoria)
    session.add(item)
    session.commit()

def listar_itens():
    return session.query(Item).all()

def remover_item(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        session.delete(item)
        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

def marcar_emprestado(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        item.emprestado = True
        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

def marcar_devolvido(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        item.emprestado = False
        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Catálogo de Itens IoT")

# Função para adicionar item via interface
def adicionar_item_interface():
    nome = nome_entry.get()
    descricao = descricao_entry.get()
    categoria = categoria_entry.get()
    
    if nome:  # Verificar se o nome foi preenchido
        adicionar_item(nome, descricao, categoria)
        listar_itens_interface()
    else:
        messagebox.showerror("Erro", "Nome do item é obrigatório!")

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
    if item_id.isdigit():
        marcar_emprestado(int(item_id))
        listar_itens_interface()
    else:
        messagebox.showerror("Erro", "ID inválido!")

# Função para marcar item como devolvido via interface
def marcar_devolvido_interface():
    item_id = id_entry.get()
    if item_id.isdigit():
        marcar_devolvido(int(item_id))
        listar_itens_interface()
    else:
        messagebox.showerror("Erro", "ID inválido!")

# Função para listar itens na interface
def listar_itens_interface():
    lista.delete(0, tk.END)
    itens = listar_itens()
    for item in itens:
        status = "Emprestado" if item.emprestado else "Disponível"
        lista.insert(tk.END, f'ID: {item.id} - {item.nome} ({item.categoria}): {status}')

# Labels e Campos de Entrada
tk.Label(root, text="Nome").grid(row=0)
tk.Label(root, text="Descrição").grid(row=1)
tk.Label(root, text="Categoria").grid(row=2)
tk.Label(root, text="ID (para empréstimo/remover)").grid(row=4)

nome_entry = tk.Entry(root)
descricao_entry = tk.Entry(root)
categoria_entry = tk.Entry(root)
id_entry = tk.Entry(root)

nome_entry.grid(row=0, column=1)
descricao_entry.grid(row=1, column=1)
categoria_entry.grid(row=2, column=1)
id_entry.grid(row=4, column=1)

# Botões para Ações
tk.Button(root, text='Adicionar Item', command=adicionar_item_interface).grid(row=3, column=1)
tk.Button(root, text='Remover Item', command=remover_item_interface).grid(row=5, column=1)
tk.Button(root, text='Marcar como Emprestado', command=marcar_emprestado_interface).grid(row=6, column=1)
tk.Button(root, text='Marcar como Devolvido', command=marcar_devolvido_interface).grid(row=7, column=1)

# Listbox para exibir itens
lista = tk.Listbox(root, width=50)
lista.grid(row=8, column=0, columnspan=2)
listar_itens_interface()

root.mainloop()
