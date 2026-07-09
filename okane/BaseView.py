from typing import Any, override
from django.views import View as DjangoView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBase
from django_htmx.middleware import HtmxDetails
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()

class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails  # pyright: ignore[reportUninitializedInstanceVariable]

def render_content(
    request: HtmxHttpRequest,
    template: str,
    context: dict[str, Any] | None = None,
    as_is: bool = False,
    *args: Any,
    **kwargs: Any,
) -> HttpResponseBase:
    if context is None:
        context = {}

    if request.htmx and not as_is:
        template += "#partial"

    return render(request, template, context, *args, **kwargs)


class BaseView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DjangoView,
):
    permission_required: str | None = None
    template_name: str | None = None
    permission_denied_message: str = ""

    @override
    async def dispatch(self, request: HtmxHttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase: # pyright: ignore[reportIncompatibleMethodOverride]
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        self.request: HtmxHttpRequest = request  # pyright: ignore[reportIncompatibleVariableOverride]
        self.user: User = request.user   # pyright: ignore[reportUninitializedInstanceVariable, reportAttributeAccessIssue]

        self.permission_required = (
            "None" if not self.permission_required else self.permission_required
        )
        self.permission_denied_message: Any = "Insufficient permissions, contact your administrator."

        return await super().dispatch(request, *args, **kwargs)  # pyright: ignore[reportUnknownVariableType, reportGeneralTypeIssues]

    @override
    def has_permission(self) -> bool:
        """
        Override this method to customize the way permissions are checked.
        """
        return (
            True
            if self.permission_required == "None"
            else super().has_permission()
        )

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
        return render_content(
            self.request,
            self.template_name or "",
            context,
            as_is=as_is,
        )

    def today(self) -> Any:
        return timezone.now()

    @override
    def handle_no_permission(self) -> HttpResponseBase: # pyright: ignore[reportIncompatibleMethodOverride]
        if not self.request.user.is_authenticated:
            # User not logged in
            if self.request.htmx:
                response = HttpResponse(status=401)
                response["HX-Redirect"] = reverse("accounts:login")
                return response
            return super(LoginRequiredMixin, self).handle_no_permission()

        # User is logged in but lacks permission
        if self.request.htmx:
            return HttpResponse("Forbidden", status=403)
        return super(PermissionRequiredMixin, self).handle_no_permission()

    def has_perm(self, perm: str) -> bool:
        """
        Check if the current user has the given permission.
        Returns True or False.
        """
        if not self.user.is_authenticated:
            return False
        return self.user.has_perm(perm)
