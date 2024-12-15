from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cat:
            return Response(
                {
                    "error": "Mission cannot be deleted because it is already assigned to a cat."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        targets_data = serializer.validated_data.pop("targets", [])
        mission = Mission.objects.create(**serializer.validated_data)

        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)

        return Response(
            self.get_serializer(mission).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        for target_data in request.data.get("targets", []):
            target_name = target_data.get("name")
            if target_name:
                target_instance = instance.targets.filter(name=target_name).first()
                if target_instance:
                    if target_instance.is_complete or instance.is_complete:
                        return Response(
                            {
                                "error": f"Cannot update notes for target {target_instance.id} "
                                f"because the target or the mission is completed."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

        return super().update(request, *args, **kwargs)


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
