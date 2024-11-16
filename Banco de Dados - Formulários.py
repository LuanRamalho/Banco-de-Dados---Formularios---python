import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Função para criar a tabela se não existir
def create_table():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age TEXT,
            email TEXT,
            location TEXT,
            gender TEXT,
            hobbies TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar ou salvar usuário
def add_or_save_user():
    name = name_entry.get()
    age = age_entry.get()
    email = email_entry.get()
    location = location_entry.get()
    gender = gender_var.get()
    hobbies = hobbies_text.get("1.0", tk.END).strip()

    if not all([name, age, email, location, gender, hobbies]):
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Verifica se é uma edição ou um novo cadastro
    if edit_mode.get():
        selected_id = int(user_data_tree.item(user_data_tree.selection())['values'][0])
        cursor.execute('''
            UPDATE users SET name=?, age=?, email=?, location=?, gender=?, hobbies=? WHERE id=?
        ''', (name, age, email, location, gender, hobbies, selected_id))
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
    else:
        cursor.execute('''
            INSERT INTO users (name, age, email, location, gender, hobbies) 
            VALUES (?, ?, ?, ?, ?, ?)''', (name, age, email, location, gender, hobbies))
        messagebox.showinfo("Sucesso", "Dados enviados com sucesso!")
    
    conn.commit()
    conn.close()
    clear_form()
    refresh_user_data()
    edit_mode.set(False)
    add_save_button.config(text="Adicionar")

# Função para limpar o formulário
def clear_form():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    hobbies_text.delete("1.0", tk.END)
    gender_var.set(None)
    edit_mode.set(False)
    add_save_button.config(text="Adicionar")

# Função para buscar usuários
def search_users():
    search_term = search_entry.get().lower()
    refresh_user_data(search_term)

# Função para atualizar a tabela com dados de usuários
def refresh_user_data(search_term=""):
    for row in user_data_tree.get_children():
        user_data_tree.delete(row)

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM users'
    if search_term:
        query += ' WHERE name LIKE ? OR email LIKE ? OR location LIKE ?'
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    else:
        cursor.execute(query)
    
    for row in cursor.fetchall():
        user_data_tree.insert('', 'end', values=row)
    conn.close()

# Função para carregar dados para edição
def edit_user():
    try:
        selected_item = user_data_tree.selection()[0]
        values = user_data_tree.item(selected_item, 'values')
        
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])

        age_entry.delete(0, tk.END)
        age_entry.insert(0, values[2])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[3])

        location_entry.delete(0, tk.END)
        location_entry.insert(0, values[4])

        gender_var.set(values[5])

        hobbies_text.delete("1.0", tk.END)
        hobbies_text.insert("1.0", values[6])

        edit_mode.set(True)
        add_save_button.config(text="Salvar")

    except IndexError:
        messagebox.showwarning("Aviso", "Por favor, selecione um usuário para editar.")

# Função para excluir usuário
def delete_user():
    try:
        selected_item = user_data_tree.selection()[0]
        selected_id = int(user_data_tree.item(selected_item, 'values')[0])

        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (selected_id,))
        conn.commit()
        conn.close()

        user_data_tree.delete(selected_item)
        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
    except IndexError:
        messagebox.showwarning("Aviso", "Por favor, selecione um usuário para excluir.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Formulário de Usuário")
root.geometry("900x600")
root.config(bg="#eaeef1")

create_table()

# Variável para verificar o modo de edição
edit_mode = tk.BooleanVar(value=False)

# Frame do formulário
form_frame = tk.Frame(root, bg="white", padx=20, pady=20)
form_frame.pack(pady=20, padx=20)

tk.Label(form_frame, text="Nome:", bg="white").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(form_frame, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Idade:", bg="white").grid(row=1, column=0, sticky="w")
age_entry = tk.Entry(form_frame, width=40)
age_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Email:", bg="white").grid(row=2, column=0, sticky="w")
email_entry = tk.Entry(form_frame, width=40)
email_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Local de Residência:", bg="white").grid(row=3, column=0, sticky="w")
location_entry = tk.Entry(form_frame, width=40)
location_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Sexo:", bg="white").grid(row=4, column=0, sticky="w")
gender_var = tk.StringVar()
tk.Radiobutton(form_frame, text="Masculino", variable=gender_var, value="Masculino", bg="white").grid(row=4, column=1, sticky="w")
tk.Radiobutton(form_frame, text="Feminino", variable=gender_var, value="Feminino", bg="white").grid(row=4, column=1, sticky="e")

tk.Label(form_frame, text="Hobbies:", bg="white").grid(row=5, column=0, sticky="w")
hobbies_text = tk.Text(form_frame, height=5, width=37)
hobbies_text.grid(row=5, column=1, padx=10, pady=5)

# Botões de adicionar/salvar, editar e excluir
add_save_button = tk.Button(form_frame, text="Adicionar", command=add_or_save_user, bg="#4CAF50", fg="white")
add_save_button.grid(row=6, column=0, columnspan=2, pady=10)

edit_button = tk.Button(form_frame, text="Editar", command=edit_user, bg="#FF9800", fg="white")
edit_button.grid(row=7, column=0, columnspan=2, pady=10)

delete_button = tk.Button(form_frame, text="Excluir", command=delete_user, bg="#F44336", fg="white")
delete_button.grid(row=8, column=0, columnspan=2, pady=10)

# Frame da tabela de usuários
table_frame = tk.Frame(root, bg="#eaeef1")
table_frame.pack(pady=20, padx=20, fill="both", expand=True)

tk.Label(table_frame, text="Buscar:", bg="#eaeef1").grid(row=0, column=0, sticky="w")
search_entry = tk.Entry(table_frame, width=30)
search_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(table_frame, text="Buscar", command=search_users, bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5)

# Treeview com colunas configuradas para rolagem horizontal
columns = ("id", "name", "age", "email", "location", "gender", "hobbies")
user_data_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
user_data_tree.grid(row=1, column=0, columnspan=3, sticky="nsew")

# Configuração das colunas da tabela para habilitar rolagem horizontal
for col in columns:
    user_data_tree.heading(col, text=col.capitalize())
    user_data_tree.column(col, minwidth=150, width=300, stretch=True)  # Largura ajustável e expansível

# Barras de rolagem horizontal e vertical
x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=user_data_tree.xview)
user_data_tree.configure(xscrollcommand=x_scroll.set)
x_scroll.grid(row=2, column=0, columnspan=3, sticky="ew")

y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=user_data_tree.yview)
user_data_tree.configure(yscrollcommand=y_scroll.set)
y_scroll.grid(row=1, column=3, sticky="ns")

# Expansão do frame e da tabela
table_frame.grid_rowconfigure(1, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

# Carregar dados na tabela
refresh_user_data()

root.mainloop()
