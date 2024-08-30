from rest_framework.serializers import ModelSerializer


class BaseProjectModelSerializer(ModelSerializer):
    """
    Serializer should not create or update objects, as
    these actions have to be performed at the service layer.
    """

    def create(self, validated_data):
        raise NotImplementedError(
            "You must use service instead of serializer for this action!"
        )

    def update(self, instance, validated_data):
        raise NotImplementedError(
            "You must use service instead of serializer for this action!"
        )