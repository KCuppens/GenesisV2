from apps.conf.utils import get_config

class Head:
    def __init__(self, request):
        self.request = request 
        if 'seo_author' in request.session:
            self.author = request.session['seo_author']
        else:
            self.author = get_config('seo_author')
        if 'seo_title' in request.session:
            self.title = request.session['seo_title']
        else:
            self.title = get_config('seo_title')
        if 'seo_description' in request.session:
            self.description = request.session['seo_description']
        else:
            self.description = get_config('seo_description')
        if 'seo_keywords' in request.session:
            self.keywords = request.session['seo_keywords']
        else:
            self.keywords = get_config('seo_keywords')
        if 'seo_image' in request.session:
            self.image = request.session['seo_image']

    def override_by_object(self, object):
        self.request.session['seo_title'] = object.fetch_seo_title()
        if object.fetch_seo_keywords():
            self.request.session['seo_keywords'] = object.fetch_seo_keywords()
        if object.fetch_seo_description():
            self.request.session['seo_description'] = object.fetch_seo_description()
        if object.fetch_seo_image():
            self.request.session['seo_image'] = object.fetch_seo_image()

    def get_author(self):
        return self.author
    
    def get_title(self):
        return self.title 

    def get_keywords(self):
        return self.keywords

    def get_description(self):
        return self.description 

    def get_image(self):
        return self.image