# ReactJS ToDo List

A front‑end only study project implementing a To‑Do List web application using **React JS** and **Styled Components**. Includes login page, task management UI, filtering, and basic authentication flow (no backend or persistent storage).

---

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Important Files](#important-files)
- [Architecture & Execution Flow](#architecture--execution-flow)
- [Setup Instructions](#setup-instructions)
- [Design Choices](#design-choices)
- [Limitations / Future Work](#limitations--future-work)

---

## Overview
This repository contains a simple, fully‑typed To‑Do List application built with React 18, TypeScript, and Styled Components. The app demonstrates:
- User authentication (simulated via `localStorage`)
- Task creation, deletion, and filtering (All / Done / Not done)
- Category‑based task views
- Modals for adding and deleting tasks
- Protected routing based on authentication state
- Modular, reusable UI components

The project is intended as a learning exercise for React context API, routing, and styling with Styled Components.

---

## Tech Stack
| Category        | Technology / Version                                 |
|-----------------|------------------------------------------------------|
| **Language**    | TypeScript                                           |
| **UI Library**  | React 18.2.0 + React DOM                             |
| **Routing**     | react‑router‑dom 6.7.0                               |
| **Styling**     | styled‑components 5.3.6                              |
| **State Mgmt**  | React Context API (multiple focused contexts)        |
| **Build Tool**  | Create React App (react‑scripts 5.0.1)               |
| **Testing**     | @testing-library/react, @testing-library/jest-dom, @testing-library/user-event, web‑vitals |
| **Dev Tools**   | TypeScript, gh‑pages (deployment), @types/styled‑components |
| **Package Manager** | Yarn (as per README)                           |

---

## Project Structure
```
src/
├── Components/          # Reusable UI components (AddTask, TaskCard, SidebarItem, FilterTag, modals, etc.)
│   └── <Component>/     # Each component has index.tsx + styles.ts
├── Pages/               # Page‑level components (Home, Login, Categorie)
│   └── <Page>/          # Each page has index.tsx + styles.ts
├── Contexts/            # Context providers and types (auth, taskList, delete, add, categories)
├── Routes/              # Route protection logic (Route.tsx)
├── Img/                 # Static image assets (icons, logos)
├── index.tsx            # Entry point: renders <App /> inside React StrictMode
├── App.tsx              # Root component: wraps app with ContextProviders, BrowserRouter, Routes, GlobalStyle
├── contextProviders.tsx # Composes all context providers in a specific order
├── global.ts            # Global styled‑components styles
└── ...                  # tsconfig.json, etc.
public/
└── index.html           # Static HTML template
```

---

## Important Files
| File | Purpose |
|------|---------|
| `README.md` | Project overview, features, inspiration, usage instructions |
| `package.json` | Dependencies, scripts, metadata |
| `src/index.tsx` | Boots the React app, creates root, renders `<App />` |
| `src/App.tsx` | Root component: wraps app with `ContextProviders`, `BrowserRouter`, `Routes`, `GlobalStyle`; defines protected routes |
| `src/contextProviders.tsx` | Instantiates and nests context providers (TaskList → Delete → Add → Categories → Auth) |
| `src/Pages/Home/index.tsx` | Main dashboard: sidebar, task filtering, task list rendering, modals, logout handling |
| `src/Pages/Login/index.tsx` | Login page UI (simulated auth) |
| `src/Pages/Categorie/index.tsx` | Category‑filtered task view |
| `src/Routes/Route.tsx` | Implements `ProtectedRoute` component that checks auth status |
| `src/global.ts` | Global styled‑components styles |
| `tsconfig.json` | TypeScript configuration |
| `yarn.lock` | Dependency lockfile |

---

## Architecture & Execution Flow
1. **Bootstrap** – `src/index.tsx` creates a React root and renders `<App />`.
2. **App Wrapper** – `src/App.tsx`:
   - Wraps the entire app with `ContextProviders` (providing all state contexts).
   - Sets up `BrowserRouter` for client‑side routing.
   - Defines routes:
     - `/` → Home page (protected, requires login)
     - `/login` → Login page (protected, requires *not* logged in)
     - `/categorie/:name` → Category page (protected, requires login)
   - Each route uses `ProtectedRoute` from `src/Routes/Route.tsx` to conditionally render based on auth state.
3. **Context Providers** – `src/contextProviders.tsx` instantiates and nests providers in the order: **TaskList → Delete → Add → Categories → Auth**. This makes their values available to any child component via `useContext`.
4. **Home Page (`src/Pages/Home/index.tsx`)**:
   - Consumes task list, delete, add, and auth contexts.
   - Renders a sidebar with navigation items (Tasks, Categories, Settings, Logout).
   - Shows header and filter controls (All / Done / Not done) that update the displayed task list state.
   - Maps over the selected task list array to render `TaskCard` components.
   - Conditionally renders `AddTask` form and modals (`DeleteModal`, `AddModal`) based on context flags.
   - Logout clears `localStorage` and resets user data via the auth context.
5. **Login Page** – Handles simulated authentication; upon successful login, user data is stored in `localStorage` and the auth context is updated.
6. **Category Page** – Displays tasks filtered by the selected category name from the URL parameter.

---

## Setup Instructions
1. **Install Node.js** – Download from https://nodejs.org/en/
2. **Install Yarn globally**  
   ```bash
   sudo npm install -g yarn
   ```
3. **Install Git** – Download from https://git-scm.com/downloads
4. **Clone the repository**  
   ```bash
   git clone https://github.com/MatheusCavini/ReactJS-ToDoList.git
   cd ReactJS-ToDoList
   ```
5. **Install dependencies**  
   ```bash
   yarn install
   ```
6. **Start the development server**  
   ```bash
   yarn start
   ```
   The app will be available at `http://localhost:3000`.

---

## Design Choices
- **Modular Component Architecture** – Each UI component (e.g., `AddTask`, `TaskCard`) resides in its own folder with an `index.tsx` and a separate `styles.ts` using Styled Components, promoting encapsulation and reusability.
- **Context‑Driven State Management** – Instead of a global state library (Redux, MobX), the app uses multiple focused React Contexts (`auth`, `taskList`, `delete`, `add`, `categories`) to avoid prop‑drilling and keep state logic close to where it’s used.
- **Protected Routing Pattern** – A custom `ProtectedRoute` component centralizes authentication guards, making route protection declarative and consistent.
- **Styling with Styled Components** – CSS‑in‑JS approach keeps styles scoped to components, eliminates CSS naming conflicts, and allows dynamic styling based on props/theme.
- **TypeScript Adoption** – Strict typing across components, context values, and props improves developer experience and catches errors early.
- **Separation of Concerns** – Pages handle layout and data fetching (via contexts), components handle presentation and user interactions, contexts manage state, and routes manage navigation.
- **Asset Organization** – Images and icons are stored under `src/Img/` for easy import and consistent usage.

---

## Limitations / Future Work
- **No backend or persistent storage** – Tasks and user data are lost on page refresh.
- **Missing edit task functionality** – Users can only add and delete tasks; editing is not implemented.
- **Category management limited** – Categories can be viewed but not added, removed, or renamed.
- **Simulated authentication** – Auth logic relies on `localStorage` without real API integration; suitable for study only.
- **Potential enhancements**:
  - Add a backend (e.g., Node.js/Express or Firebase) for persistent storage.
  - Implement task editing and category CRUD operations.
  - Replace simulated auth with JWT‑based authentication.
  - Add unit and integration tests for core functionality.
  - Improve accessibility (ARIA labels, keyboard navigation).
  - Introduce a theme switcher (light/dark mode) using Styled Components theming.

--- 

*This document was generated from the repository analysis to provide a clear, concise reference for developers and contributors.*