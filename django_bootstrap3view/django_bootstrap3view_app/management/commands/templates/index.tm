from django_bootstrap3view_app.views.base import BaseView

class IndexView(BaseView):

    url = r"^$"

    def get(self, *args, **kwargs):

        context = {{"PROJECT_VERSION": "0.0.1"}}

        return self.render_to_response(context)
