import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import AvaliacaoEstrelas from './AvaliacaoEstrelas';

describe('AvaliacaoEstrelas', () => {
  it('renderiza cinco estrelas', () => {
    render(<AvaliacaoEstrelas onAvaliar={() => {}} />);
    expect(screen.getAllByRole('button')).toHaveLength(5);
  });

  it('marca como ativas as estrelas até a nota atual', () => {
    render(<AvaliacaoEstrelas nota={3} onAvaliar={() => {}} />);
    const ativas = screen
      .getAllByRole('button')
      .filter((estrela) => estrela.getAttribute('aria-pressed') === 'true');
    expect(ativas).toHaveLength(3);
  });

  it('chama onAvaliar com o valor da estrela clicada', async () => {
    const onAvaliar = vi.fn();
    render(<AvaliacaoEstrelas onAvaliar={onAvaliar} />);

    await userEvent.setup().click(screen.getByRole('button', { name: '4 estrelas' }));

    expect(onAvaliar).toHaveBeenCalledTimes(1);
    expect(onAvaliar).toHaveBeenCalledWith(4);
  });
});
