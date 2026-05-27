import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getResumes, deleteResume } from '../services/api';

function ResumeList() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      const response = await getResumes();
      setResumes(response.data);
      setLoading(false);
    } catch (err) {
      setError('Ошибка загрузки резюме');
      setLoading(false);
    }
  };

  const handleDelete = async (id, title) => {
    if (window.confirm(`Удалить резюме "${title}"?`)) {
      try {
        await deleteResume(id);
        loadResumes();
      } catch (err) {
        alert('Ошибка удаления');
      }
    }
  };

  if (loading) return <div className="text-center">Загрузка...</div>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>📄 Мои резюме</h2>
        <Link to="/create-resume" className="btn btn-success">
          + Создать резюме
        </Link>
      </div>

      {resumes.length === 0 ? (
        <div className="alert alert-info">
          У вас пока нет резюме. Создайте первое!
        </div>
      ) : (
        <div className="row">
          {resumes.map((resume) => (
            <div key={resume.id} className="col-md-6 mb-3">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{resume.title}</h5>
                  <p className="card-text text-muted">
                    {resume.text.substring(0, 100)}...
                  </p>
                  <div className="mb-2">
                    <strong>Навыки:</strong>
                    {resume.parsed_skills?.slice(0, 5).map((skill, idx) => (
                      <span key={idx} className="skill-badge">{skill}</span>
                    ))}
                    {resume.parsed_skills?.length > 5 && (
                      <span className="text-muted"> +{resume.parsed_skills.length - 5}</span>
                    )}
                  </div>
                  <div className="d-flex justify-content-between">
                    <small className="text-muted">
                      Создано: {new Date(resume.created_at).toLocaleDateString()}
                    </small>
                    <div>
                      <button
                        className="btn btn-sm btn-outline-danger me-2"
                        onClick={() => handleDelete(resume.id, resume.title)}
                      >
                        Удалить
                      </button>
                    </div>
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

export default ResumeList;