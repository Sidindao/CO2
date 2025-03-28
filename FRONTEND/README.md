#  Comparaison d'émission de  CO₂

## Description  
une application web qui permet de comparer les émissions de CO₂ d’un trajet en fonction des différents modes de transport (voiture, train, avion, etc.). L'objectif est d'aider les utilisateurs à choisir l'option la plus écologique pour leurs déplacements.  


# Partie Frontend de l'application



## Stack Technique  

### Frontend  
- **Framework** : [React](https://react.dev/learn/build-a-react-app-from-scratch#vite) (via Vite)  
- **Navigation** : [React Router](https://reactrouter.com/start/library/installation)  
- **Gestion des requêtes** : [React Query](https://tanstack.com/query/latest/docs/framework/react/installation)  
- **Visualisation des données** : [Recharts](https://recharts.org/en-US/guide)  
- **Styling** : [Tailwind CSS](https://tailwindcss.com/docs/installation/using-vite)  

### Outils de développement  
- **Linting** : ESLint avec le plugin `@tanstack/eslint-plugin-query` pour déboguer React Query.  
- **React Testing Library et vitest** : pour les test unitaires et d'intégration de l'application frontend.
---

## 📦 Installation  

### Prérequis  
- [Node.js](https://nodejs.org/) (version 18 ou supérieure recommandée)  
- [Git](https://git-scm.com/)  

### Étapes d'installation  

1. **Cloner le dépôt**  
   ```sh
   git clone https://forge.univ-lyon1.fr/p2412504/mif10-g13-2024-2025.git
   cd frontend
2. **installer les dépendances**  
   ```sh
   npm install
2. **tester l'application**  
   ```sh
   npm test   
4. **Lancer l'appli**  
   ```sh
   npm run dev