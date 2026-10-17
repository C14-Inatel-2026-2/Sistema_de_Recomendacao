import React, { useEffect, useState } from 'react';
import api from "../api.js";
import CriaItemForm from './CriaItemForm';

const Itens = () => {
  const [itens, setItens] = useState([]);

  const fetchItens = async () => {
    try {
      const response = await api.get('/itens');
      setItens(response.data);
    } catch (error) {
      console.error("Error fetching itens", error);
    }
  };

  const criaItem = async (idItem, tituloItem, categoriaItem) => {
    try {
      await api.post('/itens', { id: idItem, titulo: tituloItem, categoria: categoriaItem });
      fetchItens();
    } catch (error) {
      console.error("Erro ao criar item.", error);
    }
  };

  useEffect(() => {
    fetchItens();
  }, []);

  return (
    <div>
      <h2>Lista de Itens</h2>
      <ul>
        {itens && itens.map(item) => (
          <li key={item.id}>{{item.titulo} ({item.categoria})}</li>
        ))}
      </ul>
      <CriaItemForm criaItem={criaItem} />
    </div>
  );
};

export default Itens;
