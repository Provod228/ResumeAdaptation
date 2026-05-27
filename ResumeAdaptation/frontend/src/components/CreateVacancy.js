import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createVacancy } from '../services/api';

function CreateVacancy() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    description: '',
    url: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createVacancy(formData);
      navigate('/vacancies');
    } catch (err) {
      setError('Ошибка создания вакансии');
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-4">Добавление вакансии</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Название вакансии *</label>
          <input
            type="text"
            className="form-control"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            placeholder="Например: Senior Python Developer"
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Компания</label>
          <input
            type="text"
            className="form-control"
            name="company"
            value={formData.company}
            onChange={handleChange}
            placeholder="Название компании"
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Описание вакансии *</label>
          <textarea
            className="form-control"
            name="description"
            rows="10"
            value={formData.description}
            onChange={handleChange}
            required
            placeholder="Введите полное описание вакансии, требования, обязанности..."
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Ссылка на вакансию</label>
          <input
            type="url"
            className="form-control"
            name="url"
            value={formData.url}
            onChange={handleChange}
            placeholder="https://hh.ru/vacancy/..."
          />
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Добавление...' : 'Добавить вакансию'}
        </button>
        <button
          type="button"
          className="btn btn-secondary ms-2"
          onClick={() => navigate('/vacancies')}
        >
          Отмена
        </button>
      </form>
    </div>
  );
}

export default CreateVacancy;