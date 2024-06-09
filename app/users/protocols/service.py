from app.users.models import User
from xeez_pyutils.protocols.service_protocol import ServiceProtocol


class UserServiceProtocol(ServiceProtocol[User]): ...
