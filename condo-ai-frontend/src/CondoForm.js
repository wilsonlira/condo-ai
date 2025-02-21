import { useState } from "react";

const CondoForm = ({ onSave, condo = {} }) => {
  const [name, setName] = useState(condo.name || "");
  const [address, setAddress] = useState(condo.address || "");
  const [cnpj, setCnpj] = useState(condo.cnpj || "");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ name, address, cnpj });
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded">
      <div className="mb-2">
        <label className="block">Nome:</label>
        <input 
          type="text" 
          value={name} 
          onChange={(e) => setName(e.target.value)} 
          className="border p-1 w-full" 
          required
        />
      </div>
      <div className="mb-2">
        <label className="block">Endereço:</label>
        <input 
          type="text" 
          value={address} 
          onChange={(e) => setAddress(e.target.value)} 
          className="border p-1 w-full" 
          required
        />
      </div>
      <div className="mb-2">
        <label className="block">CNPJ:</label>
        <input 
          type="text" 
          value={cnpj} 
          onChange={(e) => setCnpj(e.target.value)} 
          className="border p-1 w-full" 
          required
        />
      </div>
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Salvar</button>
    </form>
  );
};

export default CondoForm;
