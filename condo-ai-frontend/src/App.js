import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import CadastroAtasComunicados from "./components/CadastroAtasComunicados";
import CadastroComunicados from "./components/CadastroComunicados";
import CadastroCondominios from "./components/CadastroCondominios";
import ListaDocumentos from "./components/ListaDocumentos";

const Home = () => (
  <div>
    <h1>Bem-vindo ao Condo AI</h1>
    <p>Selecione uma opção no menu acima.</p>
  </div>
);

const CadastroAtaPage = () => (
  <div>
    <h2>Cadastro de Comunicados</h2>
    <CadastroAtasComunicados />
    <ListaDocumentos />  {/* Lista de documentos abaixo do cadastro */}
  </div>
);

const CadastroComunicadoPage = () => (
  <div>
    <h2>Comunicados</h2>
    <CadastroComunicados />
    <ListaDocumentos />  {/* Lista de documentos abaixo do cadastro */}
  </div>
);

const CadastroCondominioPage = () => (
  <div>
    <h2>Condominios</h2>
    <CadastroCondominios />
    <ListaDocumentos />  {/* Lista de documentos abaixo do cadastro */}
  </div>
);

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/cadastro-atas-comunicados">Cadastro de Atas e Comunicados</Link></li>
            <li><Link to="/cadastro-comunicados">Cadastro de Comunicados</Link></li>
            <li><Link to="/cadastro-condominios">Cadastro de Condominios</Link></li>
            <li><Link to="/lista-documentos">Lista de Documentos</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cadastro-atas-comunicados" element={<CadastroAtaPage />} />
          <Route path="/cadastro-comunicados" element={<CadastroComunicadoPage />} />
          <Route path="/cadastro-condominios" element={<CadastroCondominioPage />} />
          <Route path="/lista-documentos" element={<ListaDocumentos />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
