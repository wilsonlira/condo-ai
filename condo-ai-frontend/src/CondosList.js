import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// const API_URL = 'https://didactic-space-funicular-jjjp5q74pqg72gvx-8000.app.github.dev/condominios/';

const CondosList = () => {
  const [condominios, setCondominios] = useState([]);
  const [nome, setNome] = useState("");
  const [endereco, setEndereco] = useState("");

  useEffect(() => {
    fetch(process.env.REACT_APP_BACKEND)
      .then((response) => response.json())
      .then((data) => setCondominios(data))
      .catch((error) => console.error("Erro ao buscar condomínios:", error));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    const novoCondominio = { nome, endereco };

    fetch(process.env.REACT_APP_BACKEND, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(novoCondominio),
    })
      .then((response) => response.json())
      .then((data) => {
        setCondominios([...condominios, data]); // Atualiza a lista com o novo condomínio
        setNome("");
        setEndereco("");
      })
      .catch((error) => console.error("Erro ao adicionar condomínio:", error));
  };

  return (
    <div>
      <h2>Lista de Condomínios</h2>
      <ul>
        {condominios.map((condo) => (
          <li key={condo.id}>
            {condo.nome} - {condo.endereco}
          </li>
        ))}
      </ul>

      <h3>Adicionar Novo Condomínio</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Endereço"
          value={endereco}
          onChange={(e) => setEndereco(e.target.value)}
          required
        />
        <button type="submit">Adicionar</button>
      </form>
    </div>
  );
};
console.log("API_URL:", process.env.REACT_APP_BACKEND);

export default CondosList;
