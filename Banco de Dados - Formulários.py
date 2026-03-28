import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Nome do arquivo de dados
DATA_FILE = 'user_data.json'

def init_json():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

    new_user = {
        "name": name,
        "age": age,
        "email": email,
        "location": location,
        "gender": gender,
        "hobbies": hobbies
    }

    data = load_data()
    current_idx = edit_mode.get()

    if current_idx != "None":
        idx = int(current_idx)
        data[idx] = new_user
        messagebox.showinfo("Sucesso", "Dados atualizados!")
    else:
        data.append(new_user)
        messagebox.showinfo("Sucesso", "Dados adicionados!")
    
    save_data(data)
    clear_form()
    refresh_cards()

def clear_form():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    hobbies_text.delete("1.0", tk.END)
    gender_var.set("")
    edit_mode.set("None")
    add_save_button.config(text="Adicionar")

def delete_user(index):
    if messagebox.askyesno("Confirmar", "Deseja excluir este usuário?"):
        data = load_data()
        data.pop(index)
        save_data(data)
        refresh_cards()

def prepare_edit(index):
    data = load_data()
    user = data[index]
    
    name_entry.delete(0, tk.END)
    name_entry.insert(0, user['name'])
    age_entry.delete(0, tk.END)
    age_entry.insert(0, user['age'])
    email_entry.delete(0, tk.END)
    email_entry.insert(0, user['email'])
    location_entry.delete(0, tk.END)
    location_entry.insert(0, user['location'])
    gender_var.set(user['gender'])
    hobbies_text.delete("1.0", tk.END)
    hobbies_text.insert("1.0", user['hobbies'])

    edit_mode.set(str(index))
    add_save_button.config(text="Salvar Alterações")

def refresh_cards(event=None):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    search_term = search_entry.get().lower()
    data = load_data()
    
    filtered_data = []
    for i, user in enumerate(data):
        if search_term and not any(search_term in str(val).lower() for val in user.values()):
            continue
        filtered_data.append((i, user))

    width = canvas.winfo_width()
    num_columns = 3 if width > 900 else 2

    for col in range(num_columns):
        scrollable_frame.grid_columnconfigure(col, weight=1, uniform="group1")

    for i, (original_idx, user) in enumerate(filtered_data):
        row, col = divmod(i, num_columns)
        
        card = tk.Frame(scrollable_frame, bg="white", highlightbackground="#d1d1d1", 
                        highlightthickness=1, padx=10, pady=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Nome e Info básica
        tk.Label(card, text=user['name'], font=("Arial", 11, "bold"), bg="white", wraplength=250).pack(anchor="w")
        tk.Label(card, text=f"{user['age']} anos | {user['gender']}", bg="white", font=("Arial", 9)).pack(anchor="w")
        
        # Localização e Email
        tk.Label(card, text=f"📍 {user['location']}", bg="white", fg="#555", font=("Arial", 8), wraplength=250).pack(anchor="w")
        tk.Label(card, text=f"✉ {user['email']}", bg="white", fg="#0066cc", font=("Arial", 8), wraplength=250).pack(anchor="w")
        
        # --- Hobbies (REINSERIDOS AQUI) ---
        tk.Label(card, text=f"Hobbies: {user['hobbies']}", bg="white", font=("Arial", 8, "italic"), 
                 wraplength=250, justify="left", fg="#333").pack(anchor="w", pady=(5,0))
        
        # Botões
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill="x", pady=(8,0))
        
        tk.Button(btn_frame, text="Editar", bg="#FF9800", fg="white", font=("Arial", 8),
                  command=lambda i=original_idx: prepare_edit(i)).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="Excluir", bg="#F44336", fg="white", font=("Arial", 8),
                  command=lambda i=original_idx: delete_user(i)).pack(side="left", expand=True, fill="x", padx=2)

# Interface Principal
root = tk.Tk()
root.title("Gerenciador de Usuários")
root.geometry("1000x750")
root.config(bg="#f0f2f5")

init_json()
edit_mode = tk.StringVar(value="None")

# Formulário (Layout reorganizado para liberar espaço)
form_container = tk.LabelFrame(root, text=" Cadastro / Edição ", bg="white", padx=10, pady=5)
form_container.pack(fill="x", padx=20, pady=10)

tk.Label(form_container, text="Nome:", bg="white").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(form_container, width=30)
name_entry.grid(row=0, column=1, pady=2, padx=5)

tk.Label(form_container, text="Idade:", bg="white").grid(row=0, column=2, sticky="w")
age_entry = tk.Entry(form_container, width=10)
age_entry.grid(row=0, column=3, pady=2, padx=5)

tk.Label(form_container, text="Email:", bg="white").grid(row=1, column=0, sticky="w")
email_entry = tk.Entry(form_container, width=30)
email_entry.grid(row=1, column=1, pady=2, padx=5)

tk.Label(form_container, text="Local:", bg="white").grid(row=1, column=2, sticky="w")
location_entry = tk.Entry(form_container, width=20)
location_entry.grid(row=1, column=3, pady=2, padx=5)

gender_var = tk.StringVar()
tk.Radiobutton(form_container, text="Masc", variable=gender_var, value="Masculino", bg="white").grid(row=2, column=1, sticky="w")
tk.Radiobutton(form_container, text="Fem", variable=gender_var, value="Feminino", bg="white").grid(row=2, column=1, sticky="e")

tk.Label(form_container, text="Hobbies:", bg="white").grid(row=2, column=2, sticky="nw")
hobbies_text = tk.Text(form_container, height=2, width=30)
hobbies_text.grid(row=2, column=3, pady=2, padx=5)

add_save_button = tk.Button(form_container, text="Adicionar", command=add_or_save_user, bg="#4CAF50", fg="white")
add_save_button.grid(row=3, column=0, columnspan=4, pady=5, sticky="ew")

# Busca
search_frame = tk.Frame(root, bg="#f0f2f5")
search_frame.pack(fill="x", padx=20)
tk.Label(search_frame, text="Buscar:", bg="#f0f2f5").pack(side="left")
search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", fill="x", expand=True, padx=5)
search_entry.bind("<KeyRelease>", refresh_cards)

# Área de Cards com Scroll
container = tk.Frame(root, bg="#f0f2f5")
container.pack(fill="both", expand=True, padx=20, pady=10)

canvas = tk.Canvas(container, bg="#f0f2f5", highlightthickness=0)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f2f5")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_canvas_configure(event):
    canvas.itemconfig(1, width=event.width)
    refresh_cards()

canvas.bind("<Configure>", on_canvas_configure)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

root.mainloop()
