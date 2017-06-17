import peewee as pw

_db = pw.SqliteDatabase('qzbot.db')


class BaseModel(pw.Model):
    """A base model that will use the Sqlite database."""

    class Meta:
        database = _db


class Session(BaseModel):
    creator_id = pw.IntegerField()
    active = pw.BooleanField(default=True)


class User(BaseModel):
    tm_id = pw.IntegerField(unique=True)
    session = pw.ForeignKeyField(
        Session, related_name='participants', null=True)


class Round(BaseModel):
    session = pw.ForeignKeyField(Session, related_name='rounds')


class Turn(BaseModel):
    user = pw.ForeignKeyField(User, related_name='rounds')
    round = pw.ForeignKeyField(Round, related_name='rounds')
    success = pw.BooleanField()


def create_tables():
    _db.connect()
    _db.create_tables([User, Session, Round, Turn], safe=True)


def create_session(tm_id):
    creator, _ = User.get_or_create(tm_id=tm_id)

    if creator.session:
        return None

    session = Session.create(creator_id=creator.id)

    creator.session = session
    creator.save()

    return session


def get_hosted_session(tm_id):
    try:
        return Session.select().join(
            User, on=(Session.creator_id == User.id)).where(
                User.tm_id == tm_id).get()
    except pw.DoesNotExist:
        return None
