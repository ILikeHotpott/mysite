from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AutoMiddleware(MiddlewareMixin):
    """ Middleware 1 """

    def process_request(self, request):

        ## 0. exclude the pages that don't need to log in
        ## request.path_info       to get the current user's request URL
        if request.path_info in ["/login/", "/image/code/"]:
            return


        ## 1. if session info can be accessed, which means has logged in, go ahead
        info_dict = request.session.get('info')
        if info_dict:
            return

        ## 2. if not yet logged in
        return redirect("/login")


    def process_response(self, request, response):
        return response

