import datetime
import os

import re
import pytz

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from obs import ObsClient, HeadPermission
import time
import hashlib


def validate_title(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title


@deconstructible
class AvatarStorage(Storage):
    def __init__(self, storage_type=settings.STORAGE_TYPE):
        if storage_type == "oss":
            self.ak = settings.OSS_ACCESS_KEY
            self.sk = settings.OSS_SECRET_KEY
            self.endpoint = settings.OSS_ENDPOINT
            self.bucket = settings.OSS_BUCKET
            self.client = ObsClient(
                access_key_id=self.ak,
                secret_access_key=self.sk,
                server=self.endpoint)
            self.file_list = None

    def _open(self, name, mode='rb'):
        if mode != "rb":
            raise ValueError(f"Can't open file as file mode `{mode}`.")
        resp = self.client.getObject(self.bucket, name)
        if resp.status > 300:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            return
        return self.client.getObject(self.bucket, name).body.response

    def set_public_ACL(self, name):
        resp = self.client.setObjectAcl(self.bucket, name, aclControl=HeadPermission.PUBLIC_READ)
        if resp.status > 300:
            print("ACL error")
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)

    def _save(self, name, content):
        start = os.path.split(name)[0]
        name = start + "/" + hashlib.md5((str(int(time.time())) + name).encode()).hexdigest() + os.path.splitext(os.path.split(name)[1])[1]
        resp = self.client.putContent(self.bucket, name, content=content)
        self.reset_file_list()
        if resp.status > 300:
            print("_save error")
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            return
        return name

    def reset_file_list(self):
        resp = self.client.listObjects(self.bucket)
        if resp.status > 300:
            print("reset file list error")
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
        else:
            self.file_list = resp.body.contents

    def url(self, name):
        return f"https://{self.bucket}.{self.endpoint}/{name}"

    def exists(self, name):
        self.reset_file_list()
        for i in self.file_list:
            if i['key'] == name:
                return True
        return False

    def delete(self, name):
        resp = self.client.deleteObject(self.bucket, name)
        if resp.status > 300:
            print("delete file list error")
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            return
        self.reset_file_list()

    def size(self, name):
        return self.client.getObjectMetadata(self.bucket, name).body.contentLength

    def get_modified_time(self, name):
        time = datetime.datetime.strptime(self.client.getObjectMetadata(self.bucket, name).body.lastModified,
                                          "%a, %d %b %Y %H:%M:%S GMT")
        return time + pytz.timezone(settings.TIME_ZONE).utcoffset(time)

    def get_valid_name(self, name):
        return validate_title(name)

    def path(self, name):
        return NotImplemented
