from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

DB = "stargaze_db"

class Observation:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.date = data['date']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data.get('creator_name', '')
        self.likes_count = data.get('likes_count', 0)
        self.liked_by_current = data.get('liked_by_current', 0)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO observations (name, location, date, description, user_id) VALUES (%(name)s, %(location)s, %(date)s, %(description)s, %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def get_all(cls, current_user_id):
        # Bonus: Ordenadas por fecha ascendente y conteo de likes
        query = '''
            SELECT o.*, CONCAT(u.first_name, ' ', u.last_name) as creator_name,
            (SELECT COUNT(*) FROM likes WHERE observation_id = o.id) as likes_count,
            (SELECT COUNT(*) FROM likes WHERE observation_id = o.id AND user_id = %(user_id)s) as liked_by_current
            FROM observations o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.date ASC;
        '''
        results = connectToMySQL(DB).query_db(query, {"user_id": current_user_id})
        observations = []
        if results:
            for row in results:
                observations.append(cls(row))
        return observations

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM observations WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_by_name(cls, data):
        query = "SELECT * FROM observations WHERE name = %(name)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE observations SET name=%(name)s, location=%(location)s, date=%(date)s, description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM observations WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
        
    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (user_id, observation_id) VALUES (%(user_id)s, %(observation_id)s);"
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validate_observation(data, is_edit=False, current_id=None):
        is_valid = True
        if not data['name']:
            flash("El nombre es obligatorio.", "obs")
            is_valid = False
        else:
            # Bonus: Nombre único
            existing = Observation.get_by_name({"name": data['name']})
            if existing:
                if not is_edit or (is_edit and str(existing.id) != str(current_id)):
                    flash("El nombre de la observación ya existe.", "obs")
                    is_valid = False
                    
        if not data['location']:
            flash("El lugar de encuentro es obligatorio.", "obs")
            is_valid = False
        if not data['date']:
            flash("La fecha es obligatoria.", "obs")
            is_valid = False
        if not data['description']:
            flash("La descripción es obligatoria.", "obs")
            is_valid = False
        return is_valid
