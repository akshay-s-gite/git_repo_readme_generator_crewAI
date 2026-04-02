# The Weather Forecasting

A React-based web application that allows users to search for cities and view current weather conditions plus a 5‑day/3‑hour forecast. Data is fetched from the OpenWeatherMap API (current weather and forecast) and a geo‑cities API (for search suggestions). The live demo is hosted at https://the-weather-forecasting.netlify.app.

---

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Important Files](#important-files)
- [Setup Instructions](#setup-instructions)
- [How It Works](#how-it-works)
- [Design Choices](#design-choices)
- [Future Enhancements](#future-enhancements)

---

## Overview
The Weather Forecasting app provides a clean, responsive interface for users to:
- Search for cities using an asynchronous paginated search box.
- View current weather conditions (temperature, description, humidity, wind, etc.).
- See a 5‑day forecast with 3‑hour intervals, presented as hourly forecasts for today and daily summaries for the upcoming days.
- The app leverages Material‑UI for a polished UI and relies on React hooks for state management.

---

## Tech Stack
| Category        | Technology/Library                                                                 |
|-----------------|-----------------------------------------------------------------------------------|
| **Framework**   | React 18.2.0 (bootstrapped with Create‑React‑App)                                 |
| **UI Library**  | Material‑UI (MUI) v5 (`@mui/material`, `@mui/icons-material`, `@emotion/react`, `@emotion/styled`) |
| **HTTP**        | Native `fetch` (no external HTTP client)                                          |
| **State Mgmt**  | React `useState` hooks (no external state library)                                |
| **Build Tool**  | React‑Scripts (webpack/Babel)                                                     |
| **Testing**     | Jest + React Testing Library (configured via CRA)                                 |
| **Styling**     | MUI’s `sx` prop (CSS‑in‑JS) and baseline `index.css`                              |
| **APIs**        | OpenWeatherMap (weather data), RapidAPI WFT GeoDB (city search)                   |
| **Deployment**  | Netlify                                                                           |

---

## Project Structure
```
src/
├── api/                  # Service layer for API calls
│   └── OpenWeatherService.js
├── components/           # UI components
│   ├── Reusable/         # Shared UI pieces (Layout, LoadingBox, ErrorBox, SectionHeader, UTCDatetime)
│   ├── Search/           # Search input component (uses react-select-async-paginate)
│   ├── TodayWeather/     # Current weather display
│   └── WeeklyForecast/   # Multi‑day forecast display
├── assets/               # Static images (icons, logo, splash)
├── utilities/            # Helper functions
│   ├── DataUtils.js      # Data transformation (getTodayForecastWeather, getWeekForecastWeather)
│   ├── DatetimeUtils.js  # Date formatting (transformDateFormat)
│   └── DateConstants.js  # Constants (ALL_DESCRIPTIONS)
├── index.css             # Baseline CSS
└── index.js              # React entry point
public/
├── index.html            # HTML entry point
├── favicon.ico
└── manifest.json
```

---

## Important Files
- **`README.md`** – Project overview, live demo link, setup instructions, tech stack, TODO list.
- **`package.json`** – Dependencies and npm scripts (`start`, `build`, `test`, `eject`).
- **`src/index.js`** – React entry point; renders `<App />` into the root div.
- **`src/App.js`** – Main application orchestrator: manages state, handles search, conditionally renders loading/error/data views.
- **`src/api/OpenWeatherService.js`** – Encapsulates calls to OpenWeatherMap (current weather & forecast) and RapidAPI GeoDB (city search).
- **`src/utilities/DataUtils.js`** – Contains `getTodayForecastWeather` and `getWeekForecastWeather` used to shape API responses for UI.
- **`src/utilities/DatetimeUtils.js`** – Provides `transformDateFormat` for displaying current date.
- **`src/utilities/DateConstants.js`** – Holds `ALL_DESCRIPTIONS` array used in forecast grouping.
- **`src/components/Search/Search.js`** – Implements the search box (uses `react-select-async-paginate` with `fetchCities` from API service).
- **`src/components/TodayWeather/TodayWeather.js`** & **`src/components/WeeklyForecast/WeeklyForecast.js`** – Presentational components receiving processed data props.

---

## Setup Instructions
1. **Prerequisites**: Ensure Node.js and npm are installed.
2. **Clone the repository**:
   ```bash
   git clone https://github.com/Amin-Awinti/the-weather-forecasting.git
   ```
3. **Install dependencies**:
   ```bash
   npm install
   ```
4. **Obtain an API key** from [OpenWeatherMap](https://openweathermap.org/api).
5. **Configure the API key**:
   - Open `src/api/OpenWeatherService.js`.
   - Replace the placeholder `WEATHER_API_KEY` with your OpenWeatherMap API key.
   - (The RapidAPI key for city search is already present in the file.)
6. **Start the development server**:
   ```bash
   npm start
   ```
   The app will be available at `http://localhost:3000`.
7. **Build for production**:
   ```bash
   npm run build
   ```
   The build output will be in the `build/` folder, ready for deployment.

---

## How It Works
### Execution Flow
1. **App Load**  
   - `src/index.js` renders the `<App />` component into the DOM root.
2. **Initial State**  
   - `App.js` sets the initial UI to show a loading splash icon and a prompt to search for a city.
3. **User Interaction**  
   - The user types in the Search component (`src/components/Search/Search.js`).
   - The component calls `fetchCities` (from `OpenWeatherService.js`) via RapidAPI to get city suggestions.
   - Upon selecting a city, the `onSearchChange` prop (defined in `App.js`) is triggered.
4. **Search Handler (`searchChangeHandler` in `App.js`)**  
   - Sets loading state to true.
   - Splits the selected value into latitude and longitude.
   - Calls `fetchWeatherData(lat, lon)` (from `OpenWeatherService.js`), which performs two parallel fetches to OpenWeatherMap:
     - `/weather` endpoint for current conditions.
     - `/forecast` endpoint for the 5‑day/3‑hour forecast list.
   - On success:
     - Calls `getTodayForecastWeather` (from `DataUtils.js`) to extract today’s hourly forecasts.
     - Calls `getWeekForecastWeather` (from `DataUtils.js`) to build daily forecasts for the next 5‑6 days.
     - Updates component state with `todayWeather`, `todayForecast`, and `weekForecast`.
   - On error: sets error state → renders an `ErrorBox`.
   - Finally, clears loading state.
5. **Rendering**  
   - If data is present: renders `<TodayWeather>` and `<WeeklyForecast>` components in a responsive grid.
   - If loading: shows a `LoadingBox`.
   - If error: shows an `ErrorBox`.
6. **Child Components**  
   - **`TodayWeather`**: Displays city name, current weather (temp, description, icon), and a list of hourly forecasts (time, temp, icon).
   - **`WeeklyForecast`**: Displays a list of days, each with date, min/max temperature, condition icon, and textual description.
7. **UI Enhancements**  
   - `UTCDatetime` shows the current UTC time in the app header.
   - A GitHub icon links to the author’s profile.
   - Responsive layout achieved via MUI `Grid` and `Box` components with breakpoint‑aware `sx` props.

---

## Design Choices
- **Separation of Concerns**: API logic is isolated in `src/api/`; data transformation utilities reside in `src/utilities/`; UI components are purely presentational, receiving processed data as props.
- **Reusable UI Components**: Loading, error, layout, section header, and datetime utilities are abstracted for reuse across views.
- **Optimistic Data Fetching**: Uses `Promise.all` to fetch current weather and forecast in parallel, reducing latency.
- **Material‑UI Styling**: Leverages MUI’s `sx` prop for concise, theme‑aware styling without external CSS files (aside from baseline `index.css`).
- **Async‑Paginate Search**: Employs `react-select-async-paginate` for efficient, debounced city search with pagination via the GeoDB API.
- **Environment‑Agnostic API Keys**: The OpenWeatherMap key is expected to be replaced by the developer; the RapidAPI key is hard‑coded (could be improved by using environment variables).
- **Extensibility**: The README includes a TODO list indicating planned enhancements (TypeScript, styled‑components, unit tests, geolocation, theme toggle, unit conversion).
- **Create‑React‑App Scaffold**: Benefits from standard React tooling (ESLint, Jest, Babel, webpack) while allowing `eject` if needed.

---

## Future Enhancements
As noted in the project’s TODO list, potential future improvements include:
- Migrating to TypeScript for improved type safety.
- Exploring alternative styling solutions (e.g., styled‑components).
- Adding comprehensive unit tests with Jest and React Testing Library.
- Implementing geolocation to show weather for the user’s current location.
- Adding a theme toggle (light/dark mode).
- Providing unit conversion options (metric/imperial).

---

*Happy coding!* 🌤️