const SeletorUsuario = ({ usuarios, usuarioId, onChange }) => (
  <label className="seletor-usuario">
    Entrar como
    <select value={usuarioId} onChange={(e) => onChange(e.target.value)}>
      <option value="">Selecione…</option>
      {usuarios.map((usuario) => (
        <option key={usuario.id} value={usuario.id}>
          {usuario.nome}
        </option>
      ))}
    </select>
  </label>
);

export default SeletorUsuario;
