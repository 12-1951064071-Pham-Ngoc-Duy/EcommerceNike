from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
COUNTRY_CHOICES = [
    ('Vietnam', 'Vietnam')
]

CITY_CHOICES = {
    'Vietnam': [
        ('An Giang', 'An Giang'),
    ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),
    ('Bình Định', 'Bình Định'),
    ('Bình Dương', 'Bình Dương'),
    ('Bình Phước', 'Bình Phước'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Cà Mau', 'Cà Mau'),
    ('Cần Thơ', 'Cần Thơ'),
    ('Cao Bằng', 'Cao Bằng'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Điện Biên', 'Điện Biên'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('Gia Lai', 'Gia Lai'),
    ('Hà Giang', 'Hà Giang'),
    ('Hà Nam', 'Hà Nam'),
    ('Hà Nội', 'Hà Nội'),
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hải Phòng', 'Hải Phòng'),
    ('Hậu Giang', 'Hậu Giang'),
    ('Hòa Bình', 'Hòa Bình'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Kon Tum', 'Kon Tum'),
    ('Lai Châu', 'Lai Châu'),
    ('Lâm Đồng', 'Lâm Đồng'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Lào Cai', 'Lào Cai'),
    ('Long An', 'Long An'),
    ('Nam Định', 'Nam Định'),
    ('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Phú Yên', 'Phú Yên'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Sơn La', 'Sơn La'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
    ('Tiền Giang', 'Tiền Giang'),
    ('TP. Hồ Chí Minh', 'TP. Hồ Chí Minh'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Yên Bái', 'Yên Bái')
    ]
}

VILLAGE_CHOICES = {
    'An Giang': [
        ('Tp. Long Xuyên', 'Tp. Long Xuyên'),
        ('Tp. Châu Đốc', 'Tp. Châu Đốc'),
        ('Thị xã Tân Châu', 'Thị xã Tân Châu'),
        ('Huyện An Phú', 'Huyện An Phú'),
        ('Huyện Châu Phú', 'Huyện Châu Phú'),
        ('Huyện Châu Thành', 'Huyện Châu Thành'),
        ('Huyện Chợ Mới', 'Huyện Chợ Mới'),
        ('Huyện Phú Tân', 'Huyện Phú Tân'),
        ('Huyện Thoại Sơn', 'Huyện Thoại Sơn'),
        ('Huyện Tịnh Biên', 'Huyện Tịnh Biên'),
        ('Huyện Tri Tôn', 'Huyện Tri Tôn'),
    ],
    'Bà Rịa - Vũng Tàu': [
        ('Tp. Vũng Tàu', 'Tp. Vũng Tàu'),
        ('Tp. Bà Rịa', 'Tp. Bà Rịa'),
        ('Thị xã Phú Mỹ', 'Thị xã Phú Mỹ'),
        ('Huyện Châu Đức', 'Huyện Châu Đức'),
        ('Huyện Côn Đảo', 'Huyện Côn Đảo'),
        ('Huyện Đất Đỏ', 'Huyện Đất Đỏ'),
        ('Huyện Long Điền', 'Huyện Long Điền'),
        ('Huyện Xuyên Mộc', 'Huyện Xuyên Mộc'),
    ],
    'Bắc Giang': [
        ('Tp. Bắc Giang', 'Tp. Bắc Giang'),
        ('Huyện Hiệp Hòa', 'Huyện Hiệp Hòa'),
        ('Huyện Lạng Giang', 'Huyện Lạng Giang'),
        ('Huyện Lục Nam', 'Huyện Lục Nam'),
        ('Huyện Lục Ngạn', 'Huyện Lục Ngạn'),
        ('Huyện Sơn Động', 'Huyện Sơn Động'),
        ('Huyện Tân Yên', 'Huyện Tân Yên'),
        ('Huyện Việt Yên', 'Huyện Việt Yên'),
        ('Huyện Yên Dũng', 'Huyện Yên Dũng'),
        ('Huyện Yên Thế', 'Huyện Yên Thế'),
    ],
    'Bắc Ninh': [
        ('Tp. Bắc Ninh', 'Tp. Bắc Ninh'),
        ('Thị xã Từ Sơn', 'Thị xã Từ Sơn'),
        ('Huyện Gia Bình', 'Huyện Gia Bình'),
        ('Huyện Lương Tài', 'Huyện Lương Tài'),
        ('Huyện Quế Võ', 'Huyện Quế Võ'),
        ('Huyện Thuận Thành', 'Huyện Thuận Thành'),
        ('Huyện Tiên Du', 'Huyện Tiên Du'),
        ('Huyện Yên Phong', 'Huyện Yên Phong'),
    ],
    'Cần Thơ': [
        ('Quận Ninh Kiều', 'Quận Ninh Kiều'),
        ('Quận Bình Thủy', 'Quận Bình Thủy'),
        ('Quận Cái Răng', 'Quận Cái Răng'),
        ('Quận Ô Môn', 'Quận Ô Môn'),
        ('Quận Thốt Nốt', 'Quận Thốt Nốt'),
        ('Huyện Cờ Đỏ', 'Huyện Cờ Đỏ'),
        ('Huyện Phong Điền', 'Huyện Phong Điền'),
        ('Huyện Thới Lai', 'Huyện Thới Lai'),
        ('Huyện Vĩnh Thạnh', 'Huyện Vĩnh Thạnh'),
    ],
    'Đà Nẵng': [
        ('Quận Hải Châu', 'Quận Hải Châu'),
        ('Quận Thanh Khê', 'Quận Thanh Khê'),
        ('Quận Sơn Trà', 'Quận Sơn Trà'),
        ('Quận Ngũ Hành Sơn', 'Quận Ngũ Hành Sơn'),
        ('Quận Liên Chiểu', 'Quận Liên Chiểu'),
        ('Quận Cẩm Lệ', 'Quận Cẩm Lệ'),
        ('Huyện Hòa Vang', 'Huyện Hòa Vang'),
        ('Huyện Hoàng Sa', 'Huyện Hoàng Sa'),
    ],
    'Hà Nội': [
        ('Quận Ba Đình', 'Quận Ba Đình'),
        ('Quận Hoàn Kiếm', 'Quận Hoàn Kiếm'),
        ('Quận Hai Bà Trưng', 'Quận Hai Bà Trưng'),
        ('Quận Đống Đa', 'Quận Đống Đa'),
        ('Quận Tây Hồ', 'Quận Tây Hồ'),
        ('Quận Cầu Giấy', 'Quận Cầu Giấy'),
        ('Quận Thanh Xuân', 'Quận Thanh Xuân'),
        ('Quận Hoàng Mai', 'Quận Hoàng Mai'),
        ('Quận Long Biên', 'Quận Long Biên'),
        ('Huyện Ba Vì', 'Huyện Ba Vì'),
        ('Huyện Chương Mỹ', 'Huyện Chương Mỹ'),
        ('Huyện Đan Phượng', 'Huyện Đan Phượng'),
        # Thêm các huyện còn lại
    ],
    'TP. Hồ Chí Minh': [
        ('Quận 1', 'Quận 1'),
        ('Quận 2', 'Quận 2'),
        ('Quận 3', 'Quận 3'),
        ('Quận 4', 'Quận 4'),
        ('Quận 5', 'Quận 5'),
        ('Quận 6', 'Quận 6'),
        ('Quận 7', 'Quận 7'),
        ('Quận 8', 'Quận 8'),
        ('Quận 9', 'Quận 9'),
        ('Quận 10', 'Quận 10'),
        ('Quận 11', 'Quận 11'),
        ('Quận 12', 'Quận 12'),
        ('Huyện Cần Giờ', 'Huyện Cần Giờ'),
        ('Huyện Nhà Bè', 'Huyện Nhà Bè'),
        # Thêm các huyện còn lại
    ],
}


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number=None, date_of_birth=None, password=None, country=None, city=None, village=None,place=None):
        if not email:
            raise ValueError('Người dùng phải có địa chỉ thư điện tử')
        
        if not username:
            raise ValueError('Người dùng phải có tên người dùng')
        
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
    

