from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app import db
from app.models import Schedule
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import logging

bp = Blueprint('schedule', __name__)
api = Api(bp)

class ScheduleResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            schedules = Schedule.query.filter_by(user_id=user_id).all()
            return [{
                "id": schedule.id,
                "title": schedule.title,
                "description": schedule.description,
                "date": schedule.date.isoformat()
            } for schedule in schedules], 200
        except Exception as e:
            logging.error(f"Error fetching schedules: {e}")
            return {"message": "Internal server error"}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()

            # Convert date string to datetime object
            date_str = data['date']
            date_obj = datetime.fromisoformat(date_str)

            new_schedule = Schedule(
                title=data['title'],
                description=data.get('description'),
                date=date_obj,
                user_id=user_id
            )
            db.session.add(new_schedule)
            db.session.commit()
            return {"message": "Schedule created successfully."}, 201
        except Exception as e:
            logging.error(f"Error creating schedule: {e}")
            return {"message": "Internal server error"}, 500

    @jwt_required()
    def delete(self, schedule_id):
        try:
            schedule = Schedule.query.get_or_404(schedule_id)
            db.session.delete(schedule)
            db.session.commit()
            return {"message": "Schedule deleted successfully."}, 200
        except Exception as e:
            logging.error(f"Error deleting schedule: {e}")
            return {"message": "Internal server error"}, 500

api.add_resource(ScheduleResource, '/schedule', '/schedule/<int:schedule_id>')
