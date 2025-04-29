from flask import Blueprint, request, jsonify
import uuid

from services.validation import validate_receipt
from services.validation import validate_id
from services.points import calculate_points
from storage.memory import receipts

# Blueprint for all /receipts routes
receipts_bp = Blueprint('receipts', __name__)

@receipts_bp.route("/receipts/process", methods=["POST"])
def process_receipt():
    data = request.get_json(silent=True)
    if not data or not validate_receipt(data):
        return jsonify({"error": "The receipt is invalid."}), 400

    receipt_id = str(uuid.uuid4())
    
    receipts[receipt_id] = data

    return jsonify({"id": receipt_id}), 200

@receipts_bp.route("/receipts/<id>/points", methods=["GET"])
def get_points(id):

    if not validate_id(id) or id not in receipts:
        return jsonify({"error": "No receipt found for that ID."}), 404
    
    # Calculate points using stored receipt
    receipt = receipts[id]
    points = calculate_points(receipt)

    return jsonify({"points": points}), 200