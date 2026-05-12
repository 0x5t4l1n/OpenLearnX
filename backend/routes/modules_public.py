from flask import Blueprint, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

bp = Blueprint("modules_public", __name__)

mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client.openlearnx


@bp.route("/<module_id>/lessons", methods=["GET"])
def get_public_module_lessons(module_id):
    """Public: get lessons for a module by module id."""
    try:
        lessons = list(db.lessons.find({"module_id": module_id}).sort("order", 1))
        if not lessons:
            try:
                oid = ObjectId(module_id)
                lessons = list(db.lessons.find({"module_id": oid}).sort("order", 1))
            except Exception:
                lessons = []

        for lesson in lessons:
            if "_id" in lesson:
                lesson["id"] = str(lesson["_id"])
                del lesson["_id"]

        return jsonify({"success": True, "lessons": lessons})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch lessons: {str(e)}"}), 500
