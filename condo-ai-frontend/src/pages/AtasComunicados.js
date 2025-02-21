import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import DocumentosList from "./pages/DocumentosList";
import DocumentoForm from "./pages/DocumentoForm";
import ConsultaIA from "./pages/ConsultaIA";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/documentos" element={<DocumentosList />} />
        <Route path="/documentos/novo" element={<DocumentoForm />} />
        <Route path="/documentos/:id" element={<DocumentoForm />} />
        <Route path="/consulta" element={<ConsultaIA />} />
      </Routes>
    </Router>
  );
}

export default App;
