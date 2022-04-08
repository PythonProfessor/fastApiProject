from REST_API.decorators import auth
from REST_API.schemas.pairing import PairingBidSchema
from REST_API.utils.pairing import PairingBid, Pairing
from REST_API.utils.users import User
from REST_API.utils.wallets import Wallet


@auth
async def bid_for_child(bid: PairingBidSchema):
    """
    Делаем ставку кролика  --> дополнительно валидируем всё,ставим ставОчку,проверяем есть ли деньги и не существует ли ставки!
    :param bid: PairingBid validation class
    :return: pet object
    """
    # here we have to get user by token
    owner = await User.get_user_by_token(bid.hard_token)
    # here we have to get pairing id
    # print(owner_id)
    #  # checking if it is exists
    data = await PairingBid.check_if_bid_exists(owner['id'])
    if data:
        return {"The bid has been already placed": data['bid_count']}     # проверяем есть ли ставка,если да,то как раз закидываем
    if not await Wallet.check_balance_to_update_level(bid.money, bid.hard_token):
        # here should be validation on wallet if the amount of money is small or max level
        return {f"Error it is impossible to make a bet, you don't have enough money": False}
      #проверить существует ли ставка, если да,
    pairing = await Pairing.get_pairing_id_by_pet_id(bid.pet_id)
    # проверить если МАНИ НЕ ХВАТАЕТ
    # pairing = Pairing.get_pairing_id_by_pet_id(pe)
    bid = await PairingBid.make_a_bet(bid_count=bid.money, owner_id=owner['id'], pairing=pairing)
    return bid
