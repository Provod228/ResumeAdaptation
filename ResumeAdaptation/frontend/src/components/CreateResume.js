import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createResume } from '../services/api';

function CreateResume() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    text: ''
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
      await createResume(formData);
      navigate('/resumes');
    } catch (err) {
      setError('Ошибка создания резюме');
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-4">Создание нового резюме</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Название резюме</label>
          <input
            type="text"
            className="form-control"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            placeholder="Например: Python-разработчик"
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Текст резюме</label>
          <textarea
            className="form-control"
            name="text"
            rows="10"
            value={formData.text}
            onChange={handleChange}
            required
            placeholder="Введите полный текст вашего резюме..."
          />
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Создание...' : 'Создать резюме'}
        </button>
        <button
          type="button"
          className="btn btn-secondary ms-2"
          onClick={() => navigate('/resumes')}
        >
          Отмена
        </button>
      </form>
    </div>
  );
}

export default CreateResume;