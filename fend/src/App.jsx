import { useEffect, useState } from 'react';
import api from './api.js';
import SeletorUsuario from './components/SeletorUsuario';
import Home from './pages/Home';
import './Home.css';

function App() {
  const [usuarios, setUsuarios] = useState([]);
  const [usuarioId, setUsuarioId] = useState('');

  useEffect(() => {
    api
      .get('/usuarios')
      .then(({ data }) => {
        setUsuarios(data);
        setUsuarioId(data[0]?.id ?? '');
      })
      .catch((e) => console.error('Erro ao buscar usuários.', e));
  }, []);

  return (
    <div className="App">
      <header className="topo">
        <h1>Sistema de Recomendação</h1>
        <SeletorUsuario usuarios={usuarios} usuarioId={usuarioId} onChange={setUsuarioId} />
      </header>
      <main>
        <Home usuarioId={usuarioId} />
      </main>
    </div>
  );
}

export default App;
