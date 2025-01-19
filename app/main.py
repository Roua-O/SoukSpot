from fastapi import FastAPI,Depends
from app.routers import users, vendors, products, reviews, order_product,recommendations,souks,bargaining
from app.database import engine, Base,get_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.security import decode_access_token, TokenData
from fastapi.openapi.utils import get_openapi


app = FastAPI(title="SoukSpot API", version="0.1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(vendors.router)
app.include_router(products.router)
app.include_router(recommendations.router)
app.include_router(reviews.router)
app.include_router(order_product.router)
app.include_router(souks.router)
app.include_router(bargaining.router)



@app.get('/users/me', response_model=TokenData, dependencies=[Depends(decode_access_token)])
async def read_users_me(current_user: TokenData):
    return current_user

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the SOUKSPOT API"}
def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Welcome to SoukSpot API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
             "flows":{
                "password":{
                    "tokenUrl":"/users/login"
                    }
                }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

