from fastapi import FastAPI

from .core.exceptions import IdentityException, identity_exception_handler

app = FastAPI()

app.add_exception_handler(IdentityException, identity_exception_handler)
