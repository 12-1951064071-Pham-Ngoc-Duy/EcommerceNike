from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
COUNTRY_CHOICES = [
    ('United States', 'United States'),
    ('Canada', 'Canada'),
    ('Mexico', 'Mexico'),
    ('United Kingdom', 'United Kingdom'),
    ('Germany', 'Germany'),
    ('France', 'France'),
    ('Italy', 'Italy'),
    ('Spain', 'Spain'),
    ('Netherlands', 'Netherlands'),
    ('Belgium', 'Belgium'),
    ('Austria', 'Austria'),
    ('Switzerland', 'Switzerland'),
    ('Sweden', 'Sweden'),
    ('Denmark', 'Denmark'),
    ('Norway', 'Norway'),
    ('Finland', 'Finland'),
    ('Ireland', 'Ireland'),
    ('Portugal', 'Portugal'),
    ('Greece', 'Greece'),
    ('Poland', 'Poland'),
    ('Czech Republic', 'Czech Republic'),
    ('Hungary', 'Hungary'),
    ('Romania', 'Romania'),
    ('Russia', 'Russia'),
    ('Australia', 'Australia'),
    ('New Zealand', 'New Zealand'),
    ('Japan', 'Japan'),
    ('South Korea', 'South Korea'),
    ('China', 'China'),
    ('Hong Kong', 'Hong Kong'),
    ('Taiwan', 'Taiwan'),
    ('Singapore', 'Singapore'),
    ('Malaysia', 'Malaysia'),
    ('Thailand', 'Thailand'),
    ('Indonesia', 'Indonesia'),
    ('Philippines', 'Philippines'),
    ('Vietnam', 'Vietnam'),
    ('India', 'India'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Turkey', 'Turkey'),
    ('South Africa', 'South Africa'),
    ('Brazil', 'Brazil'),
    ('Argentina', 'Argentina'),
    ('Chile', 'Chile'),
    ('Colombia', 'Colombia'),
    ('Peru', 'Peru'),
    ('Israel', 'Israel'),
    ('Egypt', 'Egypt'),
]

CITY_CHOICES = {
    'United States': [
        ('New York', 'New York'),
        ('Los Angeles', 'Los Angeles'),
        ('Chicago', 'Chicago'),
        # Thêm các thành phố khác của Mỹ
    ],
    'Canada': [
        ('Toronto', 'Toronto'),
        ('Vancouver', 'Vancouver'),
        ('Montreal', 'Montreal'),
        # Thêm các thành phố khác của Canada
    ],
    'Mexico': [
        ('Mexico City', 'Mexico City'),
        ('Guadalajara', 'Guadalajara'),
        ('Monterrey', 'Monterrey'),
        # Thêm các thành phố khác của Mexico
    ],
    'United Kingdom': [
        ('London', 'London'),
        ('Manchester', 'Manchester'),
        ('Birmingham', 'Birmingham'),
        # Thêm các thành phố khác của Vương Quốc Anh
    ],
    'Germany': [
        ('Berlin', 'Berlin'),
        ('Munich', 'Munich'),
        ('Hamburg', 'Hamburg'),
        # Thêm các thành phố khác của Đức
    ],
    'France': [
        ('Paris', 'Paris'),
        ('Marseille', 'Marseille'),
        ('Lyon', 'Lyon'),
        # Thêm các thành phố khác của Pháp
    ],
    'Italy': [
        ('Rome', 'Rome'),
        ('Milan', 'Milan'),
        ('Naples', 'Naples'),
        # Thêm các thành phố khác của Ý
    ],
    'Spain': [
        ('Madrid', 'Madrid'),
        ('Barcelona', 'Barcelona'),
        ('Valencia', 'Valencia'),
        # Thêm các thành phố khác của Tây Ban Nha
    ],
    # Tiếp tục thêm các lựa chọn thành phố cho các quốc gia khác...
}

VILLAGE_CHOICES = {
    'New York': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của New York
    ],
    'Los Angeles': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Los Angeles
    ],
    'Toronto': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Toronto
    ],
    'Vancouver': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Vancouver
    ],
    'Mexico City': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Mexico City
    ],
    'London': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của London
    ],
    'Berlin': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Berlin
    ],
    'Paris': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Paris
    ],
    'Rome': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Rome
    ],
    # Tiếp tục thêm các lựa chọn làng cho các thành phố khác...
}


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number=None, date_of_birth=None, password=None, country=None, city=None, village=None,place=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            country=country,        # Thêm country
            city=city,              # Thêm city
            village=village,
            place = place,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, phone_number=None, date_of_birth=None, password=None, country=None, city=None, village=None, place=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            country=country,        # Thêm country
            city=city,              # Thêm city
            village=village,
            place=place,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, verbose_name="Tên đầu")
    last_name = models.CharField(max_length=50, verbose_name="Tên cuối")
    username = models.CharField(max_length=50, unique=True, verbose_name="Tên người dùng")
    email = models.EmailField(max_length=50, unique=True, verbose_name="Thư điện tử")
    phone_number = models.CharField(max_length=50,null=True, blank=True, verbose_name="Số điện thoại")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    country = models.CharField(max_length=50,null=True, choices=COUNTRY_CHOICES, verbose_name="Đất nước")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Thành phố")
    village = models.CharField(max_length=50, blank=True, null=True, verbose_name="Huyện")
    place = models.CharField(max_length=255, blank=True, null=True, verbose_name="Địa chỉ")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tham gia")
    last_login = models.DateTimeField(auto_now_add=True, verbose_name="Đăng nhập lần cuối")
    is_admin = models.BooleanField(default=False, verbose_name="Quyền quản trị viên")
    is_staff = models.BooleanField(default=False, verbose_name="Quyền nhân viên")
    is_active = models.BooleanField(default=False, verbose_name="Quyền hoạt động")
    is_superadmin = models.BooleanField(default=False, verbose_name="Quyền siêu quản trị viên")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = MyAccountManager()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    class Meta:
        verbose_name = "Tài khoản người dùng"
        verbose_name_plural = "Tài khoản người dùng"

class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name="Người dùng")
    user_profile_address = models.CharField(max_length=100, blank=True, null=True, verbose_name="Địa chỉ")
    user_profile_picture = models.ImageField(blank=True, null=True,upload_to='userprofile', verbose_name="Ảnh hồ sơ")
    user_profile_country = models.CharField(blank=True, max_length=20, choices=COUNTRY_CHOICES, verbose_name="Đất nước")
    user_profile_city = models.CharField(blank=True, max_length=20, verbose_name="Thành phố")
    user_profile_village = models.CharField(blank=True, max_length=20, verbose_name="Huyện")
    user_profile_date_of_birth = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")

    def __str__(self):
        return self.user.first_name
    class Meta:
        verbose_name = "Hồ sơ người dùng"
        verbose_name_plural = "Hồ sơ người dùng"
    

