import datetime
import json

from annotate.model.annotation import Annotation


def create(db, entry_id, annotator, score):
    with db.cursor() as cursor:
        created = datetime.datetime.now()
        try:
            score_json = json.dumps(score)
        except Exception:
            score_json = '{}'
        cursor.execute("""
            INSERT INTO annotation (entry_id, annotator, score, created)
            VALUES (%s, %s, %s, %s)
        """, (entry_id, annotator, score_json, created))
        return find_by_id_and_annotator(db, entry_id, annotator)
        
def find_by_id_and_annotator(db, entry_id, annotator):
    with db.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM annotation WHERE entry_id = %s AND annotator = %s""",
            (entry_id, annotator)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Annotation(row)

def update_score(db, annotation, key, value):
    score = annotation.score()
    score[key] = value
    with db.cursor() as cursor:
        cursor.execute("""
            UPDATE annotation SET score = %s WHERE entry_id = %s
        """, (json.dumps(score), annotation.entry_id))

def update_or_create(db, entry_id, annotator, metric, value):
    annotation = find_by_id_and_annotator(db, entry_id, annotator)
    if annotation is None:
        return create(db, entry_id, annotator, {metric: value})
    update_score(db, annotation, metric, value)
    return annotation
