import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import api from '../api.js';
import Home from './Home';

// Troca o axios por um dublê: os testes não dependem do backend rodando.
vi.mock('../api.js', () => ({ default: { get: vi.fn(), post: vi.fn() } }));

const jogos = [
  { id: 'hades', titulo: 'Hades', categoria: 'acao' },
  { id: 'celeste', titulo: 'Celeste', categoria: 'plataforma' },
];

const chamadasA = (url) => api.get.mock.calls.filter(([u]) => u === url);

beforeEach(() => {
  vi.clearAllMocks();
  api.get.mockImplementation((url) => {
    if (url.startsWith('/recomendacoes/')) return Promise.resolve({ data: [jogos[0]] });
    if (url === '/itens') return Promise.resolve({ data: jogos });
    if (url.endsWith('/avaliacoes')) return Promise.resolve({ data: { hades: 4 } });
    return Promise.reject(new Error(`URL inesperada: ${url}`));
  });
});

describe('Home', () => {
  it('pede para escolher um usuário e não chama a API sem usuário', () => {
    render(<Home usuarioId="" />);

    expect(screen.getByText(/escolha um usuário/i)).toBeInTheDocument();
    expect(api.get).not.toHaveBeenCalled();
  });

  it('mostra uma fileira para cada estratégia e o catálogo', async () => {
    render(<Home usuarioId="alice" />);

    expect(await screen.findByRole('heading', { name: 'Recomendados para você' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Mais do que você curte' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /gosto parecido/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Todos os jogos' })).toBeInTheDocument();

    expect(api.get).toHaveBeenCalledWith('/recomendacoes/alice', {
      params: { tipo: 'colaborativa', n: 10 },
    });
  });

  it('envia a avaliação e recarrega as fileiras', async () => {
    api.post.mockResolvedValue({ data: { status: 'registrado' } });
    render(<Home usuarioId="alice" />);
    await screen.findByRole('heading', { name: 'Todos os jogos' });
    expect(chamadasA('/itens')).toHaveLength(1);

    // primeiro card da primeira fileira = Hades
    await userEvent.setup().click(screen.getAllByRole('button', { name: '5 estrelas' })[0]);

    expect(api.post).toHaveBeenCalledWith('/interacoes', {
      usuario_id: 'alice',
      item_id: 'hades',
      nota: 5,
    });
    await waitFor(() => expect(chamadasA('/itens')).toHaveLength(2));
  });

  it('mostra o erro devolvido pela API', async () => {
    api.get.mockRejectedValue({ response: { data: { detail: 'Usuário não encontrado' } } });
    render(<Home usuarioId="fantasma" />);

    expect(await screen.findByRole('alert')).toHaveTextContent('Usuário não encontrado');
  });
});
