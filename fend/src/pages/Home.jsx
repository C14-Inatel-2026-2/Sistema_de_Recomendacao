import api from '../api.js';
import FileiraItens from '../components/FileiraItens';
import useHome from '../hooks/useHome';

const Home = ({ usuarioId }) => {
  const { fileiras, notas, carregando, erro, recarregar } = useHome(usuarioId);

  const avaliar = async (itemId, nota) => {
    try {
      await api.post('/interacoes', { usuario_id: usuarioId, item_id: itemId, nota });
      await recarregar();
    } catch (e) {
      console.error('Erro ao registrar avaliação.', e.response?.data ?? e);
    }
  };

  if (!usuarioId) return <p className="home">Escolha um usuário para ver sua página inicial.</p>;
  if (erro) return <p className="home" role="alert">{erro}</p>;
  if (carregando && fileiras.length === 0) return <p className="home">Carregando…</p>;

  return (
    <div className="home">
      {fileiras.map(({ tipo, titulo, itens }) => (
        <FileiraItens key={tipo} titulo={titulo} itens={itens} notas={notas} onAvaliar={avaliar} />
      ))}
    </div>
  );
};

export default Home;
