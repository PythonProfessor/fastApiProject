from fastapi import APIRouter
# import REST_API.views.pairing as pairing_views
import REST_API.views.pairing as pairing_views
from REST_API.schemas.pairing import PairingBidSchema

router = APIRouter()


@router.post('/bid_for_child')
async def bid_for_child(bid:PairingBidSchema):
    """
    The handling of the login route
    :param user: values for creation of the user
    :return: the user view
    """
    return await pairing_views.bid_for_child(bid)
    # return await users_views.login(user=user)
