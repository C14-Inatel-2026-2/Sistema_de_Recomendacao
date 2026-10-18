import { useCallback, useEffect, useRef, useState } from 'react';
import api from '../api.js';
import { FILEIRAS, TAMANHO_FILEIRA } from '../fileiras.js';

export default function useHome(usuarioId) {
  const [fileiras, setFileiras] = useState([]);
  const [notas, setNotas] = useState({});
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(null);
  const requisicao = useRef(0);

  const carregar = useCallback(async () => {
    const id = ++requisicao.current;
    if (!usuarioId) {
      setFileiras([]);
      setNotas({});
      return;
    }
    setCarregando(true);
    setErro(null);
    try {
      const [recomendadas, catalogo, avaliacoes] = await Promise.all([
        Promise.all(
          FILEIRAS.map(({ tipo }) =>
            api.get(`/recomendacoes/${usuarioId}`, { params: { tipo, n: TAMANHO_FILEIRA } }),
          ),
        ),
        api.get('/itens'),
        api.get(`/usuarios/${usuarioId}/avaliacoes`),
      ]);
      if (id !== requisicao.current) return;
      setFileiras([
        ...FILEIRAS.map((fileira, i) => ({ ...fileira, itens: recomendadas[i].data })),
        { tipo: 'catalogo', titulo: 'Todos os jogos', itens: catalogo.data },
      ]);
      setNotas(avaliacoes.data);
    } catch (e) {
      if (id !== requisicao.current) return;
      setErro(e.response?.data?.detail ?? 'Não foi possível carregar a página inicial.');
    } finally {
      if (id === requisicao.current) setCarregando(false);
    }
  }, [usuarioId]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  return { fileiras, notas, carregando, erro, recarregar: carregar };
}
