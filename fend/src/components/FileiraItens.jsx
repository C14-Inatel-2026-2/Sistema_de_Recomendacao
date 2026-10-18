import CardItem from './CardItem';

const FileiraItens = ({ titulo, itens, notas, onAvaliar }) => (
  <section className="fileira">
    <h2>{titulo}</h2>
    {itens.length === 0 ? (
      <p className="vazia">Nenhum jogo por aqui ainda. Avalie alguns jogos para preencher esta lista.</p>
    ) : (
      <div className="fileira-itens">
        {itens.map((item) => (
          <CardItem key={item.id} item={item} nota={notas[item.id] ?? 0} onAvaliar={onAvaliar} />
        ))}
      </div>
    )}
  </section>
);

export default FileiraItens;
