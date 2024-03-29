from threading import local

from django.core.mail import get_connection

from apps.mail.settings import get_backend


# Copied from Django 1.8's django.core.cache.CacheHandler
class ConnectionHandler:
    """
    A Cache Handler to manage access to Cache instances.
    Ensures only one instance of each alias exists per thread.
    """
    def __init__(self):
        self._connections = local()

    def __getitem__(self, alias):
        try:
            return self._connections.connections[alias]
        except AttributeError:
            self._connections.connections = {}
        except KeyError:
            pass

        connection = get_connection()
        connection.open()
        self._connections.connections[alias] = connection
        return connection

    def all(self):
        return getattr(self._connections, 'connections', {}).values()

    def close(self):
        for connection in self.all():
            connection.close()


connections = ConnectionHandler()