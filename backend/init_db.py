from sqlalchemy.sql import text
from db import create_database, get_session
from models import Comment, User, Publication, Tag, publication_tag_table
import logging
from uuid import UUID, uuid4
from datetime import datetime, timedelta
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    session = create_database()
    # session = get_session()

    logger.info("Creating tables")

    User.__table__.create(session.get_bind(), checkfirst=True)
    Publication.__table__.create(session.get_bind(), checkfirst=True)
    Comment.__table__.create(session.get_bind(), checkfirst=True)
    Tag.__table__.create(session.get_bind(), checkfirst=True)
    publication_tag_table.create(session.get_bind(), checkfirst=True)

    users = [
        # Admins! Required
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-44665544000a"),
            "username": "joliu-admin",
            "email": "joliu+1@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-44665544000b"),
            "username": "dwischnevsky-admin",
            "email": "dwischnevsky+1@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-44665544000c"),
            "username": "avilamowski-admin",
            "email": "avilamowski@itba.edu.ar",
        },
        #
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440000"),
            "username": "Agustina",
            "email": "agustina.perez@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440001"),
            "username": "Bruno",
            "email": "bruno.garcia@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440002"),
            "username": "Camila",
            "email": "camila.rodriguez@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440003"),
            "username": "Diego",
            "email": "diego.fernandez@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440004"),
            "username": "Elena",
            "email": "elena.gomez@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440005"),
            "username": "Federico",
            "email": "federico.lopez@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440006"),
            "username": "Gabriela",
            "email": "gabriela.martinez@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440007"),
            "username": "Hernán",
            "email": "hernan.sanchez@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440008"),
            "username": "Isabella",
            "email": "isabella.ramirez@itba.edu.ar",
        },
        {
            "user_id": UUID("550e8400-e29b-41d4-a716-446655440009"),
            "username": "Javier",
            "email": "javier.torres@itba.edu.ar",
        },
    ]
    session.bulk_insert_mappings(User, users)

    tags = [
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440000"),
            "name": "Sistemas Operativos",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440001"),
            "name": "Cloud Computing",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440002"),
            "name": "Redes",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440003"),
            "name": "Programación Imperativa",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440004"),
            "name": "Programación Orientada a Objetos",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440005"),
            "name": "Programación Funcional",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440006"),
            "name": "EDA",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440007"),
            "name": "Lógica Computacional",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440008"),
            "name": "Matemática Discreta",
            "tag_type": "Subject",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440009"),
            "name": "Profesores",
            "tag_type": "Teacher",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440010"),
            "name": "Exámenes",
            "tag_type": "Miscellaneous",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440011"),
            "name": "Apuntes",
            "tag_type": "Miscellaneous",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440012"),
            "name": "Parciales",
            "tag_type": "Miscellaneous",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440013"),
            "name": "Finales",
            "tag_type": "Miscellaneous",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440014"),
            "name": "Técnicas de Estudio",
            "tag_type": "Miscellaneous",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440015"),
            "name": "Ing. Informática",
            "tag_type": "Career",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440016"),
            "name": "Ing. Electrónica",
            "tag_type": "Career",
        },
        {
            "tag_id": UUID("880e8400-e29b-41d4-a716-446655440017"),
            "name": "Ing. Mecánica",
            "tag_type": "Career",
        },
    ]
    session.bulk_insert_mappings(Tag, tags)

    # Mapas para fácil acceso
    tag_dict = {str(tag["tag_id"]): tag["name"] for tag in tags}
    tag_ids = [tag["tag_id"] for tag in tags]
    user_ids = [user["user_id"] for user in users]
    user_names = {str(user["user_id"]): user["username"] for user in users}

    publications = []
    publication_tag_mappings = []

    # Contenido realista de publicaciones
    tag_related_content = {
        "Sistemas Operativos": [
            "Dudas sobre el TP de Sistemas Operativos",
            "Guía para entender concurrencia y paralelismo",
            "Experiencias con Agodio en SO",
        ],
        "Cloud Computing": [
            "Introducción a AWS y sus servicios",
            "Comparativa entre AWS, Azure y GCP",
            "El final de Cloud me da flashbacks a Inge II",
        ],
        "Redes": [
            "Preguntas sobre protocolos TCP/IP",
            "Resumen de la capa de transporte",
            "Ejercicios resueltos de enrutamiento",
        ],
        "Programación Imperativa": [
            "Buenas prácticas en C",
            "Manejo de memoria dinámica",
            "Es esto pesimo estilo?",
            "Programación defensiva",
        ],
        "Programación Orientada a Objetos": [
            "Patrones de diseño más utilizados",
            "Encapsulación y herencia en Java",
            "Ejemplos prácticos de POO en Ruby",
        ],
        "Programación Funcional": [
            "Introducción a Haskell",
            "Funciones puras vs impuras",
            "Monadas y su aplicación",
        ],
        "EDA": [
            "Implementación de árboles AVL",
            "Análisis de complejidad de algoritmos",
            "Uso de grafos en problemas reales",
        ],
        "PAW": [
            "No duermo hace una semana y no entiendo nada",
            "La impedancia objeto relacional y sus consecuencias en la vida cotidiana",
            "¿Cómo hago para que mi página se vea bonita?",
            "Ayuda con SMTP",
            "Debo el final de hace un año y me acabo de enterar que cambio el servidor de Tomcat",
        ],
        "Lógica Computacional": [
            "¿Cuál es el cardinal del conjunto de los conjuntos que no se contienen a sí mismos?",
            "Resolución de problemas de lógica de primer orden",
            "Funciones RP",
            "El halting problem explicado con gatitos",
        ],
        "Matemática Discreta": [
            "Principios de conteo y combinatoria",
            "Grafos k-conexos",
            "Grafo bipartito",
        ],
        "Profesores": [
            "Opiniones sobre un parcial de la época de Bermudez en POO",
            "Recomendaciones de docentes para Redes",
            "Horarios de consulta actualizados",
            "Estoy esperando una respuesta de Gonzalo hace 3 semanas y me estoy muriendo",
        ],
        "Exámenes": [
            "Fechas de los parciales de este cuatrimestre",
            "¿Qué temas entran en el final de EDA?",
            "Tips para aprobar PAW en primera vuelta",
            "Qué temas entran en el final de POD???",
        ],
        "Apuntes": [
            "Compartiendo apuntes de Lógica",
            "Resumen de Sistemas Operativos",
            "Guía de estudio para Arqui",
        ],
        "Parciales": [
            "Ejercicios de parciales anteriores de POO",
            "Consultas sobre el parcial de Cloud Computing",
            "Estrategias para el parcial de Programación Imperativa",
        ],
        "Finales": [
            "Mi experiencia en el final de Proba",
            "Preguntas frecuentes en el final de Cripto",
            "Material recomendado para preparar el final de SO",
        ],
        "Técnicas de Estudio": [
            "Cómo organizarse para estudiar varias materias",
            "Métodos efectivos para retener información",
            "Consejos para rendir mejor en exámenes",
        ],
    }

    # Generar publicaciones
    for i in range(1, 60):  # Generar 60 publicaciones
        publication_id = uuid4()
        user_id = random.choice(user_ids)
        num_tags = random.randint(1, 3)  # Reducir a 1-3 tags para mayor relevancia
        assigned_tags = random.sample(tag_ids, num_tags)
        tag_names = [tag_dict[str(tag_id)] for tag_id in assigned_tags]

        # Generar título y contenido basado en los tags
        possible_contents = []
        for tag_name in tag_names:
            if tag_name in tag_related_content:
                possible_contents.extend(tag_related_content[tag_name])

        if possible_contents:
            title = random.choice(possible_contents)
            content = f"{title}. {random.choice(['En este post, comparto mi experiencia.', '¿Alguien más tiene información al respecto?', 'Espero que les sea útil.'])}"
        else:
            title = f"Discusión sobre {' y '.join(tag_names)}"
            content = f"Abro este espacio para hablar sobre {' y '.join(tag_names)}. ¡Compartamos información y recursos!"

        # Fecha de creación aleatoria en los últimos 30 días
        created_at = datetime.now() - timedelta(days=random.randint(0, 30))

        publications.append(
            {
                "publication_id": publication_id,
                "user_id": user_id,
                "title": title,
                "content": content,
                "created_at": created_at,
            }
        )

        # Asignar etiquetas a la publicación
        for tag_id in assigned_tags:
            publication_tag_mappings.append(
                {"publication_id": publication_id, "tag_id": tag_id}
            )

    session.bulk_insert_mappings(Publication, publications)

    # Insertar en la tabla de asociación publication_tag_table
    session.execute(publication_tag_table.insert(), publication_tag_mappings)

    comments = []

    # Comentarios realistas
    sample_comments = [
        "¡Muchas gracias por la info!",
        "Tengo la misma duda, ¿alguien sabe?",
        "Acá dejo un enlace que puede ayudar.",
        "Me sirvió mucho tu aporte.",
        "Creo que podrías profundizar en este punto.",
        "¿Podrías compartir los apuntes?",
        "Excelente resumen, gracias por compartir.",
        "¿Alguien tiene el material de años anteriores?",
        "Estoy preparando el final, esto es muy útil.",
        "¡Éxitos en los exámenes a todos!",
    ]

    # Generar comentarios
    for i in range(1, 180):  # Generar 180 comentarios
        comment_id = uuid4()
        publication = random.choice(publications)
        publication_id = publication["publication_id"]
        user_id = random.choice(user_ids)
        content = random.choice(sample_comments)
        created_at = datetime.now() - timedelta(days=random.randint(0, 30))

        comments.append(
            {
                "comment_id": comment_id,
                "publication_id": publication_id,
                "user_id": user_id,
                "content": content,
                "created_at": created_at,
            }
        )

    session.bulk_insert_mappings(Comment, comments)

    session.commit()
    session.close()

    logger.info("Tables created successfully")

    return {"statusCode": 200, "body": "Tables created successfully"}
