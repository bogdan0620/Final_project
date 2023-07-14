from main import app
from database import get_music_db, add_file_to_db, update_file_in_db, download_db, delete_file_from_db
from fastapi import UploadFile, File
import random


@app.get('/get-music')
async def get_file(file_id: int = None, music_name: str = None, singer: str = None):
    result = get_music_db(file_id, music_name, singer)

    return {'status': 1, 'message': result}


@app.post('/add-music')
async def add_file(music_name: str, singer: str = 'Неизвестный', file: UploadFile = File(...)):
    result = add_file_to_db(music_name, singer, file)

    with open(f'{"uploaded_files/"}{music_name}-{result}', "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()

    return {'status': 1, 'message': result}


@app.post('/update-music')
async def update_file(file_id: int, new_music_name: str, singer='Неизвестный', file: UploadFile = File()):
    result = update_file_in_db(file_id, new_music_name, singer, file)

    if result == 'Такой музыки нет':
        return {'status': 1, 'message': result}

    else:
        with open(f'{"uploaded_files/"}{new_music_name}-{file_id}', "wb") as uploaded_file:
            file_content = await file.read()
            uploaded_file.write(file_content)
            uploaded_file.close()

        return {'status': 1, 'message': result}


@app.get('/download-music')
async def download_file(file_id: int):
    result = download_db(file_id)

    return result


@app.delete('/delete-music')
async def delete_file(file_id: int):
    result = delete_file_from_db(file_id)

    return {'status': 1, 'message': result}
