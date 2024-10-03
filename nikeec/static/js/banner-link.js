const tooltipButtonBanner = document.getElementById('tooltipButtonBanner');
const tooltipMessageBanner = document.getElementById('tooltipMessageBanner');

tooltipButtonBanner.addEventListener('mouseenter', () => {
    tooltipMessageBanner.style.display = 'block'; // Hiển thị tooltip
});

tooltipButtonBanner.addEventListener('mouseleave', () => {
    tooltipMessageBanner.style.display = 'none'; // Ẩn tooltip
});