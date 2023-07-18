import requests
from main import app
from database import get_music_db, add_music_db, update_music_db, download_music_db, delete_music_db
from fastapi import UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates('templates')


@app.get('/get-music')
async def get_music_api(file_id: int = None, music_name: str = None, singer_name: str = None, request: Request = Request):
    result = get_music_db(file_id, music_name, singer_name)
    # return {'status': 1, 'message': result}
    return templates.TemplateResponse(name="find.html", context={'status': 1, 'message': result, 'request': request})


@app.get('/add-music-doc', response_class=HTMLResponse)
async def add_music_doc(request: Request):
    return templates.TemplateResponse("add_music_doc.html", context={'request': request})


@app.post('/add-music', response_class=RedirectResponse)
async def add_music_api(request: Request, music_name: str = Form(...), singer_name: str = Form(...), file: UploadFile = File(...)):
    result = add_music_db(music_name, singer_name, file)
    s = result["type_format"]
    s1 = s.replace("audio/", ".")

    with open(f'{"uploaded_files/"}{result["music_name"]}-{result["singer_name"]}{s1}', "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()

    # return {'status': 1, 'message': result}
    return templates.TemplateResponse("find.html", context={'request': request, 'message': result})


@app.post('/update-music')
async def update_music_api(file_id: int, new_music_name: str, singer_name='Неизвестный', file: UploadFile = File(...)):
    result1 = update_music_db(file_id, new_music_name, singer_name, file)

    if result1 == 'Такой музыки нет':
        return {'status': 1, 'message': result1}

    else:
        s = result1["type_format"]
        s1 = s.replace("audio/", ".")
        print(s1)
        with open(f'{"uploaded_files/"}{result1["music_name"]}-{result1["singer_name"]}{s1}', "wb") as uploaded_file:
            file_content = await file.read()
            uploaded_file.write(file_content)
            uploaded_file.close()

        return {'status': 1, 'message': result1}


@app.get('/download-music')
async def download_music_api(file_id: int):
    result = download_music_db(file_id)
    return result


@app.delete('/delete-music')
async def delete_music_api(file_id: int):
    result = delete_music_db(file_id)
    return {'status': 1, 'message': result}
