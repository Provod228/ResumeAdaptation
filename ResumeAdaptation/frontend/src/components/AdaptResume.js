import React, { useState, useEffect } from 'react';
import { getResumes, getVacancies, adaptResume } from '../services/api';

function AdaptResume() {
  const [resumes, setResumes] = useState([]);
  const [vacancies, setVacancies] = useState([]);
  const [selectedResume, setSelectedResume] = useState('');
  const [selectedVacancy, setSelectedVacancy] = useState('');
  const [language, setLanguage] = useState('ru');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [resumesRes, vacanciesRes] = await Promise.all([
        getResumes(),
        getVacancies()
      ]);
      setResumes(resumesRes.data);
      setVacancies(vacanciesRes.data);
    } catch (err) {
      setError('Ошибка загрузки данных');
    }
  };

  const handleAdapt = async () => {
    if (!selectedResume || !selectedVacancy) {
      alert('Выберите резюме и вакансию');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await adaptResume({
        resume_id: parseInt(selectedResume),
        vacancy_id: parseInt(selectedVacancy),
        language: language
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Ошибка адаптации резюме');
    } finally {
      setLoading(false);
    }
  };

  const getScoreClass = (score) => {
    if (score >= 70) return 'score-high';
    if (score >= 40) return 'score-medium';
    return 'score-low';
  };

  return (
    <div>
      <h2 className="mb-4">🚀 Адаптация резюме под вакансию</h2>

      <div className="row">
        <div className="col-md-6">
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Выберите резюме</h5>
              <select
                className="form-select"
                value={selectedResume}
                onChange={(e) => setSelectedResume(e.target.value)}
              >
                <option value="">-- Выберите резюме --</option>
                {resumes.map(resume => (
                  <option key={resume.id} value={resume.id}>
                    {resume.title}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Выберите вакансию</h5>
              <select
                className="form-select"
                value={selectedVacancy}
                onChange={(e) => setSelectedVacancy(e.target.value)}
              >
                <option value="">-- Выберите вакансию --</option>
                {vacancies.map(vacancy => (
                  <option key={vacancy.id} value={vacancy.id}>
                    {vacancy.title} {vacancy.company && `(${vacancy.company})`}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <label className="form-label">Язык адаптации</label>
        <div>
          <div className="form-check form-check-inline">
            <input
              type="radio"
              className="form-check-input"
              name="language"
              value="ru"
              checked={language === 'ru'}
              onChange={(e) => setLanguage(e.target.value)}
            />
            <label className="form-check-label">Русский</label>
          </div>
          <div className="form-check form-check-inline">
            <input
              type="radio"
              className="form-check-input"
              name="language"
              value="en"
              checked={language === 'en'}
              onChange={(e) => setLanguage(e.target.value)}
            />
            <label className="form-check-label">English</label>
          </div>
        </div>
      </div>

      <button
        className="btn btn-primary btn-lg w-100 mb-4"
        onClick={handleAdapt}
        disabled={loading || !selectedResume || !selectedVacancy}
      >
        {loading ? 'Адаптация...' : 'Адаптировать резюме'}
      </button>

      {error && (
        <div className="alert alert-danger">{error}</div>
      )}

      {result && (
        <div>
          <h3 className="mt-4">Результат адаптации</h3>

          <div className="row mb-4">
            <div className="col-md-6">
              <div className="card text-center">
                <div className="card-body">
                  <h5>Совместимость ДО</h5>
                  <h2 className={getScoreClass(result.score_before)}>
                    {result.score_before}%
                  </h2>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="card text-center">
                <div className="card-body">
                  <h5>Совместимость ПОСЛЕ</h5>
                  <h2 className={getScoreClass(result.score_after)}>
                    {result.score_after}%
                  </h2>
                </div>
              </div>
            </div>
          </div>

          <div className="card mb-4">
            <div className="card-header">
              <h5 className="mb-0">Адаптированное резюме</h5>
            </div>
            <div className="card-body">
              <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                {result.adapted_text}
              </pre>
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Лог изменений</h5>
            </div>
            <div className="card-body">
              <p><strong>Добавленные навыки:</strong></p>
              <div>
                {result.changes_log?.added_skills?.map((skill, idx) => (
                  <span key={idx} className="skill-badge bg-success">{skill}</span>
                ))}
                {(!result.changes_log?.added_skills || result.changes_log.added_skills.length === 0) && (
                  <span className="text-muted">Нет добавленных навыков</span>
                )}
              </div>

              <hr />

              <p><strong>Улучшение скора:</strong>
                <span className={result.changes_log?.score_improvement > 0 ? 'score-high' : 'score-low'}>
                  {' '}{result.changes_log?.score_improvement > 0 ? '+' : ''}{result.changes_log?.score_improvement}%
                </span>
              </p>

              <details>
                <summary>Детальная информация</summary>
                <pre className="mt-2">
                  {JSON.stringify(result.changes_log, null, 2)}
                </pre>
              </details>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdaptResume;