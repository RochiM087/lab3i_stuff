from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified
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
    disponivel = Column(Integer, default=1)
    emprestado = Column(Boolean, default=False)
    em_uso = Column(Boolean, default=False)
    #horario_emprestimo = Column(DateTime)
    emprestimos = Column(JSON, default=[])

# Conexão com o banco de dados SQLite
engine = create_engine('sqlite:///catalogo.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Janelas abertas pelos botões
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

    tk.Button(janela_add, text='Adicionar Item', font=("Verdana", 14), command=lambda: [adicionar_item_interface(nome=nome_entry.get(),descricao=descricao_entry.get(),categoria=categoria_entry.get(),quantidade=quantidade_entry.get()), janela_add.destroy()], bg="#4CAF50", fg="white").grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    tk.Button(janela_add, text='Cancelar', font=("Verdana", 14), command=janela_add.destroy, bg="#F44336", fg="white").grid(row=5, column=3, columnspan=3, padx=10, pady=10, sticky="ew")

def abrir_janela_updt():
    id_lista = lista.selection()
    if not id_lista:
        messagebox.showerror("Erro", "Seleção inválida!")
        return
    
    item_data = lista.item(id_lista)
    item_id = item_data["values"][0]
    item = session.query(Item).filter_by(id=item_id).first()


    janela_updt = Toplevel(root)
    janela_updt.title("Atualizar Item")

    janela_updt.geometry("900x540+140+170")
    janela_updt.configure(background="#166ba9")

    for i in range(6):
        janela_updt.columnconfigure(i, minsize=150, weight=1)
    for i in range(8):
        janela_updt.rowconfigure(i, minsize=60, weight=1)

    
    tk.Label(janela_updt, text="ID", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_updt, text="Nome", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_updt, text="Descrição", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_updt, text="Categoria", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_updt, text="Quantidade máxima", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_updt, text="Quantidade disponível", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    id_entry = tk.Entry(janela_updt)
    id_entry.grid(row=0, column=2, columnspan=4, padx=10, pady=5, sticky="ew")
    id_entry.insert(0, item.id)
    id_entry.config(state="readonly")

    nome_entry = tk.Entry(janela_updt)
    nome_entry.grid(row=1, column=2, columnspan=4, padx=10, pady=5, sticky="ew")
    nome_entry.insert(0, item.nome)

    descricao_entry = tk.Entry(janela_updt)
    descricao_entry.grid(row=2, column=2, columnspan=4, padx=10, pady=5, sticky="ew")
    descricao_entry.insert(0, item.descricao)

    categoria_entry = tk.Entry(janela_updt)
    categoria_entry.grid(row=3, column=2, columnspan=4, padx=10, pady=5, sticky="ew")
    categoria_entry.insert(0, item.categoria)

    quantidade_entry = tk.Entry(janela_updt)
    quantidade_entry.grid(row=4, column=2, columnspan=4, padx=10, pady=5, sticky="ew")
    quantidade_entry.insert(0, item.quantidade)

    disponivel_entry = tk.Entry(janela_updt)
    disponivel_entry.grid(row=5, column=2, columnspan=4, padx=10, pady=5, sticky="ew")
    disponivel_entry.insert(0, item.disponivel)

    tk.Button(janela_updt, text='Atualizar Item', font=("Verdana", 14), command=lambda: [atualizar_item_interface(item_id = item.id, nome=nome_entry.get(),descricao=descricao_entry.get(),categoria=categoria_entry.get(),quantidade=quantidade_entry.get(), disponivel=disponivel_entry.get()), janela_updt.destroy()], bg="#4CAF50", fg="white").grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    tk.Button(janela_updt, text='Cancelar', font=("Verdana", 14), command=janela_updt.destroy, bg="#F44336", fg="white").grid(row=7, column=3, columnspan=3, padx=10, pady=10, sticky="ew")

def abrir_janela_emprestimo():
    id_lista = lista.selection()
    if not id_lista:
        messagebox.showerror("Erro", "Seleção inválida!")
        return
    
    item_data = lista.item(id_lista)
    item_id = item_data["values"][0]

    janela_emp = Toplevel(root)
    janela_emp.title("Emprestar Item")

    janela_emp.geometry("600x240+140+170")
    janela_emp.configure(background="#166ba9")

    for i in range(4):
        janela_emp.columnconfigure(i, minsize=150, weight=1)
        janela_emp.rowconfigure(i, minsize=60, weight=1)

    tk.Label(janela_emp, text="Nome da pessoa", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_emp, text="Quantidade", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    pessoa_entry = tk.Entry(janela_emp)
    pessoa_entry.grid(row=0, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    quantidade_entry = tk.Entry(janela_emp)
    quantidade_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    tk.Button(janela_emp, text='Emprestar', font=("Verdana", 14), command=lambda: [marcar_emprestado_interface(item_id, pessoa=pessoa_entry.get(), quantidade=quantidade_entry.get()), janela_emp.destroy()], bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    tk.Button(janela_emp, text='Cancelar', font=("Verdana", 14), command=janela_emp.destroy, bg="#F44336", fg="white").grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

def abrir_janela_devolucao():
    id_lista = lista.selection()
    if not id_lista:
        messagebox.showerror("Erro", "Seleção inválida!")
        return
    
    item_data = lista.item(id_lista)
    item_id = item_data["values"][0]
    item = session.query(Item).filter_by(id=item_id).first()


    janela_devol = Toplevel(root)
    janela_devol.title("Devolver Item")

    janela_devol.geometry("600x240+140+170")
    janela_devol.configure(background="#166ba9")

    for i in range(4):
        janela_devol.columnconfigure(i, minsize=150, weight=1)
        janela_devol.rowconfigure(i, minsize=60, weight=1)

    tk.Label(janela_devol, text="Nome da pessoa", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    tk.Label(janela_devol, text="Quantidade", font=("Verdana", 14), fg="white", bg="#235da3", borderwidth=2, relief="groove").grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    pessoa_dropdown_options = [emp["pessoa"] for emp in item.emprestimos]
    pessoa_dropdown = ttk.Combobox(janela_devol, values=pessoa_dropdown_options, state="readonly")
    pessoa_dropdown.grid(row=0, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    quantidade_entry = tk.Entry(janela_devol)
    quantidade_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    tk.Button(janela_devol, text='Emprestar', font=("Verdana", 14), command=lambda: [marcar_devolvido_interface(item_id, pessoa=pessoa_dropdown.get(), quantidade=quantidade_entry.get()), janela_devol.destroy()], bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    tk.Button(janela_devol, text='Cancelar', font=("Verdana", 14), command=janela_devol.destroy, bg="#F44336", fg="white").grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky="ew")


# Funções para gerenciar itens no banco de dados
def adicionar_item(nome, descricao, categoria, quantidade):
    item = Item(nome=nome, descricao=descricao, categoria=categoria, quantidade=quantidade, disponivel=quantidade)
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
    
def atualizar_item(item_id, nome, descricao, categoria, quantidade, disponivel):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        item.nome = nome
        item.descricao = descricao
        item.categoria = categoria
        item.quantidade = quantidade
        item.disponivel = disponivel

        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")


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
        if item.disponivel >= quantidade:
            item.disponivel -= quantidade
            if item.quantidade == 0:
                item.emprestado = True

            cur_emprestimos = item.emprestimos + [{
                "pessoa": pessoa,
                "quantidade": quantidade,
                "data": datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
            }]

            item.emprestimos = cur_emprestimos
            session.commit()
        else:
            messagebox.showerror("Erro", "Quantidade insuficiente!")
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

def marcar_devolvido(item_id, pessoa, quantidade):
    item = session.query(Item).filter_by(id=item_id).first()

    emprestado = next((emp for emp in item.emprestimos if emp["pessoa"] == pessoa), None)

    if emprestado:
        emp_index = item.emprestimos.index(emprestado)

        if emprestado["quantidade"] < quantidade:
            messagebox.showerror("Erro", "A quantidade excede o empréstimo!")
            return
        elif emprestado["quantidade"] == quantidade:
            item.emprestimos.pop(emp_index)
        else:
            emprestado["quantidade"] -= quantidade
            item.emprestimos[emp_index] = emprestado
        
        item.disponivel += quantidade

        flag_modified(item, "emprestimos")
        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

def marcar_em_uso(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        item.em_uso = not item.em_uso
        session.commit()
    else:
        messagebox.showerror("Erro", "Item não encontrado!")

# Listar itens
def listar_itens_interface(itens):
    lista.delete(*lista.get_children())

    if itens == []:
        return

    for it in itens:
        emp_fmt = ", ".join((f"{emp["pessoa"]} (x{emp["quantidade"]}) - {emp["data"]}" for emp in it.emprestimos))

        lista.insert("", "end", values=(
        it.id, # ID
        it.nome, # Nome
        it.categoria, # Categoria
        it.descricao, # Descrição
        str(it.disponivel) + "/" + str(it.quantidade), #Quantidade
        "Em Uso" if it.em_uso else "Livre", # Estado
        emp_fmt # Empréstimos
        ))

# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Catálogo de Itens Lab3i")
root.geometry("1080x700")  # Resolução base
root.configure(background="#166ba9")
root.resizable(True, True)  # Torna a janela redimensionável

# Função para adicionar item via interface
def adicionar_item_interface(nome, descricao, categoria, quantidade):
    if nome and quantidade.isdigit():
        adicionar_item(nome, descricao, categoria, int(quantidade))
        listar_itens_interface(listar_itens())
    else:
        messagebox.showerror("Erro", "Nome e quantidade são obrigatórios!")

# Função para atualizar item pela interface
def atualizar_item_interface(item_id, nome, descricao, categoria, quantidade, disponivel):
    if nome and quantidade.isdigit() and disponivel.isdigit():
        if int(quantidade) >= int(disponivel): 
            atualizar_item(item_id, nome, descricao, categoria, int(quantidade), int(disponivel))
            listar_itens_interface(listar_itens())
        else:
            messagebox.showerror("Erro", "Existem mais itens disponíveis do que o total!")
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
def marcar_emprestado_interface(item_id, pessoa, quantidade):

    if isinstance(item_id, int) and quantidade.isdigit() and pessoa:
        marcar_emprestado(int(item_id), int(quantidade), pessoa)
        listar_itens_interface(listar_itens())
    else:
        messagebox.showerror("Erro", "ID, quantidade e nome da pessoa são obrigatórios!")

# Função para marcar item como devolvido via interface
def marcar_devolvido_interface(item_id, pessoa, quantidade):

    if isinstance(item_id, int) and quantidade.isdigit() and pessoa:
        marcar_devolvido(item_id=int(item_id),pessoa=pessoa, quantidade=int(quantidade))
        listar_itens_interface(listar_itens())
    else:
        messagebox.showerror("Erro", "ID e quantidade inválidos!")

# Função para marcar item como em uso via interface
def marcar_em_uso_interface():
    id_lista = lista.selection()
    if id_lista:
        item_data = lista.item(id_lista)
        item_id = item_data["values"][0]
        if isinstance(item_id, int):
            marcar_em_uso(int(item_id))
            listar_itens_interface(listar_itens())
        else:
            messagebox.showerror("Erro", "ID inválido!")
    else:
        messagebox.showerror("Erro", "Seleção inválida!")

# Busca ao detectar uma mudança na barra de busca
def handle_busca(event):
    busca_query = busca_entry.get()
    tipo = busca_dropdown.get()
    listar_itens_interface(buscar_item(busca_query, tipo))

# Habilita o estado do botão de remover item
def handle_button_state(event):
    if lista.selection():
        atualizar_button.config(state="normal")
        remover_button.config(state="normal")
        emprestar_button.config(state="normal")
        devolver_button.config(state="normal")
        em_uso_button.config(state="normal")
    else:
        atualizar_button.config(state="disabled")
        remover_button.config(state="disabled")
        emprestar_button.config(state="disabled")
        devolver_button.config(state="disabled")
        em_uso_button.config(state="disabled")

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
colunas_lista = ["ID", "Nome", "Categoria", "Descrição", "Quantidade", "Estado", "Empréstimos"]
lista = ttk.Treeview(root, columns=colunas_lista, show="headings")
lista.grid(row=1, column=0, columnspan=12, sticky="nsew")

for it in colunas_lista:
    lista.heading(it, text=it)
    lista.column(it, anchor="center")

lista_rolagem_horizontal = ttk.Scrollbar(root, orient="horizontal", command=lista.xview)
lista.configure(xscrollcommand=lista_rolagem_horizontal.set)
lista.bind("<<TreeviewSelect>>", handle_button_state)

lista_rolagem_horizontal.grid(row=2, column=0, columnspan=12, sticky="ew")

# Botões
tk.Button(root, text='Adicionar Item', font=("Verdana", 14), command=abrir_janela_add, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

atualizar_button = tk.Button(root, text='Atualizar Item', font=("Verdana", 14), command=lambda: abrir_janela_updt(), bg="#235da3", fg="white")
atualizar_button.grid(row=3, column=4, columnspan=4, padx=10, pady=10, sticky="ew")
atualizar_button.config(state="disabled")

remover_button = tk.Button(root, text='Remover Item', font=("Verdana", 14), command=remover_item_interface, bg="#F44336", fg="white")
remover_button.grid(row=3, column=8, columnspan=4, padx=10, pady=10, sticky="ew")
remover_button.config(state="disabled")

emprestar_button = tk.Button(root, text='Marcar como Emprestado', font=("Verdana", 14), command=abrir_janela_emprestimo, bg="#235da3", fg="white")
emprestar_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
emprestar_button.config(state="disabled")

devolver_button =tk.Button(root, text='Marcar como Devolvido', font=("Verdana", 14), command=abrir_janela_devolucao, bg="#235da3", fg="white")
devolver_button.grid(row=4, column=4, columnspan=4, padx=10, pady=10, sticky="ew")
devolver_button.config(state="disabled")

em_uso_button = tk.Button(root, text='Marcar como Em Uso/Livre', font=("Verdana", 14), command=marcar_em_uso_interface, bg="#235da3", fg="white")
em_uso_button.grid(row=4, column=8, columnspan=4, padx=10, pady=10, sticky="ew")
em_uso_button.config(state="disabled")

# Botão para listar itens
tk.Button(root, text='Listar Todos os Itens', font=("Verdana", 14), command=lambda: listar_itens_interface(listar_itens()), bg="#235da3", fg="white").grid(row=12, column=0, columnspan=12, padx=10, pady=10, sticky="ew")

# Iniciar a interface
listar_itens_interface(listar_itens())
root.mainloop()