from sven.decorator import get
from models import User


@get('/')
async def index():
    users = await User.find_all()

    return {
        'users': users
    }


