import datetime

from annotate.model.entry import Entry


def create(db, url):
    with db.cursor() as cursor:
        uuid = db.uuid()
        created = datetime.datetime.now()
        cursor.execute("""
            INSERT INTO entry (id, uri, created)
            VALUES (%s, %s, %s)
        """, (uuid, url, created))
        return find_by_id(db, uuid)

def find_or_create_entry(db, url):
    entry = find_by_url(db, url)
    if entry is not None:
        return entry
    return create(db, url)

def find_by_id(db, uuid):
    with db.cursor() as cursor:
        cursor.execute("""SELECT * FROM entry WHERE id = %s""", (uuid,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Entry(row)

def find_by_url(db, url):
    with db.cursor() as cursor:
        cursor.execute("""SELECT * FROM entry WHERE uri = %s""", (url,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Entry(row)
