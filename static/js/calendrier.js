// Variables globales
let currentDate = new Date();
let currentView = 'month';
let events = [
    {
        id: 1,
        title: "Examen de Mathématiques",
        category: "exam",
        startDate: "2024-09-15",
        endDate: "2024-09-15",
        startTime: "09:00",
        endTime: "11:00",
        class: "L2",
        location: "Salle A101",
        description: "Examen final de mathématiques pour la Licence 2",
        allDay: false
    },
    {
        id: 2,
        title: "Réunion pédagogique",
        category: "meeting",
        startDate: "2024-09-20",
        endDate: "2024-09-20",
        startTime: "14:00",
        endTime: "16:00",
        class: "",
        location: "Salle de réunion",
        description: "Réunion des enseignants pour planifier le semestre",
        allDay: false
    },
    {
        id: 3,
        title: "Vacances d'automne",
        category: "holiday",
        startDate: "2024-10-21",
        endDate: "2024-10-27",
        startTime: "",
        endTime: "",
        class: "",
        location: "",
        description: "Vacances scolaires d'automne",
        allDay: true
    },
    {
        id: 4,
        title: "Rendu projet informatique",
        category: "deadline",
        startDate: "2024-09-30",
        endDate: "2024-09-30",
        startTime: "23:59",
        endTime: "23:59",
        class: "L3",
        location: "Plateforme en ligne",
        description: "Date limite de rendu du projet de programmation",
        allDay: false
    }
];

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    renderCalendar();
    updateMonthDisplay();
});

// Rendu du calendrier
function renderCalendar() {
    const grid = document.getElementById('calendarGrid');
    grid.innerHTML = '';

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());

    for (let i = 0; i < 42; i++) {
        const cell = document.createElement('div');
        cell.className = 'calendar-cell';
        
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        
        const isCurrentMonth = date.getMonth() === month;
        const isToday = isSameDate(date, new Date());
        
        if (!isCurrentMonth) {
            cell.classList.add('other-month');
        }
        if (isToday) {
            cell.classList.add('today');
        }
        
        cell.innerHTML = `
            <div class="date-number">${date.getDate()}</div>
            <div class="events-container" id="events-${date.toISOString().split('T')[0]}"></div>
        `;
        
        cell.addEventListener('click', () => selectDate(date));
        grid.appendChild(cell);
    }
    
    renderEvents();
}

// Rendu des événements
function renderEvents() {
    events.forEach(event => {
        const eventElement = createEventElement(event);
        const dateStr = event.startDate;
        const container = document.getElementById(`events-${dateStr}`);
        if (container) {
            container.appendChild(eventElement);
        }
    });
}

// Création d'un élément événement
function createEventElement(event) {
    const eventDiv = document.createElement('div');
    eventDiv.className = `calendar-event ${event.category}`;
    eventDiv.innerHTML = `
        <div class="event-title">${event.title}</div>
        ${event.startTime ? `<div class="event-time">${event.startTime}</div>` : ''}
    `;
    eventDiv.addEventListener('click', (e) => {
        e.stopPropagation();
        showEventDetails(event);
    });
    return eventDiv;
}

// Navigation
function previousMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
    updateMonthDisplay();
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
    updateMonthDisplay();
}

function today() {
    currentDate = new Date();
    renderCalendar();
    updateMonthDisplay();
}

function updateMonthDisplay() {
    const months = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
    ];
    document.getElementById('currentMonth').textContent = 
        `${months[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
}

// Sélection de date
function selectDate(date) {
    // Pré-remplir la date dans le modal d'ajout
    document.getElementById('eventStartDate').value = date.toISOString().split('T')[0];
    document.getElementById('eventEndDate').value = date.toISOString().split('T')[0];
    
    // Ouvrir le modal d'ajout
    const modal = new bootstrap.Modal(document.getElementById('addEventModal'));
    modal.show();
}

// Sauvegarde d'un événement
function saveEvent() {
    const form = document.getElementById('addEventForm');
    const formData = new FormData(form);
    
    const event = {
        id: Date.now(),
        title: formData.get('title'),
        category: formData.get('category'),
        startDate: formData.get('startDate'),
        endDate: formData.get('endDate'),
        startTime: formData.get('startTime'),
        endTime: formData.get('endTime'),
        class: formData.get('class'),
        location: formData.get('location'),
        description: formData.get('description'),
        allDay: formData.get('allDay') === 'on'
    };
    
    events.push(event);
    renderCalendar();
    
    // Fermer le modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('addEventModal'));
    modal.hide();
    
    // Réinitialiser le formulaire
    form.reset();
    
    alert('Événement ajouté avec succès !');
}

// Affichage des détails d'un événement
function showEventDetails(event) {
    const modal = new bootstrap.Modal(document.getElementById('eventDetailsModal'));
    const header = document.getElementById('eventDetailsHeader');
    const body = document.getElementById('eventDetailsBody');
    
    // Couleur du header selon la catégorie
    header.className = `modal-header ${event.category}`;
    
    body.innerHTML = `
        <div class="event-details">
            <div class="row">
                <div class="col-md-6">
                    <h6><i class="bi bi-calendar-event"></i> Titre</h6>
                    <p>${event.title}</p>
                </div>
                <div class="col-md-6">
                    <h6><i class="bi bi-tag"></i> Catégorie</h6>
                    <span class="badge ${event.category}">${getCategoryName(event.category)}</span>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <h6><i class="bi bi-calendar-plus"></i> Date de début</h6>
                    <p>${formatDate(event.startDate)}</p>
                </div>
                <div class="col-md-6">
                    <h6><i class="bi bi-calendar-minus"></i> Date de fin</h6>
                    <p>${formatDate(event.endDate)}</p>
                </div>
            </div>
            
            ${event.startTime ? `
            <div class="row">
                <div class="col-md-6">
                    <h6><i class="bi bi-clock"></i> Heure de début</h6>
                    <p>${event.startTime}</p>
                </div>
                <div class="col-md-6">
                    <h6><i class="bi bi-clock-fill"></i> Heure de fin</h6>
                    <p>${event.endTime}</p>
                </div>
            </div>
            ` : ''}
            
            ${event.class ? `
            <div class="row">
                <div class="col-md-6">
                    <h6><i class="bi bi-people"></i> Classe</h6>
                    <p>${event.class}</p>
                </div>
            </div>
            ` : ''}
            
            ${event.location ? `
            <div class="row">
                <div class="col-md-6">
                    <h6><i class="bi bi-geo-alt"></i> Lieu</h6>
                    <p>${event.location}</p>
                </div>
            </div>
            ` : ''}
            
            ${event.description ? `
            <div class="row">
                <div class="col-12">
                    <h6><i class="bi bi-text-paragraph"></i> Description</h6>
                    <p>${event.description}</p>
                </div>
            </div>
            ` : ''}
        </div>
    `;
    
    // Stocker l'événement pour les actions
    window.currentEvent = event;
    
    modal.show();
}

// Modification d'un événement
function editEvent() {
    const event = window.currentEvent;
    if (!event) return;
    
    // Pré-remplir le formulaire
    document.getElementById('eventTitle').value = event.title;
    document.getElementById('eventCategory').value = event.category;
    document.getElementById('eventStartDate').value = event.startDate;
    document.getElementById('eventEndDate').value = event.endDate;
    document.getElementById('eventStartTime').value = event.startTime;
    document.getElementById('eventEndTime').value = event.endTime;
    document.getElementById('eventClass').value = event.class;
    document.getElementById('eventLocation').value = event.location;
    document.getElementById('eventDescription').value = event.description;
    document.getElementById('eventAllDay').checked = event.allDay;
    
    // Fermer le modal de détails
    const detailsModal = bootstrap.Modal.getInstance(document.getElementById('eventDetailsModal'));
    detailsModal.hide();
    
    // Ouvrir le modal d'édition
    const editModal = new bootstrap.Modal(document.getElementById('addEventModal'));
    editModal.show();
    
    // Changer le titre du modal
    document.getElementById('addEventModalLabel').innerHTML = '<i class="bi bi-pencil"></i> Modifier l\'événement';
    
    // Changer l'action du bouton
    const saveBtn = document.querySelector('#addEventModal .btn-primary');
    saveBtn.onclick = updateEvent;
}

// Mise à jour d'un événement
function updateEvent() {
    const form = document.getElementById('addEventForm');
    const formData = new FormData(form);
    const event = window.currentEvent;
    
    if (!event) return;
    
    // Mettre à jour l'événement
    event.title = formData.get('title');
    event.category = formData.get('category');
    event.startDate = formData.get('startDate');
    event.endDate = formData.get('endDate');
    event.startTime = formData.get('startTime');
    event.endTime = formData.get('endTime');
    event.class = formData.get('class');
    event.location = formData.get('location');
    event.description = formData.get('description');
    event.allDay = formData.get('allDay') === 'on';
    
    // Re-rendre le calendrier
    renderCalendar();
    
    // Fermer le modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('addEventModal'));
    modal.hide();
    
    // Réinitialiser le formulaire et le bouton
    form.reset();
    document.getElementById('addEventModalLabel').innerHTML = '<i class="bi bi-plus-circle"></i> Ajouter un événement';
    const saveBtn = document.querySelector('#addEventModal .btn-primary');
    saveBtn.onclick = saveEvent;
    
    alert('Événement modifié avec succès !');
}

// Suppression d'un événement
function deleteEvent() {
    const event = window.currentEvent;
    if (!event) return;
    
    if (confirm('Êtes-vous sûr de vouloir supprimer cet événement ?')) {
        const index = events.findIndex(e => e.id === event.id);
        if (index > -1) {
            events.splice(index, 1);
            renderCalendar();
            
            // Fermer le modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('eventDetailsModal'));
            modal.hide();
            
            alert('Événement supprimé avec succès !');
        }
    }
}

// Filtrage des événements
function filterEvents() {
    const categoryFilter = document.getElementById('categoryFilter').value;
    const classFilter = document.getElementById('classFilter').value;
    const searchFilter = document.getElementById('searchEvents').value.toLowerCase();
    
    // Masquer tous les événements
    document.querySelectorAll('.calendar-event').forEach(eventEl => {
        eventEl.style.display = 'none';
    });
    
    // Filtrer et afficher
    events.forEach(event => {
        let show = true;
        
        // Filtre par catégorie
        if (categoryFilter && event.category !== categoryFilter) {
            show = false;
        }
        
        // Filtre par classe
        if (classFilter && event.class !== classFilter) {
            show = false;
        }
        
        // Filtre par recherche
        if (searchFilter && !event.title.toLowerCase().includes(searchFilter)) {
            show = false;
        }
        
        // Afficher ou masquer l'événement
        const eventElements = document.querySelectorAll(`[data-event-id="${event.id}"]`);
        eventElements.forEach(el => {
            el.style.display = show ? 'block' : 'none';
        });
    });
}

// Effacer les filtres
function clearFilters() {
    document.getElementById('categoryFilter').value = '';
    document.getElementById('classFilter').value = '';
    document.getElementById('searchEvents').value = '';
    
    // Afficher tous les événements
    document.querySelectorAll('.calendar-event').forEach(eventEl => {
        eventEl.style.display = 'block';
    });
}

// Changement de vue
function setView(view) {
    currentView = view;
    
    // Mettre à jour les boutons
    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Pour l'instant, on garde la vue mois
    // TODO: Implémenter les vues semaine et jour
    alert(`Vue ${view} - Fonctionnalité à implémenter`);
}

// Fonctions utilitaires
function isSameDate(date1, date2) {
    return date1.getDate() === date2.getDate() &&
           date1.getMonth() === date2.getMonth() &&
           date1.getFullYear() === date2.getFullYear();
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return date.toLocaleDateString('fr-FR', options);
}

function getCategoryName(category) {
    const categories = {
        'exam': 'Examen',
        'course': 'Cours',
        'meeting': 'Réunion',
        'deadline': 'Échéance',
        'holiday': 'Vacances'
    };
    return categories[category] || category;
}

// Événements de filtrage
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('categoryFilter').addEventListener('change', filterEvents);
    document.getElementById('classFilter').addEventListener('change', filterEvents);
    document.getElementById('searchEvents').addEventListener('input', filterEvents);
});