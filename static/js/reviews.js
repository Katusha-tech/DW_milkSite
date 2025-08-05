/* JavaScript для работы с формой отзывов */
document.addEventListener("DOMContentLoaded", function () {
    // Инициализация обработчика для звездочек рейтинга
    initRatingStats();
    // Инициализация валидации формы
    initFormValidation();
});

/* Инициализация обработчика для звездочек рейтинга */
function initRatingStats() {
    const stars = document.querySelectorAll('.star-rating-item');
    const ratingInput = document.getElementById('rating-value');
    
    // ✅ Общая функция для обновления звездочек
    function setStarsState(rating) {
        stars.forEach((star) => {
            const starValue = star.getAttribute("data-rating");
            // Используем toggle для более элегантного переключения классов
            star.classList.toggle("bi-star-fill", starValue <= rating);
            star.classList.toggle("bi-star", starValue > rating);
        });
    }
    
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.getAttribute("data-rating");
            ratingInput.value = rating;
            // Используем общую функцию
            setStarsState(rating);
        });
               
        // Добавляем эффект при наведении
        star.addEventListener("mouseover", function () {
            const hoverRating = this.getAttribute("data-rating");
            // Используем общую функцию
            setStarsState(hoverRating);
        });
        
        // Возвращаем выбранное состояние при уходе курсора
        star.addEventListener("mouseout", function () {
            const currentRating = ratingInput.value || 0;
            // Используем общую функцию
            setStarsState(currentRating);
        });
    });
}

/* Инициализация клиентской валидации формы */
function initFormValidation() {
    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
        reviewForm.addEventListener("submit", function (event) {
            if (!validateReviewForm()) {
                event.preventDefault();
            }
        });
    }
    
    /* Основная функция валидации формы */
    function validateReviewForm() {
        let isValid = true;
        
        // Валидация имени клиента
        const clientNameInput = document.getElementById("id_client_name");
        if (clientNameInput && clientNameInput.value.trim() === "") {
            isValid = false;
            showError(clientNameInput, "Пожалуйста, укажите ваше имя");
        } else if (clientNameInput) {
            clearError(clientNameInput);
        }
        
        // Валидация текста отзыва
        const textInput = document.getElementById("id_text");
        if (textInput && textInput.value.trim() === "") {
            isValid = false;
            showError(textInput, "Пожалуйста, напишите текст отзыва");
        } else if (textInput && textInput.value.trim().length < 10) {
            isValid = false;
            showError(
                textInput,
                "Текст отзыва должен содержать не менее 10 символов"
            );
        } else if (textInput) {
            clearError(textInput);
        }
        
        // Валидация рейтинга
        const ratingInput = document.getElementById("id_rating");
        if (ratingInput && (!ratingInput.value || parseInt(ratingInput.value) < 1)) {
            isValid = false;
            // Показываем ошибку возле звездочек
            const ratingStars = document.querySelector(".rating-stars");
            if (ratingStars) {
                showErrorNear(ratingStars, "Пожалуйста, выберите оценку");
            }
        } else {
            // Убираем сообщение об ошибке возле звездочек
            const ratingStars = document.querySelector(".rating-stars");
            if (ratingStars) {
                clearErrorNear(ratingStars);
            }
        }
        
    }
    
    /* Показ сообщения об ошибке */
    function showError(element, message) {
        // Удаляем предыдущую ошибку
        clearError(element);
        // Добавляем класс is-invalid
        element.classList.add("is-invalid");
        // Создаем элемент для сообщения об ошибке
        const errorDiv = document.createElement("div");
        errorDiv.className = "invalid-feedback";
        errorDiv.textContent = message;
        // Добавляем сообщение после элемента
        element.parentNode.appendChild(errorDiv);
    }
    
    /* Показ сообщения об ошибке рядом с элементом (не для input) */
    function showErrorNear(element, message) {
        // Удаляем предыдущую ошибку
        clearErrorNear(element);
        // Создаем элемент для сообщения об ошибке
        const errorDiv = document.createElement("div");
        errorDiv.className = "text-danger mt-2 rating-error";
        errorDiv.textContent = message;
        // Добавляем сообщение после элемента
        element.parentNode.appendChild(errorDiv);
    }
    
    /* Очистка сообщения об ошибке для input */
    function clearError(element) {
        // Убираем класс is-invalid
        element.classList.remove("is-invalid");
        // Удаляем сообщение об ошибке, если оно есть
        const errorMessage = element.parentNode.querySelector(".invalid-feedback");
        if (errorMessage) {
            errorMessage.remove();
        }
    }
    
    /* Очистка сообщения об ошибке рядом с элементом */
    function clearErrorNear(element) {
        // Удаляем сообщение об ошибке, если оно есть
        const errorMessage = element.parentNode.querySelector(".rating-error");
        if (errorMessage) {
            errorMessage.remove();
        }
    }
}