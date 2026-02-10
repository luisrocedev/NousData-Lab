"""
Ejemplo de uso del Data Access Framework

Este archivo muestra cómo utilizar el framework de acceso a datos
para crear una aplicación de biblioteca simple.

Autor: DAM2526
"""

from data_access_framework import create_framework
from data_access_framework.models import Book, Author
import json


def main():
    """Ejemplo de uso del framework."""

    # Crear instancia del framework
    framework = create_framework(
        data_format='json',  # Usar JSON para persistencia
        config={
            'api.enabled': True,
            'api.port': 5000,
            'ui.theme': 'corporate'
        }
    )

    print("🚀 Framework inicializado exitosamente!")

    # Obtener servicios
    auth_service = framework.get_service('auth')
    book_repo = framework.get_repository('Book')
    author_repo = framework.get_repository('Author')
    loan_service = framework.get_service('loan')
    report_service = framework.get_service('report')

    print("\n📚 Creando datos de ejemplo...")

    # Crear autores
    author1 = Author(
        name='Gabriel',
        last_name='García Márquez',
        birth_date='1927-03-06',
        nationality='Colombiano'
    )
    author_repo.save(author1)

    author2 = Author(
        name='Isabel',
        last_name='Allende',
        birth_date='1942-08-02',
        nationality='Chilena'
    )
    author_repo.save(author2)

    print(f"✅ Autor creado: {author1.full_name}")
    print(f"✅ Autor creado: {author2.full_name}")

    # Crear libros
    book1 = Book(
        title='Cien años de soledad',
        isbn='978-84-376-0494-7',
        author_id=author1.id,
        genre='Novela',
        year=1967,
        pages=417,
        available=True
    )
    book_repo.save(book1)

    book2 = Book(
        title='La casa de los espíritus',
        isbn='978-84-376-0154-0',
        author_id=author2.id,
        genre='Novela',
        year=1982,
        pages=368,
        available=True
    )
    book_repo.save(book2)

    print(f"✅ Libro creado: {book1.title}")
    print(f"✅ Libro creado: {book2.title}")

    # Crear usuario (o usar existente)
    existing_users = auth_service.user_repo.find_by(email='juan.perez@email.com')
    if existing_users:
        user = existing_users[0]
        print(f"✅ Usuario existente encontrado: {user.full_name} ({user.email})")
    else:
        user = auth_service.register_user(
            name='Juan',
            last_name='Pérez',
            email='juan.perez@email.com',
            password='password123',
            role='user'
        )
        print(f"✅ Usuario creado: {user.full_name} ({user.email})")

    # Crear préstamo (solo si no existe uno activo para este libro)
    existing_loans = loan_service.get_active_loans_by_user(user.id)
    active_loans_for_book = [l for l in existing_loans if l.book_id == book1.id and l.status == 'active']

    loan_created = False
    if active_loans_for_book:
        loan = active_loans_for_book[0]
        print(f"✅ Préstamo existente encontrado: {book1.title} -> {user.full_name}")
    else:
        try:
            loan = loan_service.create_loan(
                user_id=user.id,
                book_id=book1.id,
                days=14
            )
            loan_created = True
            print(f"✅ Préstamo creado: {book1.title} -> {user.full_name}")
        except ValueError as e:
            print(f"⚠️ No se pudo crear préstamo: {e}")
            print("ℹ️ Continuando con el ejemplo sin crear nuevo préstamo...")
            loan_created = False
    print(f"   Fecha de devolución: {loan.due_date.strftime('%Y-%m-%d')}")

    # Obtener estadísticas
    stats = framework.get_stats()
    print("\n📊 Estadísticas del sistema:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    # Generar reporte de libros
    books_report = report_service.generate_books_report()
    print("\n📈 Reporte de libros:")
    print(f"  - Total de libros: {books_report['total_books']}")
    print(f"  - Libros por género: {books_report['by_genre']}")
    print(f"  - Rango de años: {books_report['year_range']['oldest']} - {books_report['year_range']['newest']}")

    # Devolver el préstamo (solo si se creó uno nuevo)
    if loan_created:
        result = loan_service.return_loan(loan.id)
        print("\n📚 Préstamo devuelto:")
        print(f"  - Libro: {book1.title}")
        print(f"  - Estado: {result['status']}")
        if result.get('fine_amount', 0) > 0:
            print(f"  - Multa: ${result['fine_amount']:.2f}")
        if result.get('days_overdue', 0) > 0:
            print(f"  - Días de retraso: {result['days_overdue']}")
    else:
        print("\n📚 Saltando devolución de préstamo (no se creó uno nuevo)")

    print("\n🎉 ¡Ejemplo completado exitosamente!")
    print("💡 El framework está listo para usar en tus aplicaciones!")

    # Iniciar API si está habilitada
    if framework.config_manager.get('api.enabled', False):
        print("\n🌐 Iniciando API REST...")
        framework.start_api()
    else:
        print("\n💻 Iniciando interfaz gráfica...")
        framework.start_ui()


if __name__ == '__main__':
    main()