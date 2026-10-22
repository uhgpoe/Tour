/**
 * Wanderlust Journeys - Main JavaScript
 * Handles dynamic price calculator, interactions, alerts, and charts.
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Auto-dismiss Bootstrap alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 6000);
  });

  // 2. Dynamic Price Calculator for Booking Page
  const travelersInput = document.getElementById('travelers_count_input');
  const unitPriceElement = document.getElementById('unit_price_val');
  const totalPriceDisplay = document.getElementById('calculated_total_price');
  const subtotalDisplay = document.getElementById('calculated_subtotal');

  if (travelersInput && unitPriceElement && totalPriceDisplay) {
    const unitPrice = parseFloat(unitPriceElement.getAttribute('data-price') || '0');

    function updatePrice() {
      const count = parseInt(travelersInput.value, 10) || 1;
      const total = (count * unitPrice).toFixed(2);
      totalPriceDisplay.textContent = `$${Number(total).toLocaleString()}`;
      if (subtotalDisplay) {
        subtotalDisplay.textContent = `$${Number(total).toLocaleString()}`;
      }
    }

    travelersInput.addEventListener('input', updatePrice);
    travelersInput.addEventListener('change', updatePrice);
    updatePrice();
  }

  // 3. Increment / Decrement Guest Buttons (if present)
  const btnPlus = document.getElementById('btn_guests_plus');
  const btnMinus = document.getElementById('btn_guests_minus');
  if (btnPlus && btnMinus && travelersInput) {
    btnPlus.addEventListener('click', function () {
      let val = parseInt(travelersInput.value, 10) || 1;
      if (val < 20) {
        travelersInput.value = val + 1;
        travelersInput.dispatchEvent(new Event('input'));
      }
    });

    btnMinus.addEventListener('click', function () {
      let val = parseInt(travelersInput.value, 10) || 1;
      if (val > 1) {
        travelersInput.value = val - 1;
        travelersInput.dispatchEvent(new Event('input'));
      }
    });
  }

  // 4. Payment Method Tab/Radio Interaction
  const paymentRadios = document.querySelectorAll('input[name="payment_method"]');
  const cardDetailsSection = document.getElementById('credit_card_details_section');

  if (paymentRadios.length > 0 && cardDetailsSection) {
    paymentRadios.forEach(function (radio) {
      radio.addEventListener('change', function () {
        if (this.value === 'Credit Card' || this.value === 'Debit Card') {
          cardDetailsSection.style.display = 'block';
        } else {
          cardDetailsSection.style.display = 'none';
        }
      });
    });
  }
});
