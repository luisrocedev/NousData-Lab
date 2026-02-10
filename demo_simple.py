#!/usr/bin/env python3
"""
Demo simple del Framework de Acceso a Datos
"""

from data_access_framework import create_framework
from data_access_framework.models import Book, Author

def main():
    print("🚀 Iniciando demo del framework...")

    # Crear framework con SQLite
    framework = create_framework(data_format='sqlite')

    # Obtener repositorios
    book_repo = framework.get_repository('Book')
    author_repo = framework.get_repository('Author')

    print("✅ Framework inicializado")

    # Crear y guardar autor
    autor = Author(
        name='Demo',
        last_name='Author',
        nationality='Español'
    )
    author_repo.save(autor)
    print(f"✅ Autor guardado: {autor.full_name}")

    # Crear y guardar libro
    libro = Book(
        title='Libro Demo',
        author_id=autor.id,
        isbn='9788437604947',  # ISBN válido
        genre='Demo',
        pages=100
    )
    book_repo.save(libro)
    print(f"✅ Libro guardado: {libro.title}")

    # Mostrar estadísticas
    libros = book_repo.load_all()
    autores = author_repo.load_all()

    print("\n📊 Estadísticas:")
    print(f"   📚 Libros totales: {len(libros)}")
    print(f"   👤 Autores totales: {len(autores)}")

    # Buscar libro
    libro_encontrado = book_repo.load(libro.id)
    if libro_encontrado:
        print(f"\n🔍 Libro encontrado: {libro_encontrado.title}")
        print(f"   Autor ID: {libro_encontrado.author_id}")
        print(f"   ISBN: {libro_encontrado.isbn}")

    print("\n🎉 ¡Demo completado exitosamente!")

if __name__ == '__main__':
    main()