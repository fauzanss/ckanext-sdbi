document.addEventListener('DOMContentLoaded', function () {
  // Step Navigation
  document.querySelectorAll('.next-step').forEach(function (button) {
    button.addEventListener('click', function () {
      const currentStep = this.closest('.form-step');
      const nextStep = currentStep.nextElementSibling;

      if (validateCurrentStep(currentStep)) {
        currentStep.classList.remove('active');
        nextStep.classList.add('active');
        updateProgressSteps();
      }
    });
  });

  document.querySelectorAll('.prev-step').forEach(function (button) {
    button.addEventListener('click', function () {
      const currentStep = this.closest('.form-step');
      const prevStep = currentStep.previousElementSibling;

      currentStep.classList.remove('active');
      prevStep.classList.add('active');
      updateProgressSteps();
    });
  });

  // Step Click Navigation
  document.querySelectorAll('.step').forEach(function (step) {
    step.addEventListener('click', function () {
      const stepNumber = this.dataset.step;
      document.querySelectorAll('.form-step').forEach(function (formStep) {
        formStep.classList.remove('active');
      });
      document.querySelector(`.form-step[data-step="${stepNumber}"]`).classList.add('active');
      updateProgressSteps();
    });
  });

  // Update Progress Steps
  function updateProgressSteps() {
    const activeStep = document.querySelector('.form-step.active').dataset.step;
    document.querySelectorAll('.step').forEach(function (step) {
      step.classList.remove('active', 'completed');
    });

    document.querySelectorAll('.step').forEach(function (step) {
      const stepNum = step.dataset.step;
      if (stepNum < activeStep) {
        step.classList.add('completed');
      } else if (stepNum == activeStep) {
        step.classList.add('active');
      }
    });
  }

  // Validate Current Step
  function validateCurrentStep(step) {
    const stepNumber = step.dataset.step;
    let isValid = true;

    if (stepNumber == 1) {
      const title = document.getElementById('title').value.trim();
      if (!title) {
        showError('Judul form harus diisi');
        isValid = false;
      }
    } else if (stepNumber == 2) {
      const url = document.getElementById('form_url').value.trim();
      if (!url) {
        showError('URL Google Form harus diisi');
        isValid = false;
      } else if (!isValidGoogleFormsUrl(url)) {
        showError('URL Google Form tidak valid');
        isValid = false;
      }
    }

    return isValid;
  }

  // URL Validation
  const formUrlInput = document.getElementById('form_url');
  if (formUrlInput) {
    formUrlInput.addEventListener('input', function () {
      const url = this.value.trim();
      const validation = document.getElementById('urlValidation');

      if (!url) {
        validation.classList.remove('valid', 'invalid');
        validation.textContent = '';
      } else if (isValidGoogleFormsUrl(url)) {
        validation.classList.remove('invalid');
        validation.classList.add('valid');
        validation.innerHTML = '<i class="fa fa-check"></i> URL Google Form valid';
      } else {
        validation.classList.remove('valid');
        validation.classList.add('invalid');
        validation.innerHTML = '<i class="fa fa-times"></i> URL Google Form tidak valid';
      }
    });
  }

  function isValidGoogleFormsUrl(url) {
    return url.match(/^https:\/\/(forms\.google\.com|docs\.google\.com\/forms)\/.+/);
  }

  // Status Toggle
  document.querySelectorAll('.status-label').forEach(function (label) {
    label.addEventListener('click', function () {
      document.querySelectorAll('.status-label').forEach(function (l) {
        l.classList.remove('active');
      });
      this.classList.add('active');
      this.previousElementSibling.checked = true;
    });
  });

  // Form Review
  document.querySelectorAll('.next-step').forEach(function (button) {
    button.addEventListener('click', function () {
      if (this.closest('.form-step').dataset.step == 2) {
        updateReview();
      }
    });
  });

  function updateReview() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const formUrl = document.getElementById('form_url').value;
    const category = document.querySelector('input[name="category"]:checked').value;
    const status = document.querySelector('input[name="status"]:checked').value;
    const exitIntent = document.getElementById('exit_intent').checked;

    document.getElementById('reviewTitle').textContent = title;
    document.getElementById('reviewDescription').textContent = description || 'Tidak ada deskripsi';
    document.getElementById('reviewUrl').textContent = formUrl;
    document.getElementById('reviewCategory').textContent = getCategoryName(category);
    document.getElementById('reviewStatus').textContent = getStatusName(status);
    document.getElementById('review-exit-intent').textContent = exitIntent ? 'Ya' : 'Tidak';
  }

  function getCategoryName(category) {
    const categories = {
      'bencana': 'Bencana Alam',
      'kesiapsiagaan': 'Kesiapsiagaan',
      'evakuasi': 'Evakuasi',
      'rehabilitasi': 'Rehabilitasi',
      'lainnya': 'Lainnya'
    };
    return categories[category] || category;
  }

  function getStatusName(status) {
    const statuses = {
      'active': 'Aktif',
      'inactive': 'Tidak Aktif',
      'draft': 'Draft'
    };
    return statuses[status] || status;
  }

  function showError(message) {
    // Create error alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade in';
    alertDiv.innerHTML = `
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
      <i class="fa fa-exclamation-triangle"></i> ${message}
    `;

    // Insert at top of form
    const form = document.getElementById('createForm');
    form.insertBefore(alertDiv, form.firstChild);

    // Auto remove after 5 seconds
    setTimeout(function () {
      if (alertDiv.parentNode) {
        alertDiv.parentNode.removeChild(alertDiv);
      }
    }, 5000);
  }

  // Tips modal
  const tipsModal = document.getElementById('tipsModal');
  const tipsButton = document.getElementById('tipsButton');
  const tipsClose = document.querySelector('.tips-close');

  if (tipsButton) {
    tipsButton.addEventListener('click', function () {
      tipsModal.style.display = 'block';
    });
  }

  if (tipsClose) {
    tipsClose.addEventListener('click', function () {
      tipsModal.style.display = 'none';
    });
  }

  // Close modal when clicking outside
  window.addEventListener('click', function (event) {
    if (event.target == tipsModal) {
      tipsModal.style.display = 'none';
    }
  });
}); 