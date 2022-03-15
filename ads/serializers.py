from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from ads.models import Categories, User, Ads, City, Selections


class CategorySerializer(serializers.ModelSerializer):
    # class CategorySerializer(serializers.Serializer):
    #     name = serializers.CharField(max_length=150)

    class Meta:
        model = Categories
        fields = '__all__'


class AdsSerializer(serializers.ModelSerializer):
    # author_name = serializers.SlugRelatedField(required=False,
    #                                            many=False,
    #                                            # read_only=False,
    #                                            queryset=User.objects.all(),
    #                                            slug_field='username')

    class Meta:
        model = Ads
        fields = '__all__'
        # fields = ['id','name','author_name']


class AdCreateSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = Ads
        fields = ['name', 'author', 'price', 'author_id', 'description', 'address', 'is_published', 'poster',
                  'category_id']
        read_only_fields = ('author_id',)


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ['name', 'author', 'price', 'description', 'address', 'poster', 'is_published']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(required=False,
                                             many=True,
                                             # read_only=False,
                                             queryset=City.objects.all(),
                                             slug_field='name')

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'age', 'locations']


class CreateUserSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(required=False,
                                             many=True,
                                             # read_only=False,
                                             queryset=City.objects.all(),
                                             slug_field='name')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'age', 'locations']

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        for city in self._locations:
            location_obj, _ = City.objects.get_or_create(name=city)
            user.locations.add(location_obj)
        user.save()
        return user


class AdsSerializerForSelectionList(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ['id', 'name']


class SelectionsListSerializer(serializers.ModelSerializer):
    items = AdsSerializerForSelectionList(many=True, read_only=True)

    class Meta:
        model = Selections
        fields = ['id', 'name', 'items']


class SelectionsCreateSerializer(serializers.ModelSerializer):
    items = PrimaryKeyRelatedField(required=False,
                                   many=True, queryset=Ads.objects.all())

    class Meta:
        model = Selections
        fields = ['id', 'name', 'items', 'owner']
        read_only_fields = ('owner',)


class SelectionsDetailSerializer(serializers.ModelSerializer):
    # items = serializers.SlugRelatedField(required=False,
    #                                          many=True,
    #                                          # read_only=False,
    #                                          queryset=Ads.objects.all(),
    #                                          slug_field='name')
    items = AdsSerializer(many=True, read_only=True)

    class Meta:
        model = Selections
        fields = ['id', 'items', 'name', 'owner']
