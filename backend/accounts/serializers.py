from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JWTTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data['firstname'] = self.user.first_name
        data['lastname'] = self.user.last_name
        data['fullname'] = self.user.get_full_name()
        data['email'] = self.user.email
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser

        return data


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email']
        read_only_fields = ['id', 'username']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(
        max_length=128, write_only=True, required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(
        max_length=128, write_only=True, required=True)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self.user = self.context['request'].user

    def validate(self, data):
        """Validate old & new password before initiating password change."""

        if not self.user:
            raise serializers.ValidationError("Missing auth.")
        elif not self.user.check_password(data['old_password']):
            raise serializers.ValidationError("Old password is incorrect.")
        elif data.get('new_password') != data.get('new_password_confirm'):
            raise serializers.ValidationError(
                "New password & confirm password does not match.")

        return data

    def save(self, **kwargs):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        return self.user

    @property
    def data(self):
        return {'details': 'Password changed'}
