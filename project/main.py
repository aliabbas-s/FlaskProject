# flask imports
from flask import jsonify , Blueprint
from project.auth import token_required
from project.models import User

main = Blueprint('main', __name__)

@main.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):

    users = User.query.all()
    output = []
    for user in users:

        output.append({
            'phone-number': user.mobile,
            'name' : user.name,
            'email' : user.email
        })
  
    return jsonify({'users': output})