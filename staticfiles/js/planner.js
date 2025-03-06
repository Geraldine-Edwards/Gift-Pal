
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
    const eventDescription = document.getElementById('eventDescription');
    const eventColor = document.getElementById('eventColor');
    const eventId = document.getElementById('eventId');
    const saveEventButton = document.getElementById('saveEvent');
    const deleteEventButton = document.getElementById('deleteEvent');

    
    // Enhanced calendar initialization with error handling
        function initializeCalendar() {
        fetch(getEventsUrl)
            .then(response => {
                if (!response.ok) {
                    console.error('Server error:', response.status);
                    showCalendarError();
                    return Promise.reject('Failed to load events');
                }
                return response.json();
            })
            .then(data => {
                console.log('Received events data:', data);  // Debugging log
                
                // Handle both {events: [...]} and direct array responses
                const eventsArray = data.events || data;
                
                if (!Array.isArray(eventsArray)) {
                    console.error('Invalid events data format:', data);
                    showCalendarError();
                    return;
                }

                initFullCalendar(eventsArray);
            })
            .catch(error => {
                console.error('Error initializing calendar:', error);
                showCalendarError();
            });
    }

    function initFullCalendar(events) {
        if (calendar) calendar.destroy();
        
        calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            editable: true,
            selectable: true,
            eventTimeFormat: {
                hour: 'numeric',
                minute: '2-digit',
                hour12: true,
                meridiem: 'short'
            },
            eventDidMount: function (info) {
                // Set background and border colors
                info.el.style.backgroundColor = info.event.backgroundColor;
                info.el.style.borderColor = info.event.backgroundColor;
            
                // Check if the view is 'dayGridMonth'
                if (info.view.type === 'dayGridMonth') {
                    // Create a dot element
                    const dot = document.createElement('div');
                    dot.className = 'fc-event-dot';
                    dot.style.backgroundColor = info.event.backgroundColor;
            
                    // Safely prepend the dot to the event's content
                    const eventContent = info.el.querySelector('.fc-event-main');
                    if (eventContent) {
                        eventContent.prepend(dot);
                    } else {
                        // Fallback: Append the dot directly to the event element
                        info.el.prepend(dot);
                    }
                }
            },
            events: events.map(event => ({
                id: event.id,
                title: event.title,
                start: event.start,
                end: event.end,
                backgroundColor: event.color || '#686dc3',
                extendedProps: {
                    description: event.description || '',
                    is_friend: event.is_friend,
                    profile_image: event.profile_image,
                    user: event.user
                }
            })),
            dateClick: info => openModal(null, info.dateStr),
            eventClick: info => openModal(info.event)
        });
        
        calendar.render();
    }

    function showCalendarError() {
        calendarEl.innerHTML = '<div class="alert alert-danger mt-3">Could not load calendar events. Please refresh the page.</div>';
    }

    // Improved form submission handling
        saveEventButton.addEventListener('click', function () {

        // Clear previous validation states
        eventTitle.classList.remove('is-invalid');
        eventStart.classList.remove('is-invalid');

        // Validate required fields
        if (!eventTitle.value || !eventStart.value) {
            if (!eventTitle.value) eventTitle.classList.add('is-invalid');
            if (!eventStart.value) eventStart.classList.add('is-invalid');
            alert('Please fill out all required fields (Title and Start Date).');
            return;
        }

        // Convert local datetime to UTC ISO strings
        const startDate = eventStart.value ? new Date(eventStart.value) : null;
        const endDate = eventEnd.value ? new Date(eventEnd.value) : null;

        const eventData = {
            id: eventId.value,
            title: eventTitle.value,
            start: eventStart.value,
            end: eventEnd.value || null,
            description: eventDescription.value.trim(),
            color: eventColor.value
        };

        const url = eventData.id 
            ? editEventUrl.replace('0', eventData.id)
            : addEventUrl;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(eventData)
        })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Unknown error');
            }
            return data;
        })
        .then(data => {
            if (data.status === 'success') {
                console.log("Event saved successfully!");
                eventModal.hide();
                calendar.refetchEvents();
            } else {
                throw new Error(data.message || 'Unknown error occurred');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Failed to save event: ${error.message}`);
            // Highlight problematic fields
            if (error.message.includes('start')) eventStart.classList.add('is-invalid');
            if (error.message.includes('end')) eventEnd.classList.add('is-invalid');
        });
    });

    
    // Enhanced delete handling
        deleteEventButton.addEventListener('click', function () {
        if (!confirm('Are you sure you want to delete this event?')) return;

        const url = deleteEventUrl.replace('0', eventId.value);

        fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Delete failed');
            }
            return data;
        })
        .then(data => {
            if (data.status === 'success') {
                console.log("Event deleted successfully");
                eventModal.hide();
                calendar.refetchEvents();
            } else {
                throw new Error(data.message || 'Delete failed');
            }
        })
        .catch(error => {
            console.error('Delete error:', error);
            alert(`Delete failed: ${error.message}`);
        });
    });

    function openModal(event, dateStr) {
        if (event) {
            // Editing an existing event
            eventId.value = event.id;
            eventTitle.value = event.title;
            
            // Convert UTC dates to local timezone for the datetime inputs
            if (event.start) {
                const startDate = new Date(event.start);
                eventStart.value = new Date(startDate.getTime() - (startDate.getTimezoneOffset() * 60000))
                    .toISOString()
                    .slice(0, 16);  // Format: YYYY-MM-DDTHH:mm
            } else {
                eventStart.value = '';
            }
    
            if (event.end) {
                const endDate = new Date(event.end);
                eventEnd.value = new Date(endDate.getTime() - (endDate.getTimezoneOffset() * 60000))
                    .toISOString()
                    .slice(0, 16);  // Format: YYYY-MM-DDTHH:mm
            } else {
                eventEnd.value = '';
            }
    
            // Populate other fields
            eventDescription.value = event.extendedProps.description || '';
            eventColor.value = event.backgroundColor || '#686dc3';
            deleteEventButton.style.display = 'inline-block';
        } else {
            // Adding a new event
            eventId.value = '';
            eventTitle.value = '';
            eventStart.value = dateStr ? 
                new Date(new Date(dateStr).getTime() - (new Date(dateStr).getTimezoneOffset() * 60000))
                    .toISOString()
                    .slice(0, 16) : '';  // Format: YYYY-MM-DDTHH:mm
            eventEnd.value = '';
            eventDescription.value = '';
            eventColor.value = '#686dc3';  // Default color
            deleteEventButton.style.display = 'none';
        }
    }
    // Initialize calendar when page loads
    initializeCalendar();
    
});

