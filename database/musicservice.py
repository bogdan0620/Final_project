from database.models import Music
from database import get_db
import os
from starlette.responses import FileResponse


def add_music_db(music_name, singer, file):
    db = next(get_db())
    new_file = Music(music_name=music_name, singer_name=singer, type_format=file.content_type)
    db.add(new_file)
    db.commit()
    print(new_file.as_dict())
    return new_file.as_dict()


def get_music_db(music_id, music_name, singer):
    db = next(get_db())
    if music_id and not music_name and not singer:
        result1 = db.query(Music).filter_by(music_id=music_id).all()

    elif music_id and music_name and not singer:
        result1 = db.query(Music).filter_by(music_id=music_id, music_name=music_name).all()

    elif music_id and music_name and singer:
        result1 = db.query(Music).filter_by(music_id=music_id, music_name=music_name, singer_name=singer).all()

    elif music_id and not music_name and singer:
        result1 = db.query(Music).filter_by(music_id=music_id, singer_name=singer).all()

    elif not music_id and music_name and singer:
        result1 = db.query(Music).filter_by(music_name=music_name, singer_name=singer).all()

    elif not music_id and not music_name and singer:
        result1 = db.query(Music).filter_by(singer_name=singer).all()

    elif not music_id and music_name and not singer:
        result1 = db.query(Music).filter_by(music_name=music_name).all()

    else:
        result1 = db.query(Music).all()
    result = [i.as_dict() for i in result1]
    return reversed(result)


def update_music_db(music_id, new_music_name, singer, file):
    db = next(get_db())
    music1 = db.query(Music).filter_by(music_id=music_id).first()
    print(music1)

    if music1:
        music = music1.as_dict()
        s = music["type_format"]
        s1 = s.replace("audio/", ".")

        music1.music_name = new_music_name
        music1.singer_name = singer
        music1.type_format = file.content_type
        db.commit()

        os.remove(f'{"uploaded_files/"}{music["music_name"]}-{music["singer_name"]}{s1}')

        return music

    return 'Файл музыки не найден'


def download_music_db(music_id):
    db = next(get_db())
    music1 = db.query(Music).filter_by(music_id=music_id).first()
    if music1:
        music = music1.as_dict()
        s = music["type_format"]
        s1 = s.replace("audio/", ".")
        file_resp = FileResponse(f'{"uploaded_files/"}{music["music_name"]}-{music["singer_name"]}{s1}', media_type=music["type_format"], filename=f'{music["music_name"]}-{music["singer_name"]}{s1}')
        return file_resp

    else:
        return 'Файл музыки не найден'


def delete_music_db(music_id):
    db = next(get_db())
    music1 = db.query(Music).filter_by(music_id=music_id).first()

    if music1:
        music = music1.as_dict()
        s = music["type_format"]
        s1 = s.replace("audio/", ".")
        os.remove(f'{"uploaded_files/"}{music["music_name"]}-{music["singer_name"]}{s1}')

        db.delete(music1)
        db.commit()

        return f'Удалено {music["music_name"]}-{music["singer_name"]}'

    return 'Файл музыки не найден'
