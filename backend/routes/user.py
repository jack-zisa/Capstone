from flask import Blueprint, request

user_blueprint = Blueprint('user', __name__, url_prefix = '/user')

@user_blueprint.route('/demographics', methods=['POST'])
def set_demographics():
    print(request.data)