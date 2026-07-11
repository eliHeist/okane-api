from typing import Any, Sequence, override
from django.views import View as DjangoView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBase
from django_htmx.middleware import HtmxDetails
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails  # pyright: ignore[reportUninitializedInstanceVariable]


def render_content(
    request: HtmxHttpRequest | HttpRequest,
    template: str | Sequence[str],
    context: dict[str, Any] | None = None,
    as_is: bool = False,
    *args: Any,
    **kwargs: Any,
) -> HttpResponseBase:
    context = context or {}
    if getattr(request, "htmx", None) and not as_is:
        template += "#partial" # pyright: ignore[reportOperatorIssue]
    return render(request, template, context, *args, **kwargs)


class AsyncLoginRequiredMixin:
    login_url_name = "accounts:login"

    async def ensure_authenticated(self, request: HtmxHttpRequest) -> HttpResponseBase | None:
        user = await request.auser()
        if user.is_authenticated:
            self.user = user
            return None

        if getattr(request, "htmx", None):
            response = HttpResponse(status=401)
            response["HX-Redirect"] = reverse(self.login_url_name)
            return response

        return redirect(reverse(self.login_url_name))


class AsyncPermissionRequiredMixin(AsyncLoginRequiredMixin):
    permission_required: str | None = None
    permission_denied_message = "Insufficient permissions, contact your administrator."

    async def ensure_permission(self, request: HtmxHttpRequest) -> HttpResponseBase | None:
        denied = await self.ensure_authenticated(request)
        if denied is not None:
            return denied

        if not self.permission_required:
            return None

        if not self.user.has_perm(self.permission_required): # pyright: ignore[reportAttributeAccessIssue]
            if getattr(request, "htmx", None):
                return HttpResponse("Forbidden", status=403)
            return HttpResponse(self.permission_denied_message, status=403)

        return None


class BaseView(AsyncPermissionRequiredMixin, DjangoView):
    template_name: str | Sequence[str] = ""

    @override
    async def dispatch(self, request: HtmxHttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase: # pyright: ignore[reportIncompatibleMethodOverride]
        self.request = request
        denied = await self.ensure_permission(request)
        if denied is not None:
            return denied
        return await super().dispatch(request, *args, **kwargs) # pyright: ignore[reportGeneralTypeIssues]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {
            "user": self.user,
            **kwargs,
        }

    def render(
        self,
        extra_context: dict[str, Any] | None = None,
        as_is: bool = False,
        **kwargs: Any,
    ) -> HttpResponseBase:
        context = self.get_context_data(**kwargs)
        if extra_context:
            context.update(extra_context)
        return render_content(self.request, self.template_name or "", context, as_is=as_is)

    def today(self) -> Any:
        return timezone.now()