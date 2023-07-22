from flask import Blueprint, request, jsonify
from service.email import save, get_all, get_by_id, delete

bp = Blueprint('app', __name__)

@bp.route('/save_emails', methods=['POST'])
def save_emails():
    data = request.get_json()
    response = save(data)

    return jsonify({'message': 'Emails saved successfully', 'data': response}), 201

@bp.route('/save_emails', methods=['GET'])
def get_all_emails():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    response = get_all(page, page_size)

    return jsonify(response)

@bp.route('/save_emails/<int:email_id>', methods=['GET'])
def get_email_by_id(email_id):
    response = get_by_id(email_id)

    return jsonify(response)

@bp.route('/save_emails/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    delete(email_id)

    return jsonify({'message': f'Email with ID {email_id} deleted successfully'})
