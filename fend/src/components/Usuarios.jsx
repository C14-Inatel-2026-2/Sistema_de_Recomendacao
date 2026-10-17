import React, { useEffect, useState } from 'react';
import api from "../api.js";
import CriaUsuarioForm from './CriaUsuarioForm';

const Usuarios = () => {
  const [usuarios, setUser] = useState([]);

  const fetchUsuario = async () => {
    try {
      const response = await api.get('/usuarios');
      setUser(response.data.usuarios);
    } catch (error) {
      console.error("Error fetching users", error);
    }
  };

  const criaUsuario = async (idUser, nomeUser) => {
    try {
      await api.post('/usuarios', { id: idUser, nome: nomeUser });
      fetchUsuario();
    } catch (error) {
      console.error("Erro ao criar usuário.", error);
    }
  };

  useEffect(() => {
    fetchUsuario();
  }, []);

  return (
    <div>
      <h2>Lista de Usuários</h2>
      <ul>
        {usuarios.map((usuario, id) => (
          <li key={id}>{usuario.nome}</li>
        ))}
      </ul>
      <CriaUsuarioForm criaUsuario={criaUsuario} />
    </div>
  );
};

export default Usuarios;
