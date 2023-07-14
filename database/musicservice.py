from database.models import Music
from database import get_db
import os
from starlette.responses import FileResponse


def get_music_db(file_id, music_name, singer):
    db = next(get_db())
    if file_id and not music_name and not singer:
        query = db.query(Music).filter_by(file_id=file_id).all()

    elif file_id and music_name and not singer:
        query = db.query(Music).filter_by(file_id=file_id, music_name=music_name).all()

    elif file_id and music_name and singer:
        query = db.query(Music).filter_by(file_id=file_id, music_name=music_name, singer=singer).all()

    elif file_id and not music_name and singer:
        query = db.query(Music).filter_by(file_id=file_id, singer=singer).all()

    elif not file_id and music_name and singer:
        query = db.query(Music).filter_by(music_name=music_name, singer=singer).all()

    elif not file_id and not music_name and singer:
        query = db.query(Music).filter_by(singer=singer).all()

    elif not file_id and music_name and not singer:
        query = db.query(Music).filter_by(music_name=music_name).all()

    else:
        query = db.query(Music).all()
    print(query)
    if len(query) == 0:
        return {'message': 'No results =('}

    return query


# Add File to DB
def add_file_to_db(music_name, singer, file):
    db = next(get_db())
    new_file = Music(music_name=music_name, singer=singer, type_format=file.content_type)
    db.add(new_file)
    db.commit()
    return new_file.file_id


# Update File in DB
def update_file_in_db(file_id, music_name, singer, file):
    db = next(get_db())
    music = db.query(Music).filter_by(file_id=file_id).first()
    if music:
        os.remove("uploaded_files/" + music.music_name + f'-{music.file_id}')
        music.music_name = music_name
        music.singer = singer
        music.type_format = file.content_type
        db.commit()

        return 'Обновлено'

    return 'Такой музыки нет'


def download_db(file_id):
    db = next(get_db())
    music = db.query(Music).filter_by(file_id=file_id).first()
    print(music.music_name)
    if music:
        file_resp = FileResponse("uploaded_files/" + music.music_name + f'-{file_id}', media_type=music.type_format, filename=music.music_name)
        return file_resp

    else:
        return 'File not found'


def delete_file_from_db(file_id):
    db = next(get_db())
    music = db.query(Music).filter_by(file_id=file_id).first()

    if music:
        os.remove("uploaded_files/" + music.music_name)
        # Delete file from DB
        db.delete(music)
        db.commit()

        return 'Удалено'

    return 'File does not exist'
