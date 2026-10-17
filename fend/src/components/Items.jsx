import React, { useEffect, useState } from 'react';
import api from "../api.js";
import CriaItemForm from './CriaItemForm';

const Itens = () => {
  const [itens, setItem] = useState([]);

  //const fetchFruits = async () => {
    //try {
      //const response = await api.get('/fruits');
      //setFruits(response.data.fruits);
    //} catch (error) {
      //console.error("Error fetching fruits", error);
    //}
  //};

  const addItem = async (idItem, tituloItem, categoriaItem) => {
    try {
      await api.post('/usuarios', { id: idItem, titulo: tituloItem, categoria: categoriaItem });
      //fetchFruits();  // Refresh the list after adding a fruit
    } catch (error) {
      console.error("Erro ao criar item.", error);
    }
  };

  //useEffect(() => {
    //fetchFruits();
  //}, []);

  return (
    <div>
      <h2>Lista de Itens</h2>
      <ul>
        {itens.map((item, id) => (
          <li key={id}>{item.titulo, item.categoria}</li>
        ))}
      </ul>
      <CriaItemForm addItem={addItem} />
    </div>
  );
};

export default Itens;
