from api.models import Photo, AlbumAuto, AlbumUser, AlbumPlace, Face, Person, AlbumDate, AlbumThing
from rest_framework import serializers
import ipdb
import json
import time

class PhotoHashListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'image_hash',)

class PhotoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
           'thumbnail',
           'square_thumbnail', 
           'image',
           'image_hash',
           'exif_timestamp',
           'exif_gps_lat',
           'exif_gps_lon',
           'favorited',
           'geolocation_json',
        )


class PhotoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    thumbnail_height = serializers.SerializerMethodField()
    thumbnail_width = serializers.SerializerMethodField()
    square_thumbnail_url = serializers.SerializerMethodField()
    small_thumbnail_url = serializers.SerializerMethodField()
    big_thumbnail_url = serializers.SerializerMethodField()
    big_square_thumbnail_url = serializers.SerializerMethodField()
    small_square_thumbnail_url = serializers.SerializerMethodField()
    tiny_square_thumbnail_url = serializers.SerializerMethodField()


    image_url = serializers.SerializerMethodField()
    people = serializers.SerializerMethodField()
    # geolocation = serializers.SerializerMethodField()
    # persons = PersonSerializer(many=True, read_only=True)
    class Meta:
        model = Photo
        fields = ('exif_gps_lat',
                  'exif_gps_lon',
                  'exif_timestamp',
                  'search_captions',
                  'search_location',
                  'thumbnail_url',
                  'thumbnail_height',
                  'thumbnail_width',
                  'small_thumbnail_url',
                  'big_thumbnail_url',

                  'square_thumbnail_url',
                  'big_square_thumbnail_url',
                  'small_square_thumbnail_url',
                  'tiny_square_thumbnail_url',

                  'geolocation_json',
                  'exif_json',
                  'people',
                  'image_url',
                  'image_hash',
                  'image_path',
                  'favorited')
        
    def get_thumbnail_url(self, obj):
        try:
            return obj.thumbnail.url
        except:
            return None
    def get_thumbnail_height(self, obj):
        try:
            return obj.thumbnail.height
        except:
            return None
    def get_thumbnail_width(self, obj):
        try:
            return obj.thumbnail.width
        except:
            return None
    def get_square_thumbnail_url(self, obj):
        try:
            return obj.square_thumbnail.url
        except:
            return None
    def get_small_thumbnail_url(self, obj):
        try:
            return obj.thumbnail_small.url
        except:
            return None

    def get_big_square_thumbnail_url(self, obj):
        try:
            return obj.square_thumbnail_big.url
        except:
            return None


    def get_small_square_thumbnail_url(self, obj):
        try:
            return obj.square_thumbnail_small.url
        except:
            return None


    def get_tiny_square_thumbnail_url(self, obj):
        try:
            return obj.square_thumbnail_tiny.url
        except:
            return None



    def get_big_thumbnail_url(self, obj):
        try:
            return obj.thumbnail_big.url
        except:
            return None
    def get_image_url(self, obj):
        try:
            return obj.image.url
        except:
            return None
    def get_geolocation(self, obj):
        if obj.geolocation_json:
          return json.loads(obj.geolocation_json)
        else:
          return None

    def get_people(self,obj):
        return [f.person.name for f in obj.faces.all()]

class PersonSerializer(serializers.ModelSerializer):
#     faces = FaceSerializer(many=True, read_only=False)
#     faces = serializers.StringRelatedField(many=True)
#     photos = serializers.SerializerMethodField()
    face_url = serializers.SerializerMethodField()  
    face_count = serializers.SerializerMethodField()  
    face_photo_url = serializers.SerializerMethodField()  
    class Meta:
        model = Person
        fields = ('name',
                  'face_url',
                  'face_count',
                  'face_photo_url',
                  'id',)

    def get_face_count(self,obj):
        return obj.faces.all().count()

    def get_face_url(self,obj):
        try:
            face = obj.faces.first()
            return face.image.url
        except:
            return None

    def get_face_photo_url(self,obj):
        try:
            face = obj.faces.first()
            return face.photo.square_thumbnail.url
        except:
            return None


    def create(self,validated_data):
        name = validated_data.pop('name')
        qs = Person.objects.filter(name=name)
        if qs.count() > 0:
            return qs[0]
        else:
            new_person = Person()
            new_person.name = name
            new_person.save()
            print('created person with name %s'%name)
            return new_person


#     def get_photos(self,obj):
#         faces = obj.faces.all()
#         res = []
#         for face in faces:
#             res.append(PhotoSerializer(face.photo).data)
#         return res



class FaceListSerializer(serializers.ModelSerializer):
    person_name = serializers.SerializerMethodField()
    class Meta:
        model = Face
        fields = ('id',
                  'image',
                  'person',
                  'person_name')

    def get_person_name(self,obj):
        return obj.person.name






class FaceSerializer(serializers.ModelSerializer):
    face_url = serializers.SerializerMethodField()
#     photo = PhotoSerializer(many=False, read_only=True)
    # faces = serializers.StringRelatedField(many=True)
    person = PersonSerializer(many=False)
#     person = serializers.HyperlinkedRelatedField(view_name='person-detail',read_only=True)
    class Meta:
        model = Face
        fields = ('id',
                  'face_url',
                  'photo_id',
                  'person',
                  'person_id',
                  'person_label_is_inferred')
    def get_face_url(self, obj):
        return obj.image.url

    def update(self, instance, validated_data):
        name = validated_data.pop('person')['name']
        p = Person.objects.filter(name=name)
        if p.count() > 0:
            instance.person = p[0]
        else:
            p = Person()
            p.name = name
            p.save()
            instance.person = p
            print('created person with name %s'%name)
        if instance.person.name == 'unknown':
            instance.person_label_is_inferred = None
        else:
            instance.person_label_is_inferred = False
        print('updated label for face %d to %s'%(instance.id, instance.person.name))
        instance.save()
        return instance
#         pass
#         ipdb.set_trace()
#         person_data = validated_data.pop('id')











class AlbumPlaceSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = AlbumPlace
        fields = (
            "id",   
            "title",
            "photos")

class AlbumPlaceListSerializer(serializers.ModelSerializer):
#     photos = PhotoSerializer(many=True, read_only=True)
    # people = serializers.SerializerMethodField()
    cover_photo_urls = serializers.SerializerMethodField()
    photo_count = serializers.SerializerMethodField()

    class Meta:
        model = AlbumPlace
        fields = (
            "id",   
            # "people",
            "cover_photo_urls",
            "title",
            "photo_count")

    def get_photo_count(self,obj):
        return obj.photos.count()

    def get_cover_photo_urls(self,obj):
        first_photos = obj.photos.all()[:4]
        return [first_photo.square_thumbnail.url for first_photo in first_photos]















class AlbumThingSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = AlbumThing
        fields = (
            "id",   
            "title",
            "photos")

class AlbumThingListSerializer(serializers.ModelSerializer):
#     photos = PhotoSerializer(many=True, read_only=True)
    # people = serializers.SerializerMethodField()
    cover_photo_urls = serializers.SerializerMethodField()
    photo_count = serializers.SerializerMethodField()

    class Meta:
        model = AlbumThing
        fields = (
            "id",   
            # "people",
            "cover_photo_urls",
            "title",
            "photo_count")

    def get_photo_count(self,obj):
        return obj.photos.count()

    def get_cover_photo_urls(self,obj):
        first_photos = obj.photos.all()[:4]
        return [first_photo.square_thumbnail.url for first_photo in first_photos]
















class AlbumDateSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = AlbumDate
        fields = (
            "id",   
            "title",
            "date",
            "favorited",
            "photos")

class AlbumDateListSerializer(serializers.ModelSerializer):
#     photos = PhotoSerializer(many=True, read_only=True)
    people = serializers.SerializerMethodField()
    cover_photo_url = serializers.SerializerMethodField()
    photo_count = serializers.SerializerMethodField()
#     photos = PhotoHashListSerializer(many=True, read_only=True)

    class Meta:
        model = AlbumDate
        fields = (
            "id",   
            "people",
            "cover_photo_url",
            "title",
            "favorited",
            "photo_count",
#             "photos",
            "date")

    def get_photo_count(self,obj):
        return obj.photos.count()

    def get_cover_photo_url(self,obj):
        first_photo = obj.photos.first()
        return first_photo.square_thumbnail.url

    def get_people(self,obj):
        # ipdb.set_trace()
        photos = obj.photos.all()
        res = []
        for photo in photos:
            faces = photo.faces.all()
            for face in faces:
                serialized_person = PersonSerializer(face.person).data
                if serialized_person not in res:
                    res.append(serialized_person)
        return res

class AlbumDateListWithPhotoHashSerializer(serializers.ModelSerializer):
    photos = PhotoHashListSerializer(many=True, read_only=True)
    class Meta:
        model = AlbumDate
        fields = (
            "id",   
            "photos",
            "date")





class AlbumPersonSerializer(serializers.ModelSerializer):
#     faces = FaceSerializer(many=True, read_only=False)
#     faces = serializers.StringRelatedField(many=True)
    photos = serializers.SerializerMethodField()
    # people = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = ('name',
                  'photos',
                  # 'people',
                  'id',)
#                   'faces')
    def get_photos(self,obj):
        faces = obj.faces.all()
        res = []
        for face in faces:
            res.append(PhotoSimpleSerializer(face.photo).data)
        return res

    # todo: remove this unecessary thing
    # def get_people(self,obj):
    #     faces = obj.faces.all()
    #     res = []
    #     for face in faces:
    #         serialized_person = PersonSerializer(face.person).data
    #         if serialized_person not in res:
    #             res.append(serialized_person)
    #     return res


class AlbumPersonListSerializer(serializers.ModelSerializer):
#     faces = FaceSerializer(many=True, read_only=False)
#     faces = serializers.StringRelatedField(many=True)
#     people = serializers.SerializerMethodField()
    photo_count = serializers.SerializerMethodField()
    cover_photo_url = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = ('name',
                  "photo_count",
                  "cover_photo_url",
#                   'people',
                  'id',)
#                   'faces')

    def get_photo_count(self,obj):
        return obj.faces.count()

    def get_cover_photo_url(self,obj):
        first_face = obj.faces.first()
        if first_face:
            return first_face.photo.square_thumbnail.url
        else:
            return None

    def get_face_photo_url(self,obj):
        first_face = obj.faces.first()
        if first_face:
            return first_face.image.url
        else:
            return None







class AlbumAutoSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=False)
    people = serializers.SerializerMethodField()

    class Meta:
        model = AlbumAuto
        fields = (
            "id",   
            "title",
            "favorited",
            "timestamp",
            "created_on",
            "gps_lat",
            'people',
            "gps_lon",
            "photos")

    def get_people(self,obj):
        # ipdb.set_trace()
        photos = obj.photos.all()
        res = []
        for photo in photos:
            faces = photo.faces.all()
            for face in faces:
                serialized_person = PersonSerializer(face.person).data
                if serialized_person not in res:
                    res.append(serialized_person)
        return res


class AlbumAutoListSerializer(serializers.ModelSerializer):
    photos = PhotoHashListSerializer
    
    class Meta:
        model = AlbumAuto
        fields = (
            "id",   
            "title",
            "timestamp",
            "photos",
            "favorited")

