
import os
import datetime

import sqlalchemy
import sqlalchemy.ext.declarative

import latus.util
import latus.const

Base = sqlalchemy.ext.declarative.declarative_base()

class ConfigTable(Base):
    __tablename__ = 'config'

    key = sqlalchemy.Column(sqlalchemy.String(),primary_key=True)
    value = sqlalchemy.Column(sqlalchemy.String())
    datetime = sqlalchemy.Column(sqlalchemy.DateTime())

class Config:
    def __init__(self, appdata_folder):

        self.__key_string = 'cryptokey'
        self.__cloud_root_string = 'cloudroot'
        self.__latus_folder_string = 'latusfolder'
        self.__verbose_string = 'verbose'

        folder = appdata_folder
        if not os.path.exists(folder):
            latus.util.make_dirs(folder)
        sqlite_path = 'sqlite:///' + os.path.abspath(os.path.join(folder, 'config.db'))
        self.__db_engine = sqlalchemy.create_engine(sqlite_path)  # , echo=True)
        Base.metadata.create_all(self.__db_engine)
        self.__Session = sqlalchemy.orm.sessionmaker(bind=self.__db_engine)

    def __config_set(self, key, value):
        session = self.__Session()
        config_table = ConfigTable(key=key,value=value,datetime=datetime.datetime.now())
        q = session.query(ConfigTable).filter_by(key=key).first()
        if q:
            session.delete(q)
        session.add(config_table)
        session.commit()
        session.close()

    def __config_get(self, key):
        session = self.__Session()
        row = session.query(ConfigTable).filter_by(key=key).first()
        if row:
            value = row.value
        else:
            value = None
        session.close()
        return value

    def crypto_set(self, key):
        self.__config_set(self.__key_string, key)

    def crypto_get(self):
        return self.__config_get(self.__key_string)

    def cloud_root_set(self, folder):
        self.__config_set(self.__cloud_root_string, folder)

    def cloud_root_get(self):
        return self.__config_get(self.__cloud_root_string)

    def latus_folder_set(self, folder):
        self.__config_set(self.__latus_folder_string, folder)

    def latus_folder_get(self):
        return self.__config_get(self.__latus_folder_string)

    def verbose_set(self, value):
        self.__config_set(self.__verbose_string, str(value))

    def verbose_get(self):
        return bool(self.__config_get(self.__verbose_string))

    def init(self):
        Base.metadata.drop_all(self.__db_engine)
        Base.metadata.create_all(self.__db_engine)
