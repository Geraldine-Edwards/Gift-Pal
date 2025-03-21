function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    let calendar;
    const calendarEl = document.getElementById('calendar');
    const eventModal = new bootstrap.Modal(document.getElementById('eventModal'));
    const eventForm = document.getElementById('eventForm');
    const eventTitle = document.getElementById('eventTitle');
    const eventStart = document.getElementById('eventStart');
    const eventEnd = document.getElementById('eventEnd');
    const eventAllDay = document.getElementById('eventAllDay');
    const eventDescription = document.getElementById('eventDescription');
    const eventColor = document.getElementById('eventColor');
    const eventId = document.getElementById('eventId');
    const saveEventButton = document.getElementById('saveEvent');
    const deleteEventButton = document.getElementById('deleteEvent');

    // Function to calculate contrasting text color
    function getContrastColor(hexColor) {
        const r = parseInt(hexColor.slice(1, 3), 16);
        const g = parseInt(hexColor.slice(3, 5), 16);
        const b = parseInt(hexColor.slice(5, 7), 16);
        const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        return luminance > 0.5 ? '#000000' : '#ffffff';
    }

    // Initialize FullCalendar
    function initializeCalendar() {
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            editable: true,
            selectable: true,
            eventOverlap: true, // Allow events to overlap
            slotEventOverlap: true, // Allow events to overlap in time slots
            eventTimeFormat: {
                hour: 'numeric',
                minute: '2-digit',
                hour12: true,
                meridiem: 'short'
            },
            events: fetchEvents,  // Fetch events from the server
            dateClick: info => openModal(null, info.dateStr), // Open modal for new event
            eventClick: info => openModal(info.event), // Open modal for editing event
            eventDidMount: function (info) {
                const event = info.event;
                const username = event.extendedProps.username;
                const profileImage = event.extendedProps.profile_image;
                const eventColor = event.backgroundColor || '#e83e8c';
                const textColor = getContrastColor(eventColor);
            
                // Set the event's background color
                info.el.style.backgroundColor = eventColor;
            
                // Add profile image and start time
                const eventContent = info.el.querySelector('.fc-event-main');
                if (eventContent) {
                    let content = '';
            
                    // Month View: Profile image and start time
                    if (info.view.type === 'dayGridMonth') {
                        const startTime = event.start ? event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
                        content = `
                            <div class="d-flex align-items-center">
                                <img src="${profileImage}" class="rounded-circle me-2" width="20" height="20" alt="${username}">
                                <span class="small" style="color: ${textColor};">${startTime}</span>
                            </div>
                        `;
                    }
                    // Week View: Profile image and start time
                    else if (info.view.type === 'timeGridWeek') {
                        const startTime = event.start ? event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
                        content = `
                            <div class="d-flex align-items-center">
                                <img src="${profileImage}" class="rounded-circle me-2" width="20" height="20" alt="${username}">
                                <span class="small" style="color: ${textColor};">${startTime}</span>
                            </div>
                        `;
                    }
                    // Day View: Full event details
                    else if (info.view.type === 'timeGridDay') {
                        const startTime = event.start ? event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
                        const endTime = event.end ? event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
                        content = `
                            <div class="d-flex align-items-center">
                                <img src="${profileImage}" class="rounded-circle me-2" width="20" height="20" alt="${username}">
                                <div>
                                    <span class="small" style="color: ${textColor}; font-weight: bold;">${event.title}</span><br>
                                    <span class="small" style="color: ${textColor};">${startTime} - ${endTime}</span><br>
                                    <span class="small" style="color: ${textColor};">${event.extendedProps.description || ''}</span>
                                </div>
                            </div>
                        `;
                    }
            
                    eventContent.innerHTML = content;
                }
            
                // Prepare tooltip content (only for month and week views)
                if (info.view.type === 'dayGridMonth' || info.view.type === 'timeGridWeek') {
                    let tooltipContent = `<strong>${event.title}</strong><br>`;
            
                    if (event.allDay) {
                        tooltipContent += 'All Day<br>';
                    } else {
                        const startTime = event.start ? event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
                        const endTime = event.end ? event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
                        tooltipContent += `${startTime} - ${endTime}<br>`;
                    }
            
                    if (event.extendedProps.description) {
                        tooltipContent += `${event.extendedProps.description}<br>`;
                    }
            
                    // Initialize Tippy.js for tooltips
                    if (window.tippy) {
                        tippy(info.el, {
                            content: tooltipContent,
                            allowHTML: true,
                            placement: 'top',
                            theme: 'light',
                            arrow: true,
                        });
                    }
                }
            }
        });

        calendar.render();
    }

    // Fetch events from the server
    function fetchEvents(fetchInfo, successCallback, failureCallback) {
        fetch(getEventsUrl)  // Use the DRF endpoint
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch events');
                }
                return response.json();
            })
            .then(data => {
                const events = data.map(event => ({
                    id: event.id,
                    title: event.title,
                    start: event.start,
                    end: event.end,
                    allDay: event.all_day,
                    color: event.color,
                    description: event.description,
                    username: event.username,  // Include friend's username
                    profile_image: event.profile_image,  // Include friend's profile image
                }));
                successCallback(events);
            })
            .catch(error => {
                console.error('Error fetching events:', error);
                failureCallback(error);
            });
    }

    function fetchEvents(fetchInfo, successCallback, failureCallback) {
        fetch(getEventsUrl)  // Use the DRF endpoint
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch events');
                }
                return response.json();
            })
            .then(data => {
                const events = data.map(event => ({
                    id: event.id,
                    title: event.title,
                    start: event.start,
                    end: event.end,
                    allDay: event.all_day,
                    color: event.color,
                    description: event.description,
                    username: event.username,  // Include friend's username
                    profile_image: event.profile_image,  // Include friend's profile image
                }));
                successCallback(events);
            })
            .catch(error => {
                console.error('Error fetching events:', error);
                failureCallback(error);
            });
    }
    // Open the modal for adding or editing an event
    function openModal(event, dateStr) {
        if (event) {
            // Editing an existing event
            eventId.value = event.id;
            eventTitle.value = event.title;
            eventStart.value = event.start ? event.start.toISOString().slice(0, 16) : '';
            eventEnd.value = event.end ? event.end.toISOString().slice(0, 16) : '';
            eventAllDay.checked = event.allDay || false;
            eventDescription.value = event.extendedProps.description || '';
            eventColor.value = event.backgroundColor || '#3788d8';
            deleteEventButton.style.display = 'inline-block';
        } else {
            // Adding a new event
            eventId.value = '';
            eventTitle.value = '';
            eventStart.value = dateStr ? new Date(dateStr).toISOString().slice(0, 16) : '';
            eventEnd.value = '';
            eventAllDay.checked = false;
            eventDescription.value = '';
            eventColor.value = '#3788d8';
            deleteEventButton.style.display = 'none';
        }
        eventModal.show();
    }

    // Save or update an event
    saveEventButton.addEventListener('click', function () {
        const eventData = {
            title: eventTitle.value,
            start: eventStart.value,
            end: eventEnd.value || null,
            all_day: eventAllDay.checked,
            color: eventColor.value,
            description: eventDescription.value,
        };

        const url = eventId.value ? eventDetailUrl.replace('0', eventId.value) : getEventsUrl;
        const method = eventId.value ? 'PUT' : 'POST';

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(eventData),
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        throw new Error(err.detail || 'Failed to save event');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Event saved:', data);
                eventModal.hide();
                calendar.refetchEvents();
            })
            .catch(error => {
                console.error('Error saving event:', error);
                alert('Failed to save event. Please try again.');
            });
    });

    // Delete an event
    deleteEventButton.addEventListener('click', function () {
        if (!confirm('Are you sure you want to delete this event?')) return;

        fetch(eventDetailUrl.replace('0', eventId.value), {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete event');
                }
                eventModal.hide();
                calendar.refetchEvents();
            })
            .catch(error => {
                console.error('Error deleting event:', error);
                alert('Failed to delete event. Please try again.');
            });
    });

    // Initialize the calendar when the page loads
    initializeCalendar();
});