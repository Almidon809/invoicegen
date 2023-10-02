# invoicegen
generador de factura

mi correo: javpaiewonsky@gmail.com

tengo un script de python tkinter sqlite3, que me sale un codigo de error que sale por aqui abajo y mi intencion que quiero tratar de hacer las piezas que estan en la base de datos pueda calcular su precio con su impuesto con la cantidad que se quiera consumir que esta en esa base de datos para que pueda aparecer en el template que se renderiza
voy a compartir el script, la base de datos y el template de docx para poder solucionar dicho problema

PS G:\invoice\fix - Copy\puebas\prueba3> & C:/Users/user/AppData/Local/Microsoft/WindowsApps/python3.11.exe "g:/invoice/fix - Copy/puebas/prueba3/despacho.py"
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.1520.0_x64__qbz5n2kfra8p0\Lib\tkinter\__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "g:\invoice\fix - Copy\puebas\prueba3\despacho.py", line 204, in generate_invoice
    precio_total = round(cnt * (precio + impuesto), 2)
                                ^^^^^^
UnboundLocalError: cannot access local variable 'precio' where it is not associated with a value

