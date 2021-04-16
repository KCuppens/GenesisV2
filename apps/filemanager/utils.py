import mimetypes
from django.conf import settings

def get_size(value):
    if value < 512000:
        value = value / 1024.0
        ext = 'kb'
    elif value < 4194304000:
        value = value / 1048576.0
        ext = 'mb'
    else:
        value = value / 1073741824.0
        ext = 'gb'
    return '%s %s' % (str(round(value, 2)), ext)

def base_media_path(instance, filename):
    if instance.type == "image":
        return settings.MEDIA_ROOT + "image/orig/" + filename
    else:
        return settings.MEDIA_ROOT + instance.type + "/" + filename


def guess_mime_type(file):
    return mimetypes.MimeTypes().guess_type(file)

def get_filename(file):
    path = file.name.split('/')
    filename = path[-1]
    return filename

def get_filename_without_extension(filename):
    path = filename.split('.')
    filename = path[0]
    return filename

def get_valid_image_mime_types():
    return {
        'image/png',
        'image/jpeg',
        'image/gif',
        'image/bmp',
        'image/webp',
        'image/svg+xml',
    }
    
    
    
    # [
    #     ('image/png'),
    #     ('jpe', 'image/jpeg'),
    #     ('jpeg', 'image/jpeg'),
    #     ('jpg', 'image/jpeg'),
    #     ('gif', 'image/gif'),
    #     ('bmp', 'image/bmp'),
    #     ('webp', 'image/webp'),
    #     ('svg', 'image/svg+xml')
    # ]

def get_valid_video_mime_types():
    return {
        'video/mp4',
        'application/octet-stream',
        'video/quicktime'
    }

def get_valid_audio_mime_types():
    return {
        'audio/mpeg', 
        'audio/mp3', 
        'audio/x-mp3', 
        'audio/x-mpeg', 
        'audio/x-mpg',
        'audio/wav', 
        'audio/vnd.wave', 
        'audio/x-wav'
    }

def get_valid_file_mime_types():
    return {
        'text/plain',
        'application/zip',
        'application/x-rar-compressed',
        'application/pdf',
        'application/msword',
        'application/msword',
        'application/rtf',
        'application/vnd.ms-excel',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.oasis.opendocument.text',
        'application/vnd.oasis.opendocument.spreadsheet',
    }

def get_valid_mime_types(self):
    return [
        self.get_valid_image_mime_types(),
        self.get_valid_video_mime_types(),
        self.get_valid_audio_mime_types(),
        self.get_valid_file_mime_types()
    ]

def get_feather_file_icon():
    return [
        ('txt', ('file')),
        ('png', ('image')),
        ('jpe', ('image')),
        ('jpeg', ('image')),
        ('jpg', ('image')),
        ('gif', ('image')),
        ('bmp', ('image')),
        ('svg', ('image')),
        ('webp', ('image')),
        ('zip', ('archive')),
        ('rar', ('archive')),
        ('pdf', ('file-plus')),
        ('doc', ('file-plus')),
        ('dot', ('file-plus')),
        ('rtf', ('file-plus')),
        ('xls', ('file-plus')),
        ('ppt', ('file-plus')),
        ('docx', ('file-plus')),
        ('xlsx', ('file-plus')),
        ('pptx', ('file-plus')),
        ('odt', ('file-plus')),
        ('ods', ('file-plus')),
        ('mp4', ('film')),
        ('mov', ('film')),
        ('mp3', ('volume-2')),
        ('wav', ('volume-2')),
    ]

def guess_media_type(mime):
    from apps.filemanager.models import Media
    if mime in get_valid_image_mime_types():
        return Media.TYPE_IMAGE
    elif mime in get_valid_video_mime_types():
        return Media.TYPE_VIDEO
    elif mime in get_valid_file_mime_types():
        return Media.TYPE_FILE
    elif mime in get_valid_audio_mime_types():
        return Media.TYPE_AUDIO
    return Media.TYPE_FILE