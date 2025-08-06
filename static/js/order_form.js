if (window._orderFormInitialized) {
  console.warn("order_form.js уже инициализирован!");
} else {
  window._orderFormInitialized = true;

  const SELECTORS = {
    PRODUCTS_SELECT: '#products, select[name="products"]'
  };

  function findElement(selector) {
    const element = document.querySelector(selector);
    if (element) return element;

    const selectors = selector.split(', ');
    for (const singleSelector of selectors) {
      const el = document.querySelector(singleSelector.trim());
      if (el) return el;
    }
    return null;
  }

  function initProductSelect() {
    const productsSelect = findElement(SELECTORS.PRODUCTS_SELECT);

    if (!productsSelect) {
      console.warn("Селект продуктов не найден");
      return;
    }

    // Инициализируем Select2 без поиска
    $(productsSelect).select2({
      placeholder: "Выберите продукты",
      width: "100%",
      minimumResultsForSearch: Infinity // Без поиска
    });
  }

  function initOrderForm() {
    initProductSelect();
  }

  // Инициализация после загрузки DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initOrderForm);
  } else {
    initOrderForm();
  }

  console.log("Order form с продуктами инициализирован");
}
