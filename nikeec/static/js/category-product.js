document.addEventListener("DOMContentLoaded", function () {
    var swiper = new Swiper('.mySwiper', {
        loop: true,  // Để carousel lặp lại
        slidesPerView: 3,  // Hiển thị 3 slide mỗi lần
        spaceBetween: 20,  // Khoảng cách giữa các slide
        navigation: {
            nextEl: '.swiper-button-next',  // Nút dịch phải
            prevEl: '.swiper-button-prev',  // Nút dịch trái
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,  // Cho phép click vào các dấu chấm phân trang
        },
        breakpoints: {
            1259: {
                slidesPerView: 5,  // Hiển thị 2 slide trên màn hình nhỏ hơn
            },
            768: {
                slidesPerView: 2,  // Hiển thị 2 slide trên màn hình nhỏ hơn
            },
            480: {
                slidesPerView: 1,  // Hiển thị 1 slide trên màn hình rất nhỏ
            }
        }
    });
});

/// Tooltip
const tooltipButton = document.getElementById('tooltipButton');
const tooltipMessage = document.getElementById('tooltipMessage');

tooltipButton.addEventListener('mouseenter', () => {
    tooltipMessage.style.display = 'block'; // Hiển thị tooltip
});

tooltipButton.addEventListener('mouseleave', () => {
    tooltipMessage.style.display = 'none'; // Ẩn tooltip
});
