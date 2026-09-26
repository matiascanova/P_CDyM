import flet as ft
from datetime import datetime
from queries import (
    insertarCategoria,
    listarCategorias,
    insertarGasto,
    listarGastosIntervalo
)

def main(page: ft.Page):
    page.title = "Gestor de Gastos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # ----------------------------------------------------
    # SECCIÓN 1: GESTIÓN DE CATEGORÍAS
    # ----------------------------------------------------
    txt_nombre_categoria = ft.TextField(
        label="Nombre de la categoría", 
        expand=True
    )
    lista_categorias_view = ft.ListView(expand=True, spacing=10)

    def cargar_categorias():
        lista_categorias_view.controls.clear()
        categorias = listarCategorias()
        for cat in categorias:
            lista_categorias_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon("category"),  # <--- Uso de string directo
                    title=ft.Text(cat["nombre"]),
                    subtitle=ft.Text(f"ID: {cat['id']}")
                )
            )
        page.update()

    def guardar_categoria_click(e):
        if txt_nombre_categoria.value:
            insertarCategoria(txt_nombre_categoria.value)
            txt_nombre_categoria.value = ""
            cargar_categorias()
            actualizar_dropdown_categorias()
            page.open(ft.SnackBar(ft.Text("Categoría creada con éxito")))
            page.update()

    btn_guardar_cat = ft.Button("Guardar Categoría", on_click=guardar_categoria_click)

    vista_categorias = ft.Column(
        controls=[
            ft.Text("Nueva Categoría", size=20, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[txt_nombre_categoria, btn_guardar_cat]),
            ft.Divider(),
            ft.Text("Categorías Existentes", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(content=lista_categorias_view, height=200)
        ]
    )
    # Carga inicial
    cargar_categorias()

if __name__ == "__main__":
    ft.run(main)