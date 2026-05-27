import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import ResumeList from './components/ResumeList';
import VacancyList from './components/VacancyList';
import AdaptResume from './components/AdaptResume';
import CreateResume from './components/CreateResume';
import CreateVacancy from './components/CreateVacancy';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg fixed-top">
          <div className="container">
            <Link className="navbar-brand" to="/">
              🎯 ResumeAI
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/resumes">📄 Резюме</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/vacancies">💼 Вакансии</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link btn-primary" to="/adapt">
                    ✨ Адаптировать
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="container" style={{ marginTop: '80px' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/resumes" element={<ResumeList />} />
            <Route path="/vacancies" element={<VacancyList />} />
            <Route path="/adapt" element={<AdaptResume />} />
            <Route path="/create-resume" element={<CreateResume />} />
            <Route path="/create-vacancy" element={<CreateVacancy />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

function Home() {
  const [stats, setStats] = React.useState({ resumes: 0, vacancies: 0, adaptations: 0 });

  React.useEffect(() => {
    // Здесь можно загрузить реальную статистику с бэкенда
    // Пока используем тестовые данные
    setStats({ resumes: 12, vacancies: 8, adaptations: 45 });
  }, []);

  return (
    <div className="fade-in">
      <div className="hero">
        <h1>Персонализируйте свои резюме с помощью AI</h1>
        <p>Адаптируйте ваше резюме под требования любой вакансии за секунды</p>
      </div>

      <div className="row g-4 mb-5">
        <div className="col-md-4">
          <div className="stats-card">
            <div className="stats-number">{stats.resumes}</div>
            <div className="text-muted mt-2">Резюме создано</div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="stats-card">
            <div className="stats-number">{stats.vacancies}</div>
            <div className="text-muted mt-2">Вакансий добавлено</div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="stats-card">
            <div className="stats-number">{stats.adaptations}</div>
            <div className="text-muted mt-2">Адаптаций выполнено</div>
          </div>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-md-6">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">📄 Управление резюме</h5>
              <p className="card-text text-muted">Создавайте, редактируйте и храните все свои резюме в одном месте</p>
              <Link to="/resumes" className="btn btn-primary mt-3">Перейти к резюме</Link>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">💼 Управление вакансиями</h5>
              <p className="card-text text-muted">Добавляйте вакансии с hh.ru и других сайтов</p>
              <Link to="/vacancies" className="btn btn-primary mt-3">Перейти к вакансиям</Link>
            </div>
          </div>
        </div>
      </div>

      <div className="text-center mt-5">
        <Link to="/adapt" className="btn btn-primary btn-lg px-5 py-3">
          🚀 Начать адаптацию
        </Link>
      </div>
    </div>
  );
}

export default App;