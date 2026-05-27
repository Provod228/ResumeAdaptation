import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getVacancies, deleteVacancy } from '../services/api';

function VacancyList() {
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadVacancies();
  }, []);

  const loadVacancies = async () => {
    try {
      const response = await getVacancies();
      setVacancies(response.data);
      setLoading(false);
    } catch (err) {
      setError('Ошибка загрузки вакансий');
      setLoading(false);
    }
  };

  const handleDelete = async (id, title) => {
    if (window.confirm(`Удалить вакансию "${title}"?`)) {
      try {
        await deleteVacancy(id);
        loadVacancies();
      } catch (err) {
        alert('Ошибка удаления');
      }
    }
  };

  if (loading) return <div className="text-center py-5">Загрузка...</div>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="fade-in">
      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-3">
        <div>
          <h2 className="mb-1">💼 Вакансии</h2>
          <p className="text-muted">Всего: {vacancies.length} вакансий</p>
        </div>
        <Link to="/create-vacancy" className="btn btn-success">
          + Добавить вакансию
        </Link>
      </div>

      {vacancies.length === 0 ? (
        <div className="alert alert-info text-center py-5">
          <h4 className="mb-3">Пока нет вакансий</h4>
          <p>Добавьте первую вакансию, чтобы начать адаптацию</p>
          <Link to="/create-vacancy" className="btn btn-primary mt-3">
            + Добавить вакансию
          </Link>
        </div>
      ) : (
        <div className="row g-4">
          {vacancies.map((vacancy) => (
            <div key={vacancy.id} className="col-md-6 col-lg-4">
              <div className="card h-100">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start mb-3">
                    <div>
                      <h5 className="card-title mb-1">{vacancy.title}</h5>
                      {vacancy.company && (
                        <h6 className="card-subtitle text-muted">
                          🏢 {vacancy.company}
                        </h6>
                      )}
                    </div>
                    <button
                      className="btn btn-sm btn-outline-danger"
                      onClick={() => handleDelete(vacancy.id, vacancy.title)}
                    >
                      ✕
                    </button>
                  </div>

                  <p className="card-text text-muted small">
                    {vacancy.description.substring(0, 120)}...
                  </p>

                  <div className="mb-3">
                    <strong className="small">Требуемые навыки:</strong>
                    <div className="mt-2">
                      {vacancy.parsed_skills?.slice(0, 5).map((skill, idx) => (
                        <span key={idx} className="skill-badge">{skill}</span>
                      ))}
                      {vacancy.parsed_skills?.length > 5 && (
                        <span className="badge bg-secondary">
                          +{vacancy.parsed_skills.length - 5}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="d-flex justify-content-between align-items-center mt-3 pt-2 border-top">
                    <small className="text-muted">
                      📅 {new Date(vacancy.created_at).toLocaleDateString()}
                    </small>
                    {vacancy.url && (
                      <a href={vacancy.url} target="_blank" rel="noopener noreferrer" className="small">
                        🔗 Ссылка
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default VacancyList;