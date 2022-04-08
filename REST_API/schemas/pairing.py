from pydantic import BaseModel


class PairingBidSchema(BaseModel):
    hard_token: str
    paring_id: int
    pet_id: int     # huetaa
    pet_type: str
    money: int
