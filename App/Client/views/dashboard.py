from okane.registry import app_urls
from okane.BaseView import BaseView, HtmxHttpRequest
from django.shortcuts import redirect, render

@app_urls.route('', name='landing')
class DashboardView(BaseView):
    template_name = 'dashboard/landing.html'

    async def get(self, request: HtmxHttpRequest):
        return render(request, self.template_name)