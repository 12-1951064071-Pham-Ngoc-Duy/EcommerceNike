// Lấy các phần tử nút và trường input
const btnMinus = document.getElementById('btn-minus');
const btnPlus = document.getElementById('btn-plus');
const quantityInput = document.getElementById('quantity-input');

// Sự kiện cho nút trừ
btnMinus.addEventListener('click', () => {
  let currentValue = parseInt(quantityInput.value);
  if (currentValue > 1) { // Đảm bảo số lượng không giảm dưới 1
    quantityInput.value = currentValue - 1;
  }
});

// Sự kiện cho nút cộng
btnPlus.addEventListener('click', () => {
  let currentValue = parseInt(quantityInput.value);
  quantityInput.value = currentValue + 1;
});
