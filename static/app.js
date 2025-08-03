document.addEventListener("DOMContentLoaded", () => {
  const monthYearEl = document.getElementById('monthYear');
  const calendarDatesEl = document.getElementById('calendarDates');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');

  // Use injected mapping; fallback to empty object
  const eventsData = (window.EVENT_URLS && typeof window.EVENT_URLS === 'object') ? window.EVENT_URLS : {};

  let currentDate = new Date();

  function renderCalendar(date) {
    const year = date.getFullYear();
    const month = date.getMonth();

    // Header
    const monthNames = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];
    if (monthYearEl) {
      monthYearEl.textContent = `${monthNames[month]} ${year}`;
    }

    if (!calendarDatesEl) return;
    calendarDatesEl.innerHTML = "";

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Empty slots
    for (let i = 0; i < firstDay; i++) {
      const emptyDiv = document.createElement("div");
      emptyDiv.classList.add("inactive");
      calendarDatesEl.appendChild(emptyDiv);
    }

    // Days
    for (let day = 1; day <= daysInMonth; day++) {
      const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const dayDiv = document.createElement("div");
      dayDiv.textContent = day;

      if (eventsData[dateKey]) {
        dayDiv.classList.add("active");
        dayDiv.style.cursor = "pointer";
        dayDiv.addEventListener("click", () => {
          window.location.href = eventsData[dateKey];
        });
      }

      calendarDatesEl.appendChild(dayDiv);
    }
  }

  // Navigation buttons
  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      currentDate.setMonth(currentDate.getMonth() - 1);
      renderCalendar(currentDate);
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      currentDate.setMonth(currentDate.getMonth() + 1);
      renderCalendar(currentDate);
    });
  }

  // Initial render
  renderCalendar(currentDate);
});