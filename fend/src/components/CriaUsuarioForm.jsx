import React, { useState } from 'react';

const CriaUsuarioForm = ({ criaUsuario }) => {
  const [idUsuario, setIdUsuario] = useState('');
  const [nomeUsuario, setNomeUsuario] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (idUsuario && nomeUsuario) {
        criaUsuario({id: idUsuario, nome: nomeUsuario});
        setIdUsuario('');
        setNomeUsuario('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={idUsuario}
        onChange={(e) => setIdUsuario(e.target.value)}
        placeholder="Informe o ID do usuário"
      />

      <input
        type="text"
        value={nomeUsuario}
        onChange={(e) => setNomeUsuario(e.target.value)}
        placeholder="Informe o nome de usuário"
      />
      <button type="submit">Criar Usuário</button>
    </form>
  );
};

export default CriaUsuarioForm;
