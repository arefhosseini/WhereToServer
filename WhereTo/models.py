import os
from enum import Enum

from django.db import models
from django.utils import timezone


def get_user_image_path(instance, filename):
    return os.path.join('media', 'photos', 'users', str(instance.phone_number), filename)


def get_place_image_path(instance, filename):
    return os.path.join('media', 'photos', 'places', str(instance.id), filename)


def get_uploaded_image_path(instance, filename):
    return os.path.join('media', 'photos', 'uploaded_images', str(instance.id), filename)


user_image_path_default = 'photos/users/default.png'
place_image_path_default = 'photos/places/default.png'


class PlaceTypeEnum(Enum):
    Irani = "ایرانی"
    Italian = "ایتالیایی"
    Cafe = "کافه"
    FastFood = "فست فود"


class StateTypeEnum(Enum):
    AzarbayejanSharghi = "آذربایجان شرقی"
    AzarbayejanGharbi = "آذربایجان غربی"
    Ardebil = "اردبیل"
    Isfahan = "اصفهان"
    Alborz = "البرز"
    Ilam = "ایلام"
    Booshehr = "بوشهر"
    Tehran = "تهران"
    ChaharMahal = "چهارمحال و بختیاری"
    SouthKhorasan = "خراسان جنوبی"
    KhorasanRazavi = "خراسان رضوی"
    NorthKhorasan = "خراسان شمالی"
    Khoozestan = "خوزستان"
    Zanjan = "زنجان"
    Semnan = "سمنان"
    Sistan = "سیستان و بلوچستان"
    Fars = "فارس"
    Ghazvin = "قزوین"
    Ghom = "قم"
    Kordestan = "کردستان"
    Kerman = "کرمان"
    KermanShah = "کرمانشاه"
    Kohgilooye = "کهگیلویه و بویراحمد"
    Golestan = "گلستان"
    Gilan = "گیلان"
    Lorestan = "لرستان"
    Mazandaran = "مازندران"
    Markazi = "مرکزی"
    Hormozgan = "هرمزگان"
    Hamedan = "همدان"
    Yazd = "یزد"


# noinspection SpellCheckingInspection
class TypeCityEnum(Enum):
    Tabriz = "تبریز"
    Maraghe = "	مراغه"
    Marand = "مرند"
    Ahar = "اهر"
    Oroomie = "ارومیه"
    Khooy = "خوی"
    MianDoab = "میاندوآب"
    Mahabad = "مهاباد"
    Ardebil = "اردبیل"
    ParsAbad = "پارس‌آباد"
    MeshkinShahr = "مشگین‌شهر"
    Khalkhal = "خلخال"
    Isfahan = "اصفهان"
    Kashan = "کاشان"
    KhemoeiniShahr = "خمینی‌شهر"
    NajafAbad = "نجف‌آباد"
    Karaj = "کرج"
    KamalShahr = "کمال‌شهر"
    NazarAbad = "نظرآباد"
    MohammadShahr = "محمدشهر"
    Ilam = "ایلام"
    Dehloran = "دهلران"
    Ivan = "ایوان"
    Abdanan = "آبدانان"
    Booshehr = "بوشهر"
    Borazjan = "برازجان"
    BandarKangan = "بندر کنگان"
    BandarGonave = "بندر گناوه"
    Tehran = "تهران"
    EslamShahr = "اسلامشهر"
    Malard = "ملارد"
    Ghods = "قدس"
    ShahrKord = "شهرکرد"
    Boroojen = "بروجن"
    Lordegan = "لردگان"
    FarokhShahr = "فرخ‌شهر"
    Birjand = "بیرجند"
    Ghaen = "	قائن"
    Tabas = "طبس"
    Ferdos = "فردوس"
    Mashhad = "مشهد"
    Neishaboor = "نیشابور"
    Sabzevar = "سبزوار"
    Ghoochan = "قوچان"
    TorbatHeidarie = "تربت حیدریه"
    Bojnord = "بجنورد"
    Shiravan = "شیروان"
    Esfarayen = "اسفراین"
    Ashkhane = "آشخانه"
    Ahvaz = "اهواز"
    Andika = "	اندیکا"
    Abadan = "آبادان"
    BandarMahShahr = "بندر ماهشهر"
    Zanjan = "زنجان"
    Abhar = "ابهر"
    Khoramdare = "خرمدره"
    Gheidar = "قیدار"
    Semnan = "سمنان"
    Shahrood = "شاهرود"
    Damghan = "دامغان"
    Garmsar = "گرمسار"
    Zahedan = "زاهدان"
    Zabol = "زابل"
    IranShahr = "ایرانشهر"
    Chabahar = "چابهار"
    Shiraz = "شیراز"
    MarvShahr = "مرودشت"
    Jahrom = "جهرم"
    FiroozAbad = "فیروزآباد"
    Ghazvin = "قزوین"
    Alvand = "الوند"
    Takestan = "تاکستان"
    BooeenZahra = "بوئین زهرا"
    Ghom = "قم"
    Ghanavat = "قنوات"
    Jafarie = "جعفریه"
    Kahak = "کهک"
    Sanandaj = "سنندج"
    Saghez = "سقز"
    Marivan = "مریوان"
    Bane = "بانه"
    Kerman = "کرمان"
    Sirjan = "سیرجان"
    Rafsanjan = "رفسنجان"
    Jiroft = "جیرفت"
    KermanShah = "کرمانشاه"
    EslamAbadGharb = "اسلام‌آباد غرب"
    Kangavar = "کنگاور"
    JavanRood = "جوانرود"
    Yasooj = "یاسوج"
    DoGonbadan = "دوگنبدان"
    Dehdasht = "دهدشت"
    Gorgan = "گرگان"
    GonbadKavoos = "گنبد کاووس"
    AliAbadKatool = "علی‌آباد کتول"
    BandarTorkaman = "بندر ترکمن"
    Rasht = "رشت"
    BandarAnzali = "بندر انزلی"
    Lahijan = "لاهیجان"
    Langerood = "لنگرود"
    KhoramAbad = "خرم‌آباد"
    Boroojerd = "بروجرد"
    Dorood = "دورود"
    KoohDasht = "کوهدشت"
    Sari = "ساری"
    Amol = "آمل"
    Babol = "بابل"
    GhaemShahr = "قائم‌شهر"
    Arak = "اراک"
    Save = "ساوه"
    Khomein = "خمین"
    Mahalat = "محلات"
    BandarAbas = "	بندرعباس"
    Minab = "میناب"
    Dehbarez = "دهبارز"
    BandarLenge = "بندر لنگه"
    Hamedan = "همدان"
    Malayer = "ملایر"
    Nahavand = "نهاوند"
    AsadAbad = "اسدآباد"
    Yazd = "یزد"
    Meibod = "میبد"
    Ardakan = "اردکان"
    Hamidia = "حمیدیا"


class Token(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    verify_code = models.CharField(max_length=5, null=False)

    def __str__(self):
        return "%s %s" % (self.phone_number, self.verify_code)


class User(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=50, default="", blank=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    user_score = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to=get_user_image_path, blank=True,
                                      null=True, default=user_image_path_default)

    def __str__(self):
        return self.phone_number


class Place(models.Model):
    name = models.CharField(max_length=100, null=False)
    price_degree = models.IntegerField(default=0)
    address = models.CharField(max_length=500, default="", blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    open_hours = models.TextField(default="", blank=True)
    price = models.CharField(max_length=100, default="", blank=True)
    features = models.CharField(max_length=200, default="", blank=True)
    state = models.CharField(
        max_length=100,
        choices=[(tag.name, tag.value) for tag in StateTypeEnum],
        null=False
    )
    city = models.CharField(
        max_length=100,
        choices=[(tag.name, tag.value) for tag in TypeCityEnum],
        null=False
    )
    place_image = models.ImageField(upload_to=get_place_image_path, blank=True,
                                    null=True, default=place_image_path_default)

    def __str__(self):
        return self.name


class PlaceType(models.Model):
    place = models.ForeignKey(Place, related_name="place_types", on_delete=models.CASCADE, null=False)
    type = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in PlaceTypeEnum],
        null=False
    )

    def __str__(self):
        return self.type


class PlaceScore(models.Model):
    user = models.ForeignKey(User, related_name="place_scores", on_delete=models.CASCADE, null=False)
    place = models.ForeignKey(Place, related_name="place_scores", on_delete=models.CASCADE, null=False)
    total_score = models.IntegerField(default=0)
    food_score = models.IntegerField(default=0)
    service_score = models.IntegerField(default=0)
    ambiance_score = models.IntegerField(default=0)

    def __str__(self):
        return "%s %s" % (self.user, self.place)


class CoordinatePlace(models.Model):
    place = models.ForeignKey(Place, related_name="coordinate_place", on_delete=models.CASCADE, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)

    def __str__(self):
        return "%s %s" % (self.latitude, self.longitude)


class PhonePlace(models.Model):
    place = models.ForeignKey(Place, related_name="phones_place", on_delete=models.CASCADE, null=False)
    phone_number = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.phone_number


class PlaceImage(models.Model):
    user = models.ForeignKey(User, related_name="place_images", on_delete=models.CASCADE, null=False)
    place = models.ForeignKey(Place, related_name="place_images", on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=get_uploaded_image_path, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.user, self.place)


class FavoritePlace(models.Model):
    user = models.ForeignKey(User, related_name="favorite_places", on_delete=models.CASCADE, null=False)
    place = models.ForeignKey(Place, related_name="favorite_places", on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s %s" % (self.user, self.place)


class Menu(models.Model):
    place = models.ForeignKey(Place, related_name="menus", on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class Food(models.Model):
    menu = models.ForeignKey(Menu, related_name="foods", on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200, null=False)
    detail = models.CharField(max_length=200, default="", blank=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Relation(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings', null=False)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s %s" % (self.follower, self.following)


class Review(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE, null=False)
    place = models.ForeignKey(Place, related_name="reviews", on_delete=models.CASCADE, null=False)
    text = models.TextField(default="", null=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class Hashtag(models.Model):
    place = models.ForeignKey(Place, related_name="hashtags", on_delete=models.CASCADE, null=False)
    review = models.ForeignKey(Review, related_name="hashtags", on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class ReviewVote(models.Model):
    review = models.ForeignKey(Review, related_name="review_votes", on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, related_name="review_votes", on_delete=models.CASCADE, null=False)
    vote = models.IntegerField(null=False)


class PlaceImageVote(models.Model):
    place_image = models.ForeignKey(PlaceImage, related_name="place_image_votes", on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, related_name="place_image_votes", on_delete=models.CASCADE, null=False)
    vote = models.IntegerField(null=False)


class FavoritePlaceType(models.Model):
    user = models.ForeignKey(User, related_name="favorite_place_types", on_delete=models.CASCADE, null=False)
    type = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in PlaceTypeEnum],
        null=False
    )

    def __str__(self):
        return self.type
