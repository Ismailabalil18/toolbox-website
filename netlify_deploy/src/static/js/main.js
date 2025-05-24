// Main JavaScript file for ToolBox

// Initialize Lucide icons when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
  
  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      document.querySelector('.main-nav').classList.toggle('active');
    });
  }
  
  // File upload highlighting
  const fileDropAreas = document.querySelectorAll('.file-upload');
  fileDropAreas.forEach(function(dropArea) {
    if (!dropArea) return;
    
    const fileInput = dropArea.querySelector('input[type="file"]');
    if (!fileInput) return;
    
    // Highlight drop area when file is dragged over
    ['dragenter', 'dragover'].forEach(eventName => {
      dropArea.addEventListener(eventName, function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropArea.classList.add('highlight');
      });
    });
    
    // Remove highlight when file is dragged out
    ['dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropArea.classList.remove('highlight');
      });
    });
    
    // Handle file drop
    dropArea.addEventListener('drop', function(e) {
      fileInput.files = e.dataTransfer.files;
      updateFileInfo(dropArea, fileInput);
    });
    
    // Handle file selection
    dropArea.addEventListener('click', function() {
      fileInput.click();
    });
    
    fileInput.addEventListener('change', function() {
      updateFileInfo(dropArea, fileInput);
    });
  });
  
  function updateFileInfo(dropArea, fileInput) {
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      const fileSize = (file.size / (1024 * 1024)).toFixed(2); // Convert to MB
      
      const textElement = dropArea.querySelector('p');
      if (textElement) {
        textElement.textContent = file.name;
      }
      
      const infoElement = dropArea.querySelector('.file-upload-info');
      if (infoElement) {
        infoElement.textContent = `${fileSize} MB`;
      }
      
      const convertBtn = document.getElementById('convert-btn');
      if (convertBtn) {
        convertBtn.disabled = false;
      }
    }
  }
});

// Progress bar animation
function animateProgressBar(progressBar, duration = 10000, targetWidth = 90) {
  let width = 0;
  const increment = targetWidth / (duration / 100); // Calculate increment per 100ms
  
  return setInterval(function() {
    if (width >= targetWidth) {
      clearInterval(this);
    } else {
      width += increment;
      progressBar.style.width = width + '%';
    }
  }, 100);
}

// Show error message
function showError(message) {
  const resultContainer = document.getElementById('result-container');
  const resultSuccess = document.getElementById('result-success');
  const resultError = document.getElementById('result-error');
  const errorMessage = document.getElementById('error-message');
  
  if (resultContainer && resultSuccess && resultError && errorMessage) {
    resultContainer.style.display = 'block';
    resultSuccess.style.display = 'none';
    resultError.style.display = 'block';
    errorMessage.textContent = message || 'An error occurred. Please try again.';
  }
}

// Show success message
function showSuccess() {
  const resultContainer = document.getElementById('result-container');
  const resultSuccess = document.getElementById('result-success');
  const resultError = document.getElementById('result-error');
  
  if (resultContainer && resultSuccess && resultError) {
    resultContainer.style.display = 'block';
    resultSuccess.style.display = 'block';
    resultError.style.display = 'none';
  }
}
