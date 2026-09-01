/* AtmosphereX Weather Dashboard Frontend Application Logic */

document.addEventListener('DOMContentLoaded', () => {
  let currentCity = 'London';
  let currentUnit = 'C'; // 'C' or 'F'
  let weatherCache = null;

  // UI Elements
  const searchForm = document.getElementById('search-form');
  const cityInput = document.getElementById('city-input');
  const cityChips = document.querySelectorAll('.city-chip');
  const unitCBtn = document.getElementById('unit-c');
  const unitFBtn = document.getElementById('unit-f');
  
  const locationName = document.getElementById('location-name');
  const conditionText = document.getElementById('condition-text');
  const weatherIcon = document.getElementById('weather-icon');
  const tempVal = document.getElementById('temp-val');
  const tempUnit = document.getElementById('temp-unit');
  const latVal = document.getElementById('lat-val');
  const lonVal = document.getElementById('lon-val');
  
  const humidityVal = document.getElementById('humidity-val');
  const windVal = document.getElementById('wind-val');
  const pressureVal = document.getElementById('pressure-val');
  const uvVal = document.getElementById('uv-val');
  const forecastContainer = document.getElementById('forecast-container');
  
  const latencyVal = document.getElementById('latency-val');
  const clockDisplay = document.getElementById('clock-display');

  // Realtime Live Clock
  function updateClock() {
    const now = new Date();
    clockDisplay.textContent = now.toLocaleTimeString();
  }
  setInterval(updateClock, 1000);
  updateClock();

  // Fetch Weather Data from REST API
  async function fetchWeather(city) {
    const startTime = performance.now();
    try {
      const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
      const duration = Math.round(performance.now() - startTime);
      latencyVal.textContent = `${duration}ms`;

      if (!response.ok) {
        throw new Error('Failed to load weather data');
      }

      const data = await response.json();
      weatherCache = data;
      renderWeather(data);
    } catch (err) {
      console.error('Weather API Error:', err);
      // Fallback display if network offline
      locationName.textContent = `${city} (Offline Mode)`;
    }
  }

  // Render Weather Telemetry
  function renderWeather(data) {
    locationName.textContent = `${data.city}, ${data.country}`;
    conditionText.textContent = data.condition;
    
    // Set Temperature based on active unit
    const isC = currentUnit === 'C';
    tempVal.textContent = isC ? Math.round(data.temperature.celsius) : Math.round(data.temperature.fahrenheit);
    tempUnit.textContent = currentUnit;

    latVal.textContent = data.coordinates.lat;
    lonVal.textContent = data.coordinates.lon;

    humidityVal.textContent = `${data.humidity}%`;
    windVal.textContent = `${data.wind_speed_kmh} km/h`;
    pressureVal.textContent = `${data.pressure_hpa} hPa`;
    uvVal.textContent = `${data.uv_index} (Moderate)`;

    // Update Weather Icon
    updateIcon(weatherIcon, data.condition);

    // Render Forecast
    renderForecast(data.forecast);
  }

  // Render 5-Day Forecast Cards
  function renderForecast(forecast) {
    forecastContainer.innerHTML = '';
    const isC = currentUnit === 'C';

    forecast.forEach(item => {
      const card = document.createElement('div');
      card.className = 'forecast-card';
      const temp = isC ? Math.round(item.temp_c) : Math.round(item.temp_f);

      card.innerHTML = `
        <div class="forecast-day">${item.day}</div>
        <i class="forecast-icon ${getIconClass(item.condition)}"></i>
        <div class="forecast-temp">${temp}°${currentUnit}</div>
        <div class="forecast-cond">${item.condition}</div>
      `;
      forecastContainer.appendChild(card);
    });
  }

  function getIconClass(condition) {
    switch (condition.toLowerCase()) {
      case 'clear':
      case 'sunny':
        return 'fa-solid fa-sun';
      case 'rain':
        return 'fa-solid fa-cloud-showers-heavy';
      case 'clouds':
      case 'partly cloudy':
        return 'fa-solid fa-cloud-sun';
      default:
        return 'fa-solid fa-cloud';
    }
  }

  function updateIcon(element, condition) {
    element.className = getIconClass(condition);
  }

  // Event Listeners
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const city = cityInput.value.trim();
    if (city) {
      currentCity = city;
      fetchWeather(currentCity);
    }
  });

  cityChips.forEach(chip => {
    chip.addEventListener('click', () => {
      currentCity = chip.getAttribute('data-city');
      cityInput.value = currentCity;
      fetchWeather(currentCity);
    });
  });

  unitCBtn.addEventListener('click', () => {
    if (currentUnit !== 'C') {
      currentUnit = 'C';
      unitCBtn.classList.add('active');
      unitFBtn.classList.remove('active');
      if (weatherCache) renderWeather(weatherCache);
    }
  });

  unitFBtn.addEventListener('click', () => {
    if (currentUnit !== 'F') {
      currentUnit = 'F';
      unitFBtn.classList.add('active');
      unitCBtn.classList.remove('active');
      if (weatherCache) renderWeather(weatherCache);
    }
  });

  // Initial Load
  fetchWeather(currentCity);
});
