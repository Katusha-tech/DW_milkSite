document.querySelectorAll('.product-checkbox').forEach((checkbox, index) => {
      checkbox.addEventListener('change', function () {
        const input = document.querySelector(`#quantity_${this.value}`);
        input.disabled = !this.checked;
        if (this.checked && input.value === "0") {
          input.value = "1";
        } else if (!this.checked) {
          input.value = "0";
        }
      });
    });
