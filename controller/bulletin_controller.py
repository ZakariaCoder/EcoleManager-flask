from flask import Blueprint, request, jsonify
from Model.bulletin import db, Bulletin

bulletin_bp = Blueprint('bulletin', __name__)

@bulletin_bp.route('/bulletins', methods=['GET'])
def get_bulletins():
    bulletins = Bulletin.query.all()
    return jsonify([b.serialize() for b in bulletins])

@bulletin_bp.route('/bulletins/<int:id>', methods=['GET'])
def get_bulletin(id):
    bulletin = Bulletin.query.get_or_404(id)
    return jsonify(bulletin.serialize())

@bulletin_bp.route('/bulletins', methods=['POST'])
def add_bulletin():
    data = request.json
    bulletin = Bulletin(**data)
    db.session.add(bulletin)
    db.session.commit()
    return jsonify(bulletin.serialize()), 201

@bulletin_bp.route('/bulletins/<int:id>', methods=['PUT'])
def update_bulletin(id):
    bulletin = Bulletin.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(bulletin, key, value)
    db.session.commit()
    return jsonify(bulletin.serialize())

@bulletin_bp.route('/bulletins/<int:id>', methods=['DELETE'])
def delete_bulletin(id):
    bulletin = Bulletin.query.get_or_404(id)
    db.session.delete(bulletin)
    db.session.commit()
    return '', 204

