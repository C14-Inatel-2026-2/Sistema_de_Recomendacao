const VALORES = [1, 2, 3, 4, 5];

const AvaliacaoEstrelas = ({ nota = 0, onAvaliar }) => (
  <div className="estrelas" role="group" aria-label="Sua avaliação">
    {VALORES.map((valor) => (
      <button
        key={valor}
        type="button"
        className={valor <= nota ? 'estrela ativa' : 'estrela'}
        aria-label={`${valor} ${valor === 1 ? 'estrela' : 'estrelas'}`}
        aria-pressed={valor <= nota}
        onClick={() => onAvaliar(valor)}
      >
        ★
      </button>
    ))}
  </div>
);

export default AvaliacaoEstrelas;
