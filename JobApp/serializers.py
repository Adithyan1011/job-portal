from rest_framework import serializers
from .models import JobDb,ApplicationDb
from django.contrib.auth.models import User

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDb
        fields = "__all__"
        read_only_fields= ["created_by"]

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ["id","username","email","password"]
        extra_kwargs = {
            "password":{"write_only":True}
        }
    def create(self,valdated_data):
        return User.objects.create_user(**valdated_data)


class ApplicationSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDb
        fields = "__all__"
        read_only_fields = ["applicant"]