from sqlalchemy.orm import Session

from . import models, schemas
from .exceptions import Audio_Doesnt_Exist, UpdateError, DeleteError
from .schemas import AudioFileType, AudioCreateTypeSchemas

type_modelMap = {
    'song': models.Song,
    'podcast': models.Podcast,
    'audiobook': models.Audiobook
}


def get_audioModel(audio_file_type: AudioFileType):
    return type_modelMap[audio_file_type]


def get_audioFile(db: Session, audio_file_type: AudioFileType, audio_id: int):
    audio_model = get_audioModel(audio_file_type)
    audio_object = db.query(audio_model).get(audio_id)

    if audio_object is None:
        raise Audio_Doesnt_Exist()

    return audio_object


def get_audioFiles(db: Session, audio_file_type: AudioFileType, skip: int = 0, limit: int = 100):
    audio_model = get_audioModel(audio_file_type)
    return db.query(audio_model).offset(skip).limit(limit).all()


def create_audioFile(db: Session, audio_file_type: AudioFileType, audio_file_metadata: AudioCreateTypeSchemas):
    audio_model = get_audioModel(audio_file_type)
    audio_object = audio_model(**audio_file_metadata.dict())

    db.add(audio_object)
    db.commit()
    db.refresh(audio_object)
    return audio_object


def update_audioFile(db: Session, audio_file_type: AudioFileType,
                      audio_id: int, audio_file_metadata: AudioCreateTypeSchemas):

    audio_model = get_audioModel(audio_file_type)
    audio_object_id = db.query(audio_model).filter_by(id=audio_id).update(audio_file_metadata.dict())

    if not audio_object_id:
        raise Audio_Doesnt_Exist()

    if audio_object_id != audio_id:
        raise UpdateError()

    db.commit()
    return audio_object_id


def delete_audioFile(db: Session, audio_file_type: AudioFileType,audio_id: int):

    audio_model = get_audioModel(audio_file_type)
    audio_object_id = db.query(audio_model).filter_by(id=audio_id).delete()

    if not audio_object_id:
        raise Audio_Doesnt_Exist()

    if audio_object_id != audio_id:
        raise DeleteError()

    db.commit()
    return audio_object_id
