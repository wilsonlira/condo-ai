import { useState, useEffect } from "react";

const ListaDocumentos = () => {
  const [atas, setAtas] = useState([]);
  const [comunicados, setComunicados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editando, setEditando] = useState(null);
  const [tituloEdit, setTituloEdit] = useState("");
  const [conteudoEdit, setConteudoEdit] = useState("");
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    const fetchDocumentos = async () => {
      try {
        const resAtas = await fetch(`${process.env.REACT_APP_BACKEND}/atas/`);
        const dataAtas = await resAtas.json();

        const resComunicados = await fetch(`${process.env.REACT_APP_BACKEND}/comunicados/`);
        const dataComunicados = await resComunicados.json();

        setAtas(dataAtas);
        setComunicados(dataComunicados);
      } catch (error) {
        console.error("Erro ao buscar documentos:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDocumentos();
  }, []);

  const excluirDocumento = async (tipo, id) => {
    const url = tipo === "Ata"
      ? `${process.env.REACT_APP_BACKEND}/atas/${id}`
      : `${process.env.REACT_APP_BACKEND}/comunicados/${id}`;

    try {
      await fetch(url, { method: "DELETE" });

      if (tipo === "Ata") {
        setAtas(atas.filter((ata) => ata.id !== id));
      } else {
        setComunicados(comunicados.filter((comunicado) => comunicado.id !== id));
      }
    } catch (error) {
      console.error("Erro ao excluir documento:", error);
    }
  };

  const iniciarEdicao = (doc, tipo) => {
    setEditando({
      id: doc.id,
      tipo,
      condominio_id: doc.condominio_id ?? 1, // Defina um valor padrão válido
    });
    setTituloEdit(doc.titulo);
    setConteudoEdit(doc.conteudo);
  };

  const salvarEdicao = async () => {
    if (!editando || !tituloEdit || !conteudoEdit) {
      setMensagem("❌ Preencha todos os campos antes de salvar.");
      return;
    }

    const url = editando.tipo === "Ata"
      ? `${process.env.REACT_APP_BACKEND}/atas/${editando.id}`
      : `${process.env.REACT_APP_BACKEND}/comunicados/${editando.id}`;

    const documentoEditado = {
      titulo: tituloEdit,
      conteudo: conteudoEdit,
    };
    
    if (editando.condominio_id) {
      documentoEditado.condominio_id = Number(editando.condominio_id);
    }
      

    try {
      const response = await fetch(url, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(documentoEditado),
      });

      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${await response.text()}`);
      }

      setMensagem("✅ Documento atualizado com sucesso!");

      if (editando.tipo === "Ata") {
        setAtas(atas.map((ata) => (ata.id === editando.id ? { ...ata, ...documentoEditado } : ata)));
      } else {
        setComunicados(comunicados.map((comunicado) => (comunicado.id === editando.id ? { ...comunicado, ...documentoEditado } : comunicado)));
      }

      setEditando(null);
    } catch (error) {
      console.error("Erro ao atualizar documento:", error);
      setMensagem("❌ Erro ao atualizar documento. Tente novamente.");
    }
  };

  if (loading) {
    return <p className="text-center">Carregando documentos...</p>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-5 border rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Lista de Atas e Comunicados</h2>

      {mensagem && (
        <div className={`mb-4 p-2 rounded text-center ${mensagem.includes("Erro") ? "bg-red-200 text-red-800" : "bg-green-200 text-green-800"}`}>
          {mensagem}
        </div>
      )}

      <h3 className="text-lg font-semibold mt-4">Atas</h3>
      {atas.length > 0 ? (
        <ul>
          {atas.map((ata) => (
            <li key={`ata-${ata.id}`} className="border-b py-2">
              {editando?.id === ata.id ? (
                <div>
                  <input type="text" className="w-full p-2 border rounded mt-1 mb-2" value={tituloEdit} onChange={(e) => setTituloEdit(e.target.value)} />
                  <textarea className="w-full p-2 border rounded mt-1 mb-2" rows="3" value={conteudoEdit} onChange={(e) => setConteudoEdit(e.target.value)} />
                  <button className="bg-green-500 text-white px-3 py-1 rounded mr-2" onClick={salvarEdicao}>Salvar</button>
                  <button className="bg-gray-500 text-white px-3 py-1 rounded" onClick={() => setEditando(null)}>Cancelar</button>
                </div>
              ) : (
                <div>
                  <strong>{ata.titulo}</strong> - {ata.condominio_nome}
                  <p>{ata.conteudo}</p>
                  <button className="bg-blue-500 text-white px-3 py-1 rounded mr-2" onClick={() => iniciarEdicao(ata, "Ata")}>Editar</button>
                  <button className="bg-red-500 text-white px-3 py-1 rounded" onClick={() => excluirDocumento("Ata", ata.id)}>Excluir</button>
                </div>
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p>Nenhuma ata cadastrada.</p>
      )}

      <h3 className="text-lg font-semibold mt-4">Comunicados</h3>
      {comunicados.length > 0 ? (
        <ul>
          {comunicados.map((comunicado) => (
            <li key={`comunicado-${comunicado.id}`} className="border-b py-2">
              {editando?.id === comunicado.id ? (
                <div>
                  <input type="text" className="w-full p-2 border rounded mt-1 mb-2" value={tituloEdit} onChange={(e) => setTituloEdit(e.target.value)} />
                  <textarea className="w-full p-2 border rounded mt-1 mb-2" rows="3" value={conteudoEdit} onChange={(e) => setConteudoEdit(e.target.value)} />
                  <button className="bg-green-500 text-white px-3 py-1 rounded mr-2" onClick={salvarEdicao}>Salvar</button>
                  <button className="bg-gray-500 text-white px-3 py-1 rounded" onClick={() => setEditando(null)}>Cancelar</button>
                </div>
              ) : (
                <div>
                  <strong>{comunicado.titulo}</strong> - {comunicado.condominio_nome}
                  <p>{comunicado.conteudo}</p>
                  <button className="bg-blue-500 text-white px-3 py-1 rounded mr-2" onClick={() => iniciarEdicao(comunicado, "Comunicado")}>Editar</button>
                  <button className="bg-red-500 text-white px-3 py-1 rounded" onClick={() => excluirDocumento("Comunicado", comunicado.id)}>Excluir</button>
                </div>
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p>Nenhum comunicado cadastrado.</p>
      )}
    </div>
  );
};

export default ListaDocumentos;
