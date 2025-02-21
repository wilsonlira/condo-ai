import { useState } from "react";

const CadastroAtasComunicados = () => {
  const [titulo, setTitulo] = useState("");
  const [conteudo, setConteudo] = useState("");
  const [condominioId, setCondominioId] = useState("");
  const [mensagem, setMensagem] = useState(""); // Mensagem de feedback
  const [carregando, setCarregando] = useState(false); // Estado de loading

  const handleSubmit = async (e) => {
    e.preventDefault();
    setCarregando(true);
    setMensagem(""); // Limpa a mensagem ao iniciar um novo envio

    const novaAta = {
      titulo,
      conteudo,
      condominio_id: Number(condominioId), // Garante que seja um número
    };

    try {
      console.log("Chamando API em:", `${process.env.REACT_APP_BACKEND}/atas/`);
      
      const resposta = await fetch(`${process.env.REACT_APP_BACKEND}/atas/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(novaAta),
      });

      if (!resposta.ok) {
        throw new Error(`Erro: ${resposta.status}`);
      }

      const data = await resposta.json();
      console.log("Ata cadastrada:", data);

      // Limpar os campos após o sucesso
      setTitulo("");
      setConteudo("");
      setCondominioId("");
      setMensagem("✅ Ata cadastrada com sucesso!");
    } catch (erro) {
      console.error("Erro ao cadastrar ata:", erro);
      setMensagem("❌ Erro ao cadastrar ata. Verifique os dados e tente novamente.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-5 border rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Cadastro de Atas e Comunicados</h2>

      {/* Exibir mensagem de sucesso ou erro */}
      {mensagem && (
        <div className={`mb-4 p-2 rounded text-center ${mensagem.includes("Erro") ? "bg-red-200 text-red-800" : "bg-green-200 text-green-800"}`}>
          {mensagem}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <label className="block font-semibold">Título:</label>
        <input
          type="text"
          className="w-full p-2 border rounded mt-1 mb-3"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
          required
        />

        <label className="block font-semibold">Conteúdo:</label>
        <textarea
          className="w-full p-2 border rounded mt-1 mb-3"
          rows="4"
          value={conteudo}
          onChange={(e) => setConteudo(e.target.value)}
          required
        />

        <label className="block font-semibold">Condomínio ID:</label>
        <input
          type="number"
          className="w-full p-2 border rounded mt-1 mb-3"
          value={condominioId}
          onChange={(e) => setCondominioId(e.target.value)}
          required
        />

        <button
          type="submit"
          className={`px-4 py-2 rounded text-white ${carregando ? "bg-gray-400" : "bg-blue-500 hover:bg-blue-600"}`}
          disabled={carregando}
        >
          {carregando ? "Cadastrando..." : "Cadastrar"}
        </button>
      </form>
    </div>
  );
};

export default CadastroAtasComunicados;
