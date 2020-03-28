import os
from django.conf import settings
import datetime
import uuid

# 각 media 파일에 대한 URL Prefix
MEDIA_URL = '/image/'
MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'image')

# 파일 업로드 사이즈 100M ( 100 * 1024 * 1024 )
# FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600


# 폴더는 일별로 생성됨
# 날짜에 해당하는 폴더 없으면 생성
def make_directory(datetime):
    year_dir = os.path.join(MEDIA_ROOT, datetime.strftime('%Y'))
    if not os.path.isdir(year_dir):
        os.mkdir(year_dir)
    month_dir = os.path.join(year_dir, datetime.strftime('%m'))
    if not os.path.isdir(month_dir):
        os.mkdir(month_dir)
    day_dir = os.path.join(month_dir, datetime.strftime('%d'))
    if not os.path.isdir(day_dir):
        os.mkdir(day_dir)


# 실제 파일을 저장할 경로 및 파일 명 생성
def file_upload_path(filename):
    ext = filename.split('.')[-1]
    d = datetime.datetime.now()
    make_directory(d)
    filepath = d.strftime('%Y\\%m\\%d')
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = "%s_%s.%s" % (uuid.uuid4().hex, suffix, ext)
    return os.path.join(MEDIA_ROOT, filepath, filename)


# DB 필드에서 호출
def file_upload_path_for_db(intance, filename):
    return file_upload_path(filename)
