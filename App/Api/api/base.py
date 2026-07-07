from ninja import NinjaAPI
from .accounts import router as accounts_router

api = NinjaAPI()
api.add_router("/accounts", accounts_router)
