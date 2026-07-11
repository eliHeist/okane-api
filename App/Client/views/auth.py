from okane.registry import app_urls
from okane.BaseView import BaseView, HtmxHttpRequest
from django.contrib.auth import aauthenticate, alogin, alogout, aget_user, get_user_model
from django.shortcuts import redirect, render
from django.conf import settings
from django.views import View
from django_htmx.http import retarget, reswap

User = get_user_model()

@app_urls.route('auth/login', name='auth_login')
class LoginView(View):
    template_name = 'registration/login.html'
    async def get(self, request: HtmxHttpRequest):
        context = {
            "email": '',
            "next": request.GET.get('next', ''),
            "invalid_email_error": False,
            "invalid_password_error": False,
        }
        return render(request, self.template_name, context  )
    
    async def post(self, request: HtmxHttpRequest):
        data = request.POST
        get_data = request.GET
        email: str = data.get('email', '').strip()
        password: str = data.get('password', '')
        user = await aauthenticate(request=request, email=email, password=password)
        context = {
            "email": email,
            "next": get_data.get('next', ''),
            "invalid_email_error": False,
            "invalid_password_error": False,
        }
        if not user:
            # return the template with error message and htmx reswap header
            if not await User.objects.filter(email=email).aexists():
                context['invalid_email_error'] = True
            else:
                context['invalid_password_error'] = True
            if request.htmx:
                self.template_name = self.template_name + '#form'
            response = render(request, self.template_name, context)
            return retarget(response, "#form")

        # create session
        await alogin(request, user)

        next_route: str | None = get_data.get('next')
        if next_route:
            return redirect(next_route)
        return redirect(settings.LOGIN_REDIRECT_URL)