import AvaliacaoEstrelas from './AvaliacaoEstrelas';

// Gera um matiz estável a partir do texto, para dar uma "capa" a cada jogo
// enquanto não existe imagem real.
const matiz = (texto) =>
  [...texto].reduce((soma, c) => soma + c.charCodeAt(0), 0) % 360;

const CardItem = ({ item, nota = 0, onAvaliar }) => (
  <article className="card-item">
    <div
      className="capa"
      style={{
        background: `linear-gradient(135deg, hsl(${matiz(item.categoria)} 55% 42%), hsl(${matiz(item.titulo)} 55% 22%))`,
      }}
    >
      <span aria-hidden="true">{item.titulo[0]}</span>
    </div>
    <h3>{item.titulo}</h3>
    <p className="categoria">{item.categoria}</p>
    <AvaliacaoEstrelas nota={nota} onAvaliar={(valor) => onAvaliar(item.id, valor)} />
  </article>
);

export default CardItem;
