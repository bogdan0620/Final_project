from fastapi import requests
import starlette.status as status
from main import app
from database.userservice import register_user_db, check_password_db
from database.musicservice import get_music_db
from fastapi import Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates('templates')


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@app.post("/", response_class=RedirectResponse)
async def validate(request: Request, username: str = Form(...), password: str = Form(...)):
    user = check_password_db(username, password)
    music = get_music_db(music_id='', music_name='', singer='')
    if user == 'Имя пользователя или пароль не правильный':
        redirect_url = request.url_for('login')
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND, headers={"x-error": "Error in the data"})
    elif username == user["username"] and password == user["password"]:
        return templates.TemplateResponse("find.html", context={"request": request, 'message': music})


@app.post('/register-user')
async def register_user_api(username: str, password: str):
    result = register_user_db(username=username, password=password)

    return {'status': 1, 'message': result}
