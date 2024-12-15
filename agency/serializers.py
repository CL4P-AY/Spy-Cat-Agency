import requests
from rest_framework import serializers
from .models import SpyCat, Mission, Target


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = "__all__"

    @staticmethod
    def validate_breed(value):
        breeds_url = "https://api.thecatapi.com/v1/breeds"
        try:
            response = requests.get(breeds_url)
            if response.status_code != 200:
                raise serializers.ValidationError(
                    "Unable to validate breed. External API error."
                )

            breeds = [breed["name"] for breed in response.json()]
            if value not in breeds:
                raise serializers.ValidationError(
                    f"Invalid breed '{value}'. Please provide a valid breed name."
                )
        except Exception as e:
            raise serializers.ValidationError(
                f"An error occurred while validating breed: {str(e)}"
            )

        return value


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = "__all__"
        extra_kwargs = {"mission": {"required": False, "read_only": True}}


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, required=False)

    class Meta:
        model = Mission
        fields = "__all__"

    def update(self, instance, validated_data):
        targets_data = validated_data.pop("targets", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if targets_data is not None:
            instance.targets.all().delete()

            for target_data in targets_data:
                Target.objects.create(mission=instance, **target_data)

        return instance
