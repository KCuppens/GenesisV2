def search_function_dict(dict, key = None, nl = None, en = None, fr = None):
    results = {}
    if key or nl or en or fr:
        for k, v in dict.items():
            if key and k == key:
                results[k] = v
            else:
                if nl and v['nl']['translation'] == nl:
                    results[k] = v
                elif en and v['en']['translation'] == en:
                    results[k] = v
                elif fr and v['fr']['translation'] == fr:
                    results[k] = v
        return results
    return dict

def get_media_path(path):
    from django.conf import settings
    media_path = settings.MEDIA_ROOT 

    media_split = media_path.split('\\')
    media_split.pop()
    media_url = '/'.join(media_split)
    return media_url + path
