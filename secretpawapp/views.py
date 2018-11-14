from django_registration.backends.activation.views import RegistrationView as BaseRegistrationView


class RegistrationView(BaseRegistrationView):
    def create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions.

        """
        new_user = form.save()
        new_user.save()

        self.send_activation_email(new_user)

        return new_user