from app.users.models import User
from xeez_pyutils.protocols.repository_protocol import RepositoryProtocol


class UserRepositoryProtocol(RepositoryProtocol[User]): ...
