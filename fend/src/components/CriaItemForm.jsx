import React, { useState } from 'react';

const CriaItemForm = ({ criaItem }) => {
  const [idItem, setIdItem] = useState('');
  const [tituloItem, setTituloItem] = useState('');
  const [categoriaItem, setCategoriaItem] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (idItem && tituloItem && categoriaItem) {
        criaItem(idItem, tituloItem, categoriaItem);
        setIdItem('');
        setTituloItem('');
        setCategoriaItem('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={idItem}
        onChange={(e) => setIdItem(e.target.value)}
        placeholder="Informe o ID do item"
      />

      <input
        type="text"
        value={tituloItem}
        onChange={(e) => setTituloItem(e.target.value)}
        placeholder="Informe o titulo do item"
      />

      <input
        type="text"
        value={categoriaItem}
        onChange={(e) => setCategoriaItem(e.target.value)}
        placeholder="Informe a categoria do item"
      />
      <button type="submit">Criar Item</button>
    </form>
  );
};

export default CriaItemForm;
