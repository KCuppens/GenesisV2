def search_function_dict(dict, key = None, nl = None, en = None):
    results = {}
    if key or nl or en:
        for k, v in dict.items():
            if key and k == key:
                results[k] = v
            else:
                if nl and v['nl']['translation'] == nl:
                    results[k] = v
                elif en and v['en']['translation'] == en:
                    results[k] = v
        return results
    return dict