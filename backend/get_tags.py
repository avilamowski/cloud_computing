from db import get_session
from models import Tag
import json


def lambda_handler(event, context):
    session = get_session()

    try:
        # Obtener todos los tags de la base de datos
        tags = session.query(Tag).all()
        tags_serialized = [tag.to_dict() for tag in tags]
        return {"statusCode": 200, "body": json.dumps({"tags": tags_serialized})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        session.close()
