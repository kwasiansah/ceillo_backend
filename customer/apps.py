from django.apps import AppConfig


class CustomerConfig(AppConfig):
    name = "customer"
    # Ensures signals are activated on application load

    def ready(self):
        import customer.signals
