"""
Rutas (vistas) de la Tienda Virtual.

Las consultas de productos se realizan mediante SQLAlchemy.
"""

from flask import Blueprint, render_template, request

from .models import Producto, Categoria


main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Página principal: catálogo de productos desde la base de datos."""

    # Lee el parámetro ?categoria= de la URL
    categoria_id = request.args.get("categoria", type=int)

    # Filtrar por categoría o mostrar todos los productos
    if categoria_id:
        productos = Producto.query.filter_by(
            categoria_id=categoria_id
        ).all()
    else:
        productos = Producto.query.all()

    # Consultar todas las categorías ordenadas por nombre
    categorias = Categoria.query.order_by(
        Categoria.nombre
    ).all()

    # Mostrar la página principal
    return render_template(
        "index.html",
        productos=productos,
        categorias=categorias,
        categoria_id=categoria_id
    )


@main.route("/producto/<sku>")
def detalle(sku):
    """Detalle de un producto, buscado por su SKU."""

    # Buscar el producto por SKU
    producto = Producto.query.filter_by(
        sku=sku
    ).first_or_404()

    # Mostrar el detalle
    return render_template(
        "detalle.html",
        producto=producto
    )


@main.route("/categorias")
def categorias():
    """Lista de categorías con la cantidad de productos."""

    # Consultar categorías ordenadas por nombre
    categorias = Categoria.query.order_by(
        Categoria.nombre
    ).all()

    # Mostrar las categorías
    return render_template(
        "categorias.html",
        categorias=categorias
    )
