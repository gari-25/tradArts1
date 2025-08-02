const monthYearEl = document.getElementById('monthYear');
const calendarDatesEl = document.getElementById('calendarDates');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');

let currentDate = new Date();

// Define active event days (can add links here too)
const eventsData = {
  "2025-06-02": "past1.html?date=2025-07-07",
  "2025-06-15": "past2.html?date=2025-07-07",
  "2025-06-23": "past4.html?date=2025-07-07",
  "2025-06-07": "past4.html?date=2025-07-07",
  "2025-09-08": "string.html?date=2025-07-07",
  "2025-07-07": "madhubani.html?date=2025-07-07",
  "2025-07-18": "vastra.html?date=2025-07-07",
  "2025-07-24": "clay.html?date=2025-07-07",
  "2025-08-06": "madhubani.html?date=2025-07-07",
  "2025-08-15": "vastra.html?date=2025-07-18",
  "2025-08-24": "clay.html?date=2025-07-24",
};

function renderCalendar(date) {
  const year = date.getFullYear();
  const month = date.getMonth();

  // Set month-year header
  const monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"];
  monthYearEl.textContent = `${monthNames[month]} ${year}`;

  // First day of the month
  const firstDay = new Date(year, month, 1).getDay();

  // Number of days in month
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  calendarDatesEl.innerHTML = "";

  // Fill empty blocks before start
  for (let i = 0; i < firstDay; i++) {
    const emptyDiv = document.createElement("div");
    emptyDiv.classList.add("inactive");
    calendarDatesEl.appendChild(emptyDiv);
  }

  // Fill days
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

// Navigation
prevBtn.addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar(currentDate);
});

nextBtn.addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar(currentDate);
});

renderCalendar(currentDate);




