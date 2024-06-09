from fastapi import FastAPI

from app.database import Base, engine
from app.users.routes import user_router
from xeez_pyutils.exceptions import exception_to_handler_list


def init_app(start_db: bool = True) -> FastAPI:
    """Inicializa a aplicação FastAPI.

    Args:
        start_db (bool, opcional): Indica se o banco de dados deve ser inicializado. O padrão é True.

    Returns:
        FastAPI: Instância da aplicação FastAPI inicializada.
    """
    app = FastAPI()

    # Inclui roteadores para diferentes endpoints
    app.include_router(user_router)

    # Adiciona manipuladores de exceção
    for exception_class, handler_function in exception_to_handler_list:
        app.add_exception_handler(exception_class, handler_function)  # type: ignore

    # Cria tabelas do banco de dados, se necessário
    if start_db:
        Base.metadata.create_all(bind=engine)

    return app
