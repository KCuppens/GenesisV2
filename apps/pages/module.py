
class Module:
    def __init__(self, request):
        self.request = request

    def get_queryset(self, model, method, limit, paginated = True, sort = False)
        return eval(model).objects.filter()