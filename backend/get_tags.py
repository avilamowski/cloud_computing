from db import get_session
from models import Tag
import json


def lambda_handler(event, context):
    session = get_session()

    try:
        # Obtener todos los tags de la base de datos
        tags = session.query(Tag).all()
        return {"statusCode": 200, "body": json.dumps({"tags": tags})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        session.close()
