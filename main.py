from datetime import datetime
import flet as ft
from queries import *


def main(page: ft.Page):
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    # Funciones
    def cargarCategoriaGasto():
        opciones.clear()
        categorias_db = listarCategorias()
        for cat in categorias_db:
            opcion = ft.dropdown.Option(
                key=str(cat["id"]),
                text=cat["nombre"]
            )
            opciones.append(opcion)
        page.update()

    # Segunda pestaña
    listaVista = ft.ListView(
        expand=True,
        spacing=10,
    )

    textoCategorias = ft.Text(value="GESTOR CATEGORIAS", size=25)
    containerCateg = ft.Container(
        content=ft.Row(
            controls=[textoCategorias],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    cuadroInput = ft.TextField(
        hint_text="nombre de la categoria",
        height=50,
        width=400,
        text_align=ft.TextAlign.CENTER
    )

    def verificarCat():
        if cuadroInput.value != "":
            insertarCategoria(cuadroInput.value)

            armarCategorias()
            cargarCategoriaGasto()
            
            cuadroInput.value = ""
            page.update()
            print("cargando categoria")
        else:
            print("invalido")

    botonIns = ft.IconButton(
        icon=ft.Icons.ADD,
        width=50,
        height=50,
        on_click=verificarCat,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(width=2, color=ft.Colors.GREY_700)
        ),
    )

    containerInput = ft.Container(
        padding=ft.Padding.symmetric(horizontal=5, vertical=60),
        content=ft.Row(
            controls=[cuadroInput, botonIns],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    textoMenu = ft.Text("CATEGORIAS CARGADAS", size=25)

    containerTextoMenu = ft.Container(
        content=ft.Row(
            controls=[textoMenu],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    # Funciones generales
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
        categorias_db = listarCategorias()
        valor = 0
        for cat in categorias_db:
            opcion = ft.Text(value=cat["nombre"], expand=True, size=16)
            botonModif = ft.Button(
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
            containerCategoria = ft.Container(
                width=700,
                padding=ft.Padding.symmetric(horizontal=70, vertical=5),
                content=ft.Row(
                    controls=[opcion, botonModif],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15
                ),
            )
            valor += 1
            listaVista.controls.append(containerCategoria)
        print(valor)

    page.update()

    contenedor_principalCategorias = ft.Container(
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

    # Primera pestaña
    textoEntrada = ft.Text(value="CARGAR DATOS", size=25)
    containerEntrada = ft.Container(
        content=ft.Row(
            controls=[textoEntrada],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    opciones = []
    dropCategoria = ft.Dropdown(
        label="categoria de gasto",
        options=opciones,
        width=300
    )

    cuadroFecha = ft.TextField(
        align=ft.Alignment.CENTER,
        hint_text="FECHA (DD/MM/YY)",
        width=500,
        text_align=ft.TextAlign.CENTER,
    )

    containerFecha = ft.Container(
        padding=ft.Padding.only(top=100),
        content=ft.Row(
            controls=[cuadroFecha],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    cuadroMonto = ft.TextField(
        align=ft.Alignment.CENTER,
        hint_text="MONTO DE GASTO",
        width=500,
        text_align=ft.TextAlign.CENTER,
    )

    containerMonto = ft.Container(
        content=ft.Row(
            controls=[cuadroMonto],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    cuadroNota = ft.TextField(
        align=ft.Alignment.CENTER,
        hint_text="OBSERVACIONES",
        width=500,
        text_align=ft.TextAlign.CENTER,
    )

    containerNota = ft.Container(
        padding=ft.Padding.only(bottom=100),
        content=ft.Row(
            controls=[cuadroNota],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    containerDropCategoria = ft.Container(
        padding=ft.Padding.only(bottom=100),
        content=ft.Row(
            controls=[dropCategoria],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
    )

    def fechaValida(fecha):
        if fecha == "":
            return False
        try:
            datetime.strptime(fecha, "%d/%m/%y")
            return True
        except ValueError:
            return False

    def cargarGasto(e):
        fecha = cuadroFecha.value
        monto = cuadroMonto.value
        observacion = cuadroNota.value
        categoria = dropCategoria.value
        print("carga de gasto iniciada")

        if categoria is not None and fechaValida(fecha) and monto != "":
            insertarGasto(monto, fecha, categoria)
            page.update()
            print("gasto insertado")

        else:
            stringError = ""
            if categoria is None:
                stringError += "categoria invalida-vacia"
            if not fechaValida(fecha):
                stringError += "/fecha invalida"
            if monto == "":
                stringError += "/monto invalido"
            cuadroError = ft.AlertDialog(
                title=ft.Text("Error de carga"),
                content=ft.Text(stringError),
                open=True,
            )
            page.add(cuadroError)

    botonSubir = ft.Button(
        content="Cargar Datos",
        width=300,
        height=50,
        icon=ft.Icons.MONETIZATION_ON_OUTLINED,
        align=ft.Alignment.CENTER_RIGHT,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=cargarGasto
    )

    contenedor_principal = ft.Container(
        width=1920,
        height=1080,
        padding=50,
        content=ft.Column(
            controls=[
                containerEntrada,
                containerFecha,
                containerMonto,
                containerNota,
                containerDropCategoria,
                botonSubir
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
    )

    # Tercera pestaña
    fecha_inicio_val = None
    fecha_fin_val = None

    txt_total = ft.Text(
        "$ 0.00", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400
    )
    txt_cantidad = ft.Text("0 registros", size=13, color=ft.Colors.GREY_400)

    tabla_gastos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Monto")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Categoría ID")),
        ],
        rows=[],
        expand=True,
    )

    txt_alerta = ft.Text("")

    def cerrar_alerta(e):
        dlg_alerta.open = False
        page.update()

    dlg_alerta = ft.AlertDialog(
        title=ft.Text("Aviso"),
        content=txt_alerta,
        actions=[
            ft.TextButton("Aceptar", on_click=cerrar_alerta)
        ],
    )
    page.dialog = dlg_alerta

    def mostrar_alerta(mensaje):
        txt_alerta.value = mensaje
        dlg_alerta.open = True
        page.update()

    txt_btn_inicio = ft.Text(
        "Desde", color=ft.Colors.WHITE, weight=ft.FontWeight.W_500
    )
    txt_btn_fin = ft.Text(
        "Hasta", color=ft.Colors.WHITE, weight=ft.FontWeight.W_500
    )

    def on_change_inicio(e):
        nonlocal fecha_inicio_val
        if date_picker_inicio.value:
            fecha_inicio_val = date_picker_inicio.value.strftime("%d-%m-%Y")
            txt_btn_inicio.value = date_picker_inicio.value.strftime("%d-%m-%Y")
            btn_inicio.update()

    def on_change_fin(e):
        nonlocal fecha_fin_val
        if date_picker_fin.value:
            fecha_fin_val = date_picker_fin.value.strftime("%d-%m-%Y")
            txt_btn_fin.value = date_picker_fin.value.strftime("%d-%m-%Y")
            btn_fin.update()

    date_picker_inicio = ft.DatePicker(on_change=on_change_inicio)
    date_picker_fin = ft.DatePicker(on_change=on_change_fin)

    page.overlay.extend([date_picker_inicio, date_picker_fin])

    # Apertura de selectores asignando .open = True
    def abrir_picker_inicio(e):
        date_picker_inicio.open = True
        page.update()

    def abrir_picker_fin(e):
        date_picker_fin.open = True
        page.update()

    # Botones 
    btn_inicio = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=ft.Colors.WHITE),
                txt_btn_inicio,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=ft.Colors.GREY_800,
        padding=12,
        border_radius=8,
        ink=True,
        on_click=abrir_picker_inicio,
    )

    btn_fin = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=ft.Colors.WHITE),
                txt_btn_fin,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=ft.Colors.GREY_800,
        padding=12,
        border_radius=8,
        ink=True,
        on_click=abrir_picker_fin,
    )

    def filtrar_gastos(e):
        if not fecha_inicio_val or not fecha_fin_val:
            mostrar_alerta("Por favor, selecciona ambas fechas.")
            return

        if fecha_inicio_val > fecha_fin_val:
            mostrar_alerta("La fecha de inicio no puede ser posterior a la fecha fin.")
            return

        gastos = listarGastosIntervalo(fecha_inicio_val, fecha_fin_val)

        tabla_gastos.rows.clear()
        total_acumulado = 0

        for g in gastos:
            total_acumulado += g["monto"]
            tabla_gastos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(g["id"]))),
                        ft.DataCell(ft.Text(f"${g['monto']:,.2f}")),
                        ft.DataCell(ft.Text(str(g["fecha"]))),
                        ft.DataCell(ft.Text(str(g["categoria_id"]))),
                    ]
                )
            )

        txt_total.value = f"$ {total_acumulado:,.2f}"
        txt_cantidad.value = f"{len(gastos)} gasto(s) encontrado(s)"
        page.update()

    btn_consultar = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.SEARCH, size=18, color=ft.Colors.WHITE),
                ft.Text("Consultar", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=ft.Colors.BLUE_600,
        padding=12,
        border_radius=8,
        ink=True,
        on_click=filtrar_gastos,
    )

    card_filtros = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Seleccionar Intervalo", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            btn_inicio,
                            ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.GREY_500),
                            btn_fin,
                            btn_consultar,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ]
            ),
            padding=15,
        )
    )

    card_kpi = ft.Card(
        content=ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Total del Período", size=12, color=ft.Colors.GREY_400),
                            txt_total,
                            txt_cantidad,
                        ],
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=42, color=ft.Colors.BLUE_400),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=20,
        )
    )

    card_tabla = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Detalle de Gastos", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.ListView(
                        controls=[tabla_gastos],
                        height=280,
                    ),
                ]
            ),
            padding=15,
        )
    )

    contenedorPrincipalGastos=ft.Column(
        controls=[card_filtros, card_kpi, card_tabla],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    cargarCategoriaGasto()
    armarCategorias()

    # Pestañas
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Tabs(
                selected_index=2,
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