from codes.auth_required import User, auth_required, current_user
from codes.logger import logger
from codes.timer import timer


@timer
@logger
@auth_required(role="admin")
def delete_order(order_id: int) -> dict:
    return {"deleted": order_id}


token = current_user.set(User(name="Mufi", role="admin"))
delete_order(42)
current_user.reset(token)
