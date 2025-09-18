// Fonction de validation avant soumission
function validateImport() {
    const fileInput = document.getElementById('fileInput');
    const importType = document.getElementById('importType');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!fileInput.files.length) {
        alert('Veuillez sélectionner un fichier');
        return false;
    }
    
    if (!importType.value) {
        alert('Veuillez sélectionner un type d\'importation');
        return false;
    }
    
    // Désactiver le bouton pendant l'upload
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Import en cours...';
    
    return true;
}

// Gestion du drag and drop
document.addEventListener('DOMContentLoaded', function() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const actionButtons = document.getElementById('actionButtons');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const fileType = document.getElementById('fileType');

    // Gestion du drag and drop
    ['dragover', 'dragenter'].forEach(function(event) {
        uploadZone.addEventListener(event, function(e) {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });
    });

    ['dragleave', 'dragend', 'drop'].forEach(function(event) {
        uploadZone.addEventListener(event, function(e) {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
        });
    });

    uploadZone.addEventListener('drop', function(e) {
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            updateFileInfo();
        }
    });

    // Gestion du click
    fileInput.addEventListener('change', updateFileInfo);

    function updateFileInfo() {
        if (fileInput.files.length) {
            const file = fileInput.files[0];
            fileName.textContent = file.name;
            fileSize.textContent = 'Taille: ' + formatFileSize(file.size);
            fileType.textContent = 'Type: ' + file.name.split('.').pop().toUpperCase();
            
            fileInfo.style.display = 'block';
            actionButtons.style.display = 'block';
        }
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
});

function removeFile() {
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('actionButtons').style.display = 'none';
}

// Afficher automatiquement le modal s'il y a des messages flash
if (document.getElementById('resultModal')) {
    document.addEventListener('DOMContentLoaded', function() {
        var resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
        resultModal.show();
    });
}