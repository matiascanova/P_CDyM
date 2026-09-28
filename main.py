import flet as ft
from datetime import datetime
from queries import *

def main(page: ft.Page):
    page.padding=0
    page.theme_mode = ft.ThemeMode.LIGHT


    #segunda pestaña
    listaVista=ft.ListView(
        expand=True,
        spacing=10,
    )

    textoCategorias=ft.Text(value="GESTOR CATEGORIAS",size=25)
    containerCateg=ft.Container(
        content=ft.Row(
            controls=[textoCategorias],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    cuadroInput=ft.TextField(
            hint_text="nombre de la categoria",
            height=50,
            width=400,
            text_align=ft.TextAlign.CENTER
    )

    def verificarCat():
        if cuadroInput.value!="":
            insertarCategoria(cuadroInput.value)
            armarCategorias()
            cargarCategoriaGasto()
            print("cargando categoria")
        else:
            print("invalido")  
    
    botonIns=ft.IconButton(
        icon=ft.Icons.ADD,
        width=50,
        height=50,
        on_click=verificarCat,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(width=2, color=ft.Colors.GREY_700)
        ),
    )

    containerInput=ft.Container(
        padding=ft.Padding.symmetric(horizontal=5, vertical=60),
        content=ft.Row(
            controls=[cuadroInput,botonIns],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    textoMenu=ft.Text("CATEGORIAS CARGADAS", size=25)

    containerTextoMenu=ft.Container(
        content=ft.Row(
            controls=[textoMenu],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    #funciones generales
    def borrarCat(e):
        cat_id = e.control.data 
        try:
            eliminarCategoria(cat_id)
            armarCategorias()
            cargarCategoriaGasto()
        except Exception:
            page.snack_bar = ft.SnackBar(
                ft.Text("No se puede borrar: la categoría tiene gastos registrados.")
            )
            page.snack_bar.open = True
            page.update()

    def armarCategorias():
        listaVista.controls.clear()
        categorias_db=listarCategorias()
        valor=0 
        for cat in categorias_db:
            opcion=ft.Text(value=cat["nombre"],expand=True,size=16)
            botonModif=ft.Button(
                content="borrar",
                width=100,
                height=30,
                data=(cat["id"]),
                on_click=borrarCat,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    side=ft.BorderSide(width=2, color=ft.Colors.GREY_700)
                ),
            )
            containerCategoria=ft.Container(
                width=700,
                padding=ft.Padding.symmetric(horizontal=70, vertical=5),
                content=ft.Row(
                    controls=[opcion,botonModif],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15
                ),
            )
            valor+=1
            listaVista.controls.append(containerCategoria)
        print(valor)
    page.update()

    contenedor_principalCategorias=ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                    containerCateg,
                    ft.Divider(),
                    containerInput,
                    ft.Divider(),
                    containerTextoMenu,
                    listaVista
                    ],
        ),
    )

    #primera pestaña

    textoEntrada=ft.Text(value="CARGAR DATOS",size=25)
    containerEntrada=ft.Container(
        content=ft.Row(
            controls=[textoEntrada],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )
    opciones=[]
    dropCategoria=ft.Dropdown(
        label="categoria de gasto",
        options=opciones,
        width=300
    )
    def cargarCategoriaGasto():
        categorias_db=listarCategorias()
        for cat in categorias_db:
            opcion=ft.dropdown.Option(
                key=str(cat["id"]),
                text=cat["nombre"]
            )
            opciones.append(opcion)

    cuadroFecha=ft.TextField(
        align=ft.Alignment.CENTER,
        hint_text="FECHA (DD/MM/YY)",
        width=500,
        text_align=ft.TextAlign.CENTER,
    )

    containerFecha=ft.Container(
        padding=ft.Padding.only(top=100),
        content=ft.Row(
            controls=[cuadroFecha],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )
    cuadroMonto=ft.TextField(
        align=ft.Alignment.CENTER,
        hint_text="MONTO DE GASTO",
        width=500,
        text_align=ft.TextAlign.CENTER,
    )
    containerMonto=ft.Container(
         content=ft.Row(
            controls=[cuadroMonto],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )
    cuadroNota=ft.TextField(
        align=ft.Alignment.CENTER,
        hint_text="OBSERVACIONES",
        width=500,
        text_align=ft.TextAlign.CENTER,
    )
    containerNota=ft.Container(
        padding=ft.Padding.only(bottom=100),
         content=ft.Row(
            controls=[cuadroNota],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )
    
    containerDropCategoria=ft.Container(
        padding=ft.Padding.only(bottom=100),
         content=ft.Row(
            controls=[dropCategoria],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    def fechaValida(fecha):
        if fecha=="":
            return False
        try:
            datetime.strptime(fecha, "%d/%m/%y")
            return True
        except ValueError:
            return False

    def cargarGasto(e):
        print("carga de gasto iniciada")
        fecha=cuadroFecha.value
        monto=cuadroMonto.value
        observacion=cuadroNota.value
        categoria=dropCategoria.value

        if categoria != None and fechaValida(fecha) and monto!="":
            insertarGasto(monto,fecha,categoria)
            print("gasto insertado")
        else:
            stringError=""
            if categoria==None:
                stringError+= ("categoria invalida-vacia")
            if not fechaValida(fecha):
                stringError+= ("/fecha invalida")
            if monto=="":
                stringError+= ("/monto invalido")
            cuadroError=ft.AlertDialog(
                title=ft.Text("Error de carga"),
                content=ft.Text(stringError),
                open=True,
            )
            page.add(cuadroError)

    botonSubir=ft.Button(content="Cargar Datos",
            width=300,
            height=50,
            icon=ft.Icons.MONETIZATION_ON_OUTLINED,
            align=ft.Alignment.CENTER_RIGHT,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=cargarGasto
        )

    contenedor_principal=ft.Container(
        width=1920,
        height=1080,
        padding=50,
        content=ft.Column(
            controls=[containerEntrada,containerFecha,containerMonto,containerNota,containerDropCategoria,botonSubir],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
    )

    #tercera pestaña
    textoCategorias=ft.Text(value="ANALISIS GASTOS",size=25)
    containerTextoCategorias=ft.Container(
        content=ft.Row(
            controls=[textoCategorias],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )
    listaVista_gastos=ft.ListView(
        expand=True,
        spacing=10,
        padding=15
    )

    def armarGastos():
        listaVista_gastos.controls.clear()
        gastos = listarGastos()

        for g in gastos:
            nombre_cat = obtenerNombreCategoria(g["categoria_id"]) or "Sin Categoría"
            textoFecha = ft.Text(g["fecha"], size=16)
            textoCat = ft.Text(nombre_cat, size=16, expand=True)
            textoMonto = ft.Text(f"${g['monto']}", size=16, color=ft.Colors.GREEN_700)

            # Función de borrado corregida
            def borrarGasto(e, gasto_id=g["id"]):
                eliminarGasto(gasto_id)
                armarGastos() # 1. Elimina de SQLite

            btnBorrar = ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINED,
                icon_color=ft.Colors.RED_400,
                tooltip="Eliminar gasto",
                on_click=borrarGasto,
            )
    
            filaGasto = ft.Container(
                padding=ft.Padding.symmetric(horizontal=15, vertical=10),
                border_radius=8,
                content=ft.Row(
                    controls=[textoFecha, textoCat, textoMonto, btnBorrar],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
            listaVista_gastos.controls.append(filaGasto)
    page.update()

    contenedorPrincipalGastos=ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
            containerTextoCategorias,
            listaVista_gastos
            ],
        ),   
    )


    cargarCategoriaGasto(),
    armarCategorias(),
    #pestañas
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Tabs(
                selected_index=1,
                length=3,
                expand=True,
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.TabBar(
                            tabs=[
                                ft.Tab(label="cargar gastos", icon=ft.Icons.ATTACH_MONEY),
                                ft.Tab(label="agregar/modif. categorias", icon=ft.Icons.CATEGORY),
                                ft.Tab(label="ver/modif. gastos", icon=ft.Icons.TABLE_VIEW),
                            ]
                        ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                contenedor_principal,
                                contenedor_principalCategorias,
                                contenedorPrincipalGastos,
                            ],
                        ),
                    ],
                ),
            ),
        )
    )

ft.run(main)