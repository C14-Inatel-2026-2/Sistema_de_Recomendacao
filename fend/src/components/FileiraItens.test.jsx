import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import FileiraItens from './FileiraItens';

const itens = [
  { id: 'hades', titulo: 'Hades', categoria: 'acao' },
  { id: 'celeste', titulo: 'Celeste', categoria: 'plataforma' },
];

describe('FileiraItens', () => {
  it('mostra o título da fileira e um card por jogo', () => {
    render(<FileiraItens titulo="Recomendados" itens={itens} notas={{}} onAvaliar={() => {}} />);

    expect(screen.getByRole('heading', { name: 'Recomendados' })).toBeInTheDocument();
    expect(screen.getAllByRole('article')).toHaveLength(2);
    expect(screen.getByText('Hades')).toBeInTheDocument();
  });

  it('mostra uma mensagem quando não há jogos', () => {
    render(<FileiraItens titulo="Recomendados" itens={[]} notas={{}} onAvaliar={() => {}} />);

    expect(screen.getByText(/nenhum jogo por aqui/i)).toBeInTheDocument();
    expect(screen.queryByRole('article')).not.toBeInTheDocument();
  });

  it('exibe a nota que o usuário já deu ao jogo', () => {
    render(<FileiraItens titulo="Recomendados" itens={itens} notas={{ hades: 4 }} onAvaliar={() => {}} />);

    const [cardHades] = screen.getAllByRole('article');
    const ativas = cardHades.querySelectorAll('[aria-pressed="true"]');
    expect(ativas).toHaveLength(4);
  });

  it('repassa o id do jogo e a nota ao avaliar', async () => {
    const onAvaliar = vi.fn();
    render(<FileiraItens titulo="Recomendados" itens={itens} notas={{}} onAvaliar={onAvaliar} />);

    await userEvent.setup().click(screen.getAllByRole('button', { name: '5 estrelas' })[1]);

    expect(onAvaliar).toHaveBeenCalledWith('celeste', 5);
  });
});
