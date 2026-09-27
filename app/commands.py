"""
Comandos personalizados de terminal (Flask CLI).

Permiten ejecutar tareas administrativas desde la terminal.
"""

import json
import os

import click

from .extensions import db
from .models import Categoria, Producto


RUTA_PRODUCTOS = os.path.join(
    os.path.dirname(__file__),
    "data",
    "productos.json"
)


def registrar_comandos(app):
    """Asocia los comandos a la aplicación Flask recibida."""

    @app.cli.command("init-db")
    def init_db():
        """Crea todas las tablas definidas en models.py."""
        db.create_all()
        click.echo("Base de datos inicializada correctamente.")

    @app.cli.command("reset-db")
    def reset_db():
        """Borra y vuelve a crear todas las tablas."""
        db.drop_all()
        db.create_all()
        click.echo("Base de datos reiniciada correctamente.")

    @app.cli.command("seed-db")
    def seed_db():
        """Carga los productos de productos.json en la base de datos."""

        # Leer el archivo JSON
        with open(RUTA_PRODUCTOS, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        productos_cargados = 0

        # Insertar categorías y productos
        for item in datos:

            # Buscar si la categoría ya existe
            categoria = Categoria.query.filter_by(
                nombre=item["categoria"]
            ).first()

            # Si no existe, crearla
            if categoria is None:
                categoria = Categoria(nombre=item["categoria"])
                db.session.add(categoria)
                db.session.flush()

            # Evitar productos duplicados por SKU
            producto_existente = Producto.query.filter_by(
                sku=item["sku"]
            ).first()

            if producto_existente:
                continue

            # Crear el producto
            producto = Producto(
                sku=item["sku"],
                marca=item["marca"],
                nombre=item["nombre"],
                precio=item["precio"],
                foto=item["foto"],
                stock=item["stock"],
                activo=item["activo"],
                categoria_id=categoria.id
            )

            db.session.add(producto)
            productos_cargados += 1

        # Guardar todos los cambios
        db.session.commit()

        click.echo(
            f"Se cargaron {productos_cargados} productos correctamente."
        )
