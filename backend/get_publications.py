from sqlalchemy.orm import joinedload
from sqlalchemy import func
from db import get_session
from models import Publication, Tag
import json

def get_single_publication(session, publication_id):
    # Carga la publicación junto con sus tags usando joinedload
    publication = (session.query(Publication)
                   .options(joinedload(Publication.tags), joinedload(Publication.user))
                   .filter_by(publication_id=publication_id)
                   .first())
    return publication

def lambda_handler(event, context):
    session = get_session()
    
    try:
        # Obtener parámetros de la solicitud
        query_params = event.get('queryStringParameters', {}) if event else {}
        publication_id = query_params.get('publication_id')
        search_term = query_params.get('search')
        page = int(query_params.get('page', 1))
        selected_tags = query_params.get('tags', '').split(',') if query_params.get('tags') else []

        if publication_id:
            publication = get_single_publication(session, publication_id)
            if not publication:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'publication not found'})
                }
            publication_data = publication.to_dict()
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'publication': publication_data
                })
            }

        # Validación de la página
        if not str(page).isdigit() or int(page) < 1:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'invalid page'})
            }

        # Consulta de publicaciones con filtros
        publication_query = session.query(Publication).options(joinedload(Publication.tags), joinedload(Publication.user))

        # Filtrar por término de búsqueda
        if search_term:
            publication_query = publication_query.filter(
                Publication.title.ilike(f'%{search_term}%') |
                Publication.content.ilike(f'%{search_term}%')
            )

        # Filtrar por tags seleccionados
        if selected_tags:
            publication_query = (
                publication_query.join(Publication.tags)
                .filter(Tag.name.in_(selected_tags))
                .group_by(Publication.publication_id)
                .having(func.count(Publication.publication_id) == len(selected_tags))
            )

        # Contar publicaciones para paginación
        publications_count = publication_query.distinct().count()

        # Obtener publicaciones para la página actual
        publications = (publication_query.order_by(Publication.created_at.desc())
                        .limit(10)
                        .offset((int(page) - 1) * 10)
                        .all())

        # Formatear la respuesta con to_dict() para cada publicación
        result = {
            'publications': [pub.to_dict() for pub in publications],
            'page': page,
            'total_pages': max(0, int((publications_count - 1) / 10) + 1),
            'total_publications': publications_count
        }

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    finally:
        session.close()
