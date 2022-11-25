from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailActivatedTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int):
        return str(user.pk) + str(timestamp) + str(user.active_email)

email_activation_token = EmailActivatedTokenGenerator()


class ScoresTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int):
        return str(user.pk) + str(timestamp) + str(user.zxc_scores)

scores_token = ScoresTokenGenerator()