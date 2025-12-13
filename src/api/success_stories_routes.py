"""
API Routes para gestionar casos de éxito del taller
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from api.models import db, SuccessStory
import traceback

success_stories_bp = Blueprint('success_stories', __name__)


@success_stories_bp.route('/success-stories', methods=['GET'])
def get_success_stories():
    """
    Obtener todos los casos de éxito (público)
    Query params:
        - featured: true/false para filtrar solo destacados
        - limit: número máximo de resultados
    """
    try:
        # Obtener parámetros de query
        featured_only = request.args.get('featured', 'false').lower() == 'true'
        limit = request.args.get('limit', type=int)
        
        # Construir query
        query = SuccessStory.query
        
        if featured_only:
            query = query.filter_by(is_featured=True)
        
        # Ordenar por más recientes primero
        query = query.order_by(SuccessStory.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        stories = query.all()
        
        return jsonify([story.serialize() for story in stories]), 200
        
    except Exception as e:
        print(f"❌ Error en get_success_stories: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Error al obtener casos de éxito"}), 500


@success_stories_bp.route('/success-stories/<int:story_id>', methods=['GET'])
def get_success_story(story_id):
    """
    Obtener un caso de éxito específico
    """
    try:
        story = SuccessStory.query.get(story_id)
        
        if not story:
            return jsonify({"error": "Caso de éxito no encontrado"}), 404
        
        return jsonify(story.serialize()), 200
        
    except Exception as e:
        print(f"❌ Error en get_success_story: {str(e)}")
        return jsonify({"error": "Error al obtener caso de éxito"}), 500


@success_stories_bp.route('/success-stories', methods=['POST'])
@jwt_required()
def create_success_story():
    """
    Crear un nuevo caso de éxito (solo admin)
    """
    try:
        # Verificar que sea admin
        payload = get_jwt()
        if payload.get("role_id") != 1:
            return jsonify({"error": "Acceso denegado. Solo administradores."}), 403
        
        user_id = payload.get("sub")
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['title', 'description', 'service_type', 'vehicle_model']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo requerido: {field}"}), 400
        
        # Crear nuevo caso de éxito
        new_story = SuccessStory(
            title=data['title'],
            description=data['description'],
            service_type=data['service_type'],
            vehicle_model=data['vehicle_model'],
            before_image_url=data.get('before_image_url'),
            after_image_url=data.get('after_image_url'),
            client_testimonial=data.get('client_testimonial'),
            is_featured=data.get('is_featured', False),
            created_by=user_id
        )
        
        db.session.add(new_story)
        db.session.commit()
        
        return jsonify({
            "message": "Caso de éxito creado exitosamente",
            "success_story": new_story.serialize()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error en create_success_story: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@success_stories_bp.route('/success-stories/<int:story_id>', methods=['PUT'])
@jwt_required()
def update_success_story(story_id):
    """
    Actualizar un caso de éxito existente (solo admin)
    """
    try:
        # Verificar que sea admin
        payload = get_jwt()
        if payload.get("role_id") != 1:
            return jsonify({"error": "Acceso denegado. Solo administradores."}), 403
        
        story = SuccessStory.query.get(story_id)
        if not story:
            return jsonify({"error": "Caso de éxito no encontrado"}), 404
        
        data = request.get_json()
        
        # Actualizar campos si se proporcionan
        if 'title' in data:
            story.title = data['title']
        if 'description' in data:
            story.description = data['description']
        if 'service_type' in data:
            story.service_type = data['service_type']
        if 'vehicle_model' in data:
            story.vehicle_model = data['vehicle_model']
        if 'before_image_url' in data:
            story.before_image_url = data['before_image_url']
        if 'after_image_url' in data:
            story.after_image_url = data['after_image_url']
        if 'client_testimonial' in data:
            story.client_testimonial = data['client_testimonial']
        if 'is_featured' in data:
            story.is_featured = data['is_featured']
        
        db.session.commit()
        
        return jsonify({
            "message": "Caso de éxito actualizado exitosamente",
            "success_story": story.serialize()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error en update_success_story: {str(e)}")
        return jsonify({"error": str(e)}), 500


@success_stories_bp.route('/success-stories/<int:story_id>', methods=['DELETE'])
@jwt_required()
def delete_success_story(story_id):
    """
    Eliminar un caso de éxito (solo admin)
    """
    try:
        # Verificar que sea admin
        payload = get_jwt()
        if payload.get("role_id") != 1:
            return jsonify({"error": "Acceso denegado. Solo administradores."}), 403
        
        story = SuccessStory.query.get(story_id)
        if not story:
            return jsonify({"error": "Caso de éxito no encontrado"}), 404
        
        db.session.delete(story)
        db.session.commit()
        
        return jsonify({"message": "Caso de éxito eliminado exitosamente"}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error en delete_success_story: {str(e)}")
        return jsonify({"error": str(e)}), 500
