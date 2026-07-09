from django.urls import path, include

app_configs = [
	{ 'app_name': 'App.Client', 'url': 'App/Client/', 'namespace': 'Client' },

	{ 'app_name': 'App.Api', 'url': 'App/Api/', 'namespace': 'Api' },

	{ 'app_name': 'Models.Accounts', 'url': 'Models/Accounts/', 'namespace': 'Accounts' },

	{ 'app_name': 'Models.Transactions', 'url': 'Models/Transactions/', 'namespace': 'Transactions' },

	{ 'app_name': 'Models.Users', 'url': 'Models/Users/', 'namespace': 'Users' },

    # { "app_name": "finances.payments", "url": "finances/payments", "namespace": "payments" },
]

def getAppUrls():
    urlpatterns = []
    for config in app_configs:
        urlpatterns.append(
            path(f"{config['url']}", include(f"{config['app_name']}.urls", namespace=config['namespace']))
        )
    return urlpatterns

def getAppNames():
    return [config['app_name'] for config in app_configs]
