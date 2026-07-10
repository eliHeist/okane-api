from okane.registry import app_urls
from okane.BaseView import BaseView, HtmxHttpRequest
from django.contrib.auth import aauthenticate, alogin, alogout, aget_user, get_user_model
from django.shortcuts import redirect, render
from django.conf import settings
from django.views import View



@app_urls.route('auth/login', name='auth_login')
class LoginView(View):
    template_name = 'registration/login.html'
    async def get(self, request: HtmxHttpRequest):
        return render(request, self.template_name, {'next': request.GET.get('next', '')})
    
    async def post(self, request: HtmxHttpRequest):
        data = request.POST
        get_data = request.GET
        email: str = data.get('email', '').strip()
        password: str = data.get('password', '')
        user = await aauthenticate(request=request, email=email, password=password)
        if not user:
            return {"error": "Invalid credentials"}, 401
    
        # create session
        await alogin(request, user)

        next_route: str | None = get_data.get('next')
        if next_route:
            return redirect(next_route)
        return redirect(settings.LOGIN_REDIRECT_URL)