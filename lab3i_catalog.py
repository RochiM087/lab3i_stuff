from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
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

#
def abrir_janela_add():
    janela_add = Toplevel(root)
    janela_add.title("Adicionar Item")

    janela_add.geometry("900x360+140+170")
    janela_add.configure(background="#166ba9")

    for i in range(6):
        janela_add.columnconfigure(i, minsize=150, weight=1)
        janela_add.rowconfigure(i, minsize=60, weight=1)

    tk.Label(janela_add, text="Nome", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_add, text="Descrição", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_add, text="Categoria", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_add, text="Quantidade", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    nome_entry = tk.Entry(janela_add)
    nome_entry.grid(row=0, column=2, columnspan=4, padx=10, pady=5, sticky="ew")

    descricao_entry = tk.Entry(janela_add)
    descricao_entry.grid(row=1, column=2, columnspan=4, padx=10, pady=5, sticky="ew")

    categoria_entry = tk.Entry(janela_add)
    categoria_entry.grid(row=2, column=2, columnspan=4, padx=10, pady=5, sticky="ew")

    quantidade_entry = tk.Entry(janela_add)
    quantidade_entry.grid(row=3, column=2, columnspan=4, padx=10, pady=5, sticky="ew")

    tk.Button(janela_add, text='Adicionar Item', font=("Verdana", 14), command=lambda: adicionar_item_interface(nome=nome_entry.get(),descricao=descricao_entry.get(),categoria=categoria_entry.get(),quantidade=quantidade_entry.get(), janela=janela_add), bg="#4CAF50", fg="white").grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    tk.Button(janela_add, text='Cancelar', font=("Verdana", 14), command=janela_add.destroy, bg="#F44336", fg="white").grid(row=5, column=3, columnspan=3, padx=10, pady=10, sticky="ew")



# Funções para gerenciar itens no banco de dados
def adicionar_item(nome, descricao, categoria, quantidade):
    item = Item(nome=nome, descricao=descricao, categoria=categoria, quantidade=quantidade)
    session.add(item)
    session.commit()

def listar_itens():
    return session.query(Item).all()

def buscar_item(query, tipo):
    if tipo == "Nome":
        return session.query(Item).filter(Item.nome.like(f"%{query}%")).all()
    elif tipo == "ID":
        try:
            return session.query(Item).filter_by(id=int(query)).all()
        except:
            return []
    elif tipo == "Descrição":
        return session.query(Item).filter(Item.descricao.like(f"%{query}%")).all()
    elif tipo == "Categoria":
        return session.query(Item).filter(Item.categoria.like(f"%{query}%")).all()
    else:
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

# Listar itens
def listar_itens_interface(itens):
    #lista.delete(0, tk.END)
    lista.delete(*lista.get_children())

    if itens == []:
        return

    for it in itens:
        lista.insert("", "end", values=(
        it.id, # ID
        it.nome, # Nome
        it.categoria, # Categoria
        it.descricao, # Descrição
        it.quantidade, #Quantidade
        "N/A", # Quantidade disponível
        "Em Uso" if it.em_uso else "Não em Uso", # Estado
        it.pessoa_emprestou # Empréstimos
        ))



# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Catálogo de Itens Lab3i")
root.geometry("1080x700")  # Resolução base
root.configure(background="#166ba9")
root.resizable(True, True)  # Torna a janela redimensionável

# Função para adicionar item via interface
def adicionar_item_interface(nome, descricao, categoria, quantidade, janela):
    if nome and quantidade.isdigit():
        adicionar_item(nome, descricao, categoria, int(quantidade))
        listar_itens_interface(listar_itens())
        janela.destroy()
    else:
        messagebox.showerror("Erro", "Nome e quantidade são obrigatórios!")

# Função para remover item via interface
def remover_item_interface():
    def abrir_janela_remover(item_id):
        janela_rmv = Toplevel(root)
        janela_rmv.title("Remover Item")
        janela_rmv.configure(background="#166ba9")


        tk.Label(janela_rmv, text="Essa ação não pode ser desfeita, deseja remover o item?", font=("Verdana", 14), fg="white", bg="#166ba9").grid(row=0, column=0, columnspan=2, padx=10, pady=(15,10), sticky="ew")

        tk.Button(janela_rmv, text='Confirmar', font=("Verdana", 14), command=lambda: [remover_item(item_id),listar_itens_interface(listar_itens()), janela_rmv.destroy()], bg="#F44336", fg="white").grid(row=1, column=0, padx=10, pady=(15,10), sticky="ew")
        tk.Button(janela_rmv, text='Cancelar', font=("Verdana", 14), command=janela_rmv.destroy, bg="#235da3", fg="white").grid(row=1, column=1, padx=10, pady=(15,10), sticky="ew")

    id_lista = lista.selection()
    if id_lista:
        item_data = lista.item(id_lista)
        item_id = item_data["values"][0]

        if isinstance(item_id, int):
            abrir_janela_remover(int(item_id))
        else:
            messagebox.showerror("Erro", "ID inválido!")
    else:
        messagebox.showerror("Erro", "Nenhum item selecionado!")



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


# Busca ao detectar uma mudança na barra de busca
def handle_busca(event):
    busca_query = busca_entry.get()
    tipo = busca_dropdown.get()
    listar_itens_interface(buscar_item(busca_query, tipo))

# Habilita o estado do botão de remover item
def handle_botao_remover(event):
    if lista.selection():
        remover_button.config(state="normal")
    else:
        remover_button.config(state="disabled")

# Configuração do layout ajustável
for i in range(12):
    root.columnconfigure(i, minsize=90, weight=1)

root.rowconfigure(1,minsize=420, weight=1)

# Barra de busca
busca_entry = tk.Entry(root, bd=0, relief="flat")
busca_entry.grid(row=0, column=0, columnspan=10, padx=(5,0), pady=5, sticky="ew")

dropdown_options = ["Nome", "ID", "Descrição", "Categoria"]
busca_dropdown = ttk.Combobox(root, values=dropdown_options, state="readonly")
busca_dropdown.grid(row=0, column=10, columnspan=2, padx=(0,5), pady=5, sticky="ew")
busca_dropdown.set("Nome")

busca_entry.bind("<KeyRelease>", handle_busca)
busca_dropdown.bind("<KeyRelease>", handle_busca)

# Lista de Itens
colunas_lista = ["ID", "Nome", "Categoria", "Descrição", "Quantidade", "Disponível", "Estado", "Empréstimos"]
lista = ttk.Treeview(root, columns=colunas_lista, show="headings")
lista.grid(row=1, column=0, columnspan=12, sticky="nsew")

for it in colunas_lista:
    lista.heading(it, text=it)
    lista.column(it, anchor="center")

lista_rolagem_horizontal = ttk.Scrollbar(root, orient="horizontal", command=lista.xview)
lista.configure(xscrollcommand=lista_rolagem_horizontal.set)

lista_rolagem_horizontal.grid(row=2, column=0, columnspan=12, sticky="ew")

'''# Lista de Itens
lista = tk.Listbox(root, width=80, height=24)
lista.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

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
pessoa_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")'''

# Botões

tk.Button(root, text='Adicionar Item', font=("Verdana", 14), command=abrir_janela_add, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
tk.Button(root, text='Atualizar Item', font=("Verdana", 14), command=(), bg="#235da3", fg="white").grid(row=3, column=4, columnspan=4, padx=10, pady=10, sticky="ew")

remover_button = tk.Button(root, text='Remover Item', font=("Verdana", 14), command=remover_item_interface, bg="#F44336", fg="white")
remover_button.grid(row=3, column=8, columnspan=4, padx=10, pady=10, sticky="ew")
remover_button.config(state="disabled")
lista.bind("<<TreeviewSelect>>", handle_botao_remover)

tk.Button(root, text='Marcar como Emprestado', font=("Verdana", 14), command=marcar_emprestado_interface, bg="#235da3", fg="white").grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
tk.Button(root, text='Marcar como Devolvido', font=("Verdana", 14), command=marcar_devolvido_interface, bg="#235da3", fg="white").grid(row=4, column=4, columnspan=4, padx=10, pady=10, sticky="ew")
tk.Button(root, text='Marcar como Em Uso', font=("Verdana", 14), command=marcar_em_uso_interface, bg="#235da3", fg="white").grid(row=4, column=8, columnspan=4, padx=10, pady=10, sticky="ew")

# Botão para listar itens
tk.Button(root, text='Listar Todos os Itens', font=("Verdana", 14), command=lambda: listar_itens_interface(listar_itens()), bg="#235da3", fg="white").grid(row=12, column=0, columnspan=12, padx=10, pady=10, sticky="ew")

# Iniciar a interface
listar_itens_interface(listar_itens())
root.mainloop()