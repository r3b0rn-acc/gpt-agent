from orm.fields import IntegerField, TextField
from orm.model import Model


class ApiKey(Model):
    """Модель для хранения пользовательских API ключей."""
    id = IntegerField(primary_key=True)
    name = TextField()
    value = TextField()
