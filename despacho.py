import tkinter
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from docxtpl import DocxTemplate
import os
import datetime
import sqlite3 
import subprocess


#--------------------------------------------PRINTER OPTION---------------------------------------------------------#


#-------------------------------------------------------------------------------------------------------------------#

def crear_db():
    # Crear la carpeta DB si no existe
    if not os.path.exists("DB"):
        os.makedirs("DB")
    
    # Crear la base de datos data.db si no existe
    if not os.path.exists("DB/data.db"):
        conexion = sqlite3.connect('DB/data.db')
        cursor = conexion.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS factura(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT NOT NULL,
                            apellido TEXT NOT NULL,
                            telefono TEXT NOT NULL,
                            turno TEXT NOT NULL,
                            fecha TEXT NOT NULL,
                            categoria TEXT NOT NULL,
                            referencia TEXT NOT NULL,
                            descripcion TEXT NOT NULL,
                            cantidad INTEGER NOT NULL)''')
        
        conexion.commit()
        conexion.close()


def crear_tablaF():
    conn = sqlite3.connect('DB/data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS piezas (referencia TEXT, descripcion TEXT cantidad INTEGER, precio REAL, impuesto REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS facturas (referencia TEXT, descripcion TEXT, cantidad INTEGER, precio_total REAL, turno TEXT)")
    conn.commit()
    conn.close()


def clear_item():
    cantidad_Spinbox.delete(0, tkinter.END)
    cantidad_Spinbox.insert(0, "1")

...

# Llamar la función para crear la base de datos
crear_db()

#-------------------------contadores-------------------------#
def verificar_tablas():
    con = sqlite3.connect("DB/data.db")
    cursor = con.cursor()
    # Verificar y crear las tablas si no existen
    cursor.execute("CREATE TABLE IF NOT EXISTS Contadores (categoria TEXT PRIMARY KEY, contador INTEGER)")
    con.commit()

def obtener_contadores():
    con = sqlite3.connect("DB/data.db")
    cursor = con.cursor()
    # Recuperar los valores de los contadores desde la base de datos
    cursor.execute("SELECT categoria, contador FROM Contadores")
    contadores = cursor.fetchall()
    contador_dict = {}
    for categoria, contador in contadores:
        contador_dict[categoria] = contador
    return contador_dict

def actualizar_contador(categoria, contador):
    con = sqlite3.connect("DB/data.db")
    cursor = con.cursor()
    # Actualizar el valor del contador en la base de datos
    cursor.execute("INSERT OR REPLACE INTO Contadores (categoria, contador) VALUES (?, ?)", (categoria, contador))
    con.commit()

#-------------------------contadores-------------------------#




def crear_tablaP():
    conn = sqlite3.connect('DB/data.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS piezas (referencia TEXT descripcion TEXT, cantidad INTEGER, precio REAL, impuesto REAL)")
    conn.commit()
    conn.close()

def clear_item():
    cantidad_Spinbox.delete(0, tkinter.END)
    cantidad_Spinbox.insert(0, "1")

invoice_list = []
def add_item():
    cnt = int(cantidad_Spinbox.get())
    ref = referencia_Entry.get()
    desc = Descripcion_Entry.get()

    # Obtener el precio y el impuesto de la base de datos
    conn = sqlite3.connect('DB/data.db')
    c = conn.cursor()
    c.execute("SELECT precio, impuesto FROM piezas WHERE referencia=?", (ref,))
    result = c.fetchone()

    if result:
        precio, impuesto = result
        importe = cnt*(precio + impuesto)
        invoice_item = [cnt, ref, desc, importe]
        tree.insert('', 0, values=invoice_item)
        clear_item()
        invoice_list.append(invoice_item)
    else:
        messagebox.showerror("Error", "Referencia de pieza no encontrada.")

    conn.close()

def new_invoice():
    numero_emp_Entry.delete(0, tkinter.END)
    nombre_emp_Entry.delete(0, tkinter.END)
    OT_Entry.delete(0, tkinter.END)
    clear_item()
    tree.delete(*tree.get_children())

    invoice_list.clear()

def actualizar_contador(categoria, contador):
    conexion = sqlite3.connect('DB/data.db')
    cursor = conexion.cursor()
    # Actualizar el valor del contador en la base de datos
    cursor.execute("INSERT OR REPLACE INTO Contadores (categoria, contador) VALUES (?, ?)", (categoria, contador))
    conexion.commit()


def generate_invoice():
    doc = DocxTemplate("Invoice_templatev6.docx")
    name = numero_emp_Entry.get()+"-"+nombre_emp_Entry.get()
    ot = OT_Entry.get()
    transa = NumTransa_Entry.get()
    global taller_counter, servicio_counter, pintura_counter, motor_counter, material_gastable_counter, Control_Herramientas_counter

    con = sqlite3.connect("DB/data.db")
    cursor = con.cursor()

    categoria = categoria_combobox.get()
    contadores = obtener_contadores()


    if categoria == "Taller de Vehículo":
        contadores["Taller de Vehículo"] += 1
        turno = f"T-{str(contadores['Taller de Vehículo']).zfill(4)}"
    elif categoria == "Servicio Expreso":
        contadores["Servicio Expreso"] += 1
        turno = f"SE-{str(contadores['Servicio Expreso']).zfill(4)}"
    elif categoria == "Pintura":
        contadores["Pintura"] += 1
        turno = f"P-{str(contadores['Pintura']).zfill(4)}"
    elif categoria == "Taller de Motor":
        contadores["Taller de Motor"] += 1
        turno = f"M-{str(contadores['Taller de Motor']).zfill(4)}"
    elif categoria == "Material Gastable":
        contadores["Material Gastable"] += 1
        turno = f"MG-{str(contadores['Material Gastable']).zfill(8)}"
    elif categoria == "Control de Herramientas":
        contadores["Control de Herramientas"] += 1
        turno = f"HC-{str(contadores['Control de Herramientas']).zfill(8)}"
    else:
        turno = "Error"

    actualizar_contador(categoria, contadores[categoria])



    if not os.path.exists("DOC"):
        os.makedirs("DOC")

    now = datetime.datetime.now()
    fecha = now.strftime("%d/%m/%Y %H:%M:%S")

    doc.render({"name":name,
                "ot": ot,
                "invoice_list": invoice_list,
                "turno": turno,
                "fecha": fecha,
                "transa": transa,
                })
    
    doc_name = f"{turno}_{name}_{datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S')}" + ".docx"
    doc_path = os.path.join("DOC", doc_name)
    doc.save(doc_path)
    
    for item in invoice_list:
        cnt, ref, desc, precio_total = item
        precio_total = round(cnt * (precio + impuesto), 2)
        referencia = item[1]
        descripcion = item[2]
        cantidad = item[0]
        
        # Verificar si hay suficientes piezas en existencia
        conn = sqlite3.connect('DB/data.db')
        c = conn.cursor()
        c.execute("SELECT referencia, descripcion, cantidad, precio, impuesto FROM piezas WHERE referencia=?", (referencia,))
        result = c.fetchone()

        if result is not None:
            referencia, descripcion, cantidad_existente, precio, impuesto = result

            if cantidad <= cantidad_existente:
                precio_total = round(cantidad * (precio + impuesto), 2)

                nueva_cantidad = cantidad_existente - cantidad
                c.execute("UPDATE piezas SET cantidad=? WHERE referencia=?", (nueva_cantidad, referencia))
                conn.commit()

                c.execute("INSERT INTO facturas (referencia, descripcion, cantidad, precio_total, turno) VALUES (?, ?, ?, ?, ?)",
                          (referencia, descripcion, cantidad, precio_total, turno))
                conn.commit()

                messagebox.showinfo("Éxito", "Factura generada correctamente.")
            else:
                messagebox.showerror("Error", "No hay suficientes piezas en existencia.")
        else:
            messagebox.showerror("Error", "Referencia de pieza no encontrada.")

        conn.close()

verificar_tablas()
contadores = obtener_contadores()
taller_counter = contadores.get("Taller de Vehículo", 0)
servicio_counter = contadores.get("Servicio Expreso", 0)
pintura_counter = contadores.get("Pintura", 0)
motor_counter = contadores.get("Taller de Motor", 0)
material_gastable_counter = contadores.get("Material Gastable", 0)
Control_Herramientas_counter = contadores.get("Control de Herramientas", 0)







# ----------------------- productos ----------------------- #




# ----------------------- xxxxxxxxx ----------------------- #
window = Tk()
window.title("listado empleado")
window.geometry("1000x800")



notebook = ttk.Notebook(window)

tab1 = Frame(notebook)
tab2 = Frame(notebook)
tab3 = Frame(notebook)
tab4 = Frame(notebook)
tab5 = Frame(notebook)
tab6 = Frame(notebook)
tab7 = Frame(notebook)
tab8 = Frame(notebook)


notebook.add(tab1, text="Generar Ticket")
notebook.add(tab2, text="Buscar Ticket")
notebook.add(tab3, text="Añadir empleado")
notebook.add(tab4, text="Consultar empleado")
notebook.add(tab5, text="Consultar Facturas")
notebook.add(tab6, text="Entradas de Productos (Nueva Referencia)")
notebook.add(tab7, text="Consultar piezas")
notebook.add(tab8, text="Transferencia de piezas")
notebook.pack(expand=True, fill="both")



# --------------------------------------- Tab 1  --------------------------------------- #



numero_emp_LB = tkinter.Label(tab1, text="Numero De Empleado")
numero_emp_LB.place(relx=0.05, rely=0.01)
numero_emp_Entry = tkinter.Entry(tab1)
numero_emp_Entry.place(relx=0.05, rely=0.06)

nombre_emp_Label = tkinter.Label(tab1, text="Tecnico")
nombre_emp_Label.place(relx=0.35, rely=0.01)
nombre_emp_Entry = tkinter.Entry(tab1)
nombre_emp_Entry.place(relx=0.35, rely=0.06)

OT_Label = tkinter.Label(tab1, text="Numero De OT")
OT_Label.place(relx=0.65, rely=0.01)
OT_Entry = tkinter.Entry(tab1)
OT_Entry.place(relx=0.65, rely=0.06)

cantidad_Label = tkinter.Label(tab1, text="Cnt")
cantidad_Label.place(relx=0.05, rely=0.09)
cantidad_Spinbox = tkinter.Spinbox(tab1, from_=1, to=9999999)
cantidad_Spinbox.place(relx=0.05, rely=0.12)

referencia_Label = tkinter.Label(tab1, text="Referencia")
referencia_Label.place(relx=0.35, rely=0.09)
referencia_Entry = tkinter.Entry(tab1)
referencia_Entry.place(relx=0.35, rely=0.12)

NumTransa_Label = tkinter.Label(tab1, text="Numero de Transaccion")
NumTransa_Label.place(relx=0.345, rely=0.145)
NumTransa_Entry = tkinter.Entry(tab1)
NumTransa_Entry.place(relx=0.35, rely=0.17)

Descripcion_Label = tkinter.Label(tab1, text="Descripcion")
Descripcion_Label.place(relx=0.65, rely=0.09)
Descripcion_Entry = tkinter.Entry(tab1)
Descripcion_Entry.place(relx=0.65, rely=0.12)

categorias = ["Taller de Vehículo", "Servicio Expreso", "Pintura", "Taller de Motor", "Material Gastable", "Control de Herramientas"]
categoria_combobox = ttk.Combobox(tab1, values=categorias)
categoria_combobox.place(relx=0.05, rely=0.17)
categoria_combobox.current(0)

add_item_button = tkinter.Button(tab1, text="Añadir producto", command=add_item)
add_item_button.place(relx=0.8, rely=0.11)

scrollbarx1 = Scrollbar(tab1,orient=HORIZONTAL)
scrollbary1 = Scrollbar(tab1, orient=VERTICAL)

columns = ('cnt','ref','desc')
tree = ttk.Treeview(tab1, columns=columns, show="headings")
tree.heading('cnt', text="Cnt")
tree.heading('ref', text="Referencia")
tree.heading('desc', text="Descripcion")
tree.place(relx=0.05, rely=0.21, relwidth=0.9, relheight=0.25)
tree.configure(yscrollcommand=scrollbary1.set, xscrollcommand=scrollbarx1.set)
tree.configure(selectmode="extended")
scrollbarx1.configure(command=tree.xview)
scrollbary1.configure(command=tree.yview)
scrollbarx1.place(relx=0.05, rely=0.47, relwidth=0.9, height=22)
scrollbary1.place(relx=0.95, rely=0.21, width=22, relheight=0.25)

guardar_factura_button = tkinter.Button(tab1, text="Generar Factura", command=generate_invoice)
guardar_factura_button.place(relx=0.05, rely=0.52, relwidth=0.45)
nueva_factura_button = tkinter.Button(tab1, text="Nueva Factura", command=new_invoice)
nueva_factura_button.place(relx=0.5, rely=0.52, relwidth=0.45)



version_Label = tkinter.Label(tab1, text="Perseo v1.3.8", font=('Calibri (Body)',10))
version_Label.place(relx=0.9, rely=0.96)




# --------------------------------------- window --------------------------------------- #

crear_tablaF()

crear_tablaP()


verificar_tablas()


window.mainloop()