import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { FaEdit, FaTrash, FaSave, FaTimes } from 'react-icons/fa';

// Composant principal de l'admin
export default function AdminPanel() {
  const [activeTab, setActiveTab] = useState('vehicule');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Operations Admin</h1>
      
      {/* Navigation par onglets */}
      <div className="flex border-b mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'vehicule' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
          onClick={() => {
            setActiveTab('vehicule');
            setCurrentPage(1);
          }}
        >
          Véhicule
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'ville' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
          onClick={() => {
            setActiveTab('ville');
            setCurrentPage(1);
          }}
        >
          Ville
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'autre' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
          onClick={() => {
            setActiveTab('autre');
            setCurrentPage(1);
          }}
        >
          Autre
        </button>
      </div>

      {/* Contenu dynamique */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {activeTab === 'vehicule' && (
          <EntityList 
            entityType="vehicule" 
            currentPage={currentPage} 
            setCurrentPage={setCurrentPage} 
            itemsPerPage={itemsPerPage} 
          />
        )}
        {activeTab === 'ville' && (
          <EntityList 
            entityType="ville" 
            currentPage={currentPage} 
            setCurrentPage={setCurrentPage} 
            itemsPerPage={itemsPerPage} 
          />
        )}
        {activeTab === 'autre' && (
          <EntityList 
            entityType="autre" 
            currentPage={currentPage} 
            setCurrentPage={setCurrentPage} 
            itemsPerPage={itemsPerPage} 
          />
        )}
      </div>
    </div>
  );
}

// Composant pour afficher la liste des entités
function EntityList({ entityType, currentPage, setCurrentPage, itemsPerPage }) {
  const queryClient = useQueryClient();
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});
  
  // Fetch data avec React Query
  const { data, isLoading, isError } = useQuery({
    queryKey: [entityType, currentPage],
    queryFn: async () => {
      // Remplacez ceci par votre appel API réel
      const response = await fetch(`/api/${entityType}?page=${currentPage}&limit=${itemsPerPage}`);
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    },
    keepPreviousData: true,
  });

  // Mutation pour supprimer un élément
  const deleteMutation = useMutation({
    mutationFn: (id) => fetch(`/api/${entityType}/${id}`, { method: 'DELETE' }),
    onSuccess: () => {
      queryClient.invalidateQueries([entityType]);
    },
  });

  // Mutation pour mettre à jour un élément
  const updateMutation = useMutation({
    mutationFn: (updatedItem) => 
      fetch(`/api/${entityType}/${updatedItem.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedItem),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries([entityType]);
      setEditingId(null);
    },
  });

  // Gérer le changement de formulaire
  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditForm(prev => ({ ...prev, [name]: value }));
  };

  // Gérer la soumission du formulaire
  const handleEditSubmit = (e) => {
    e.preventDefault();
    updateMutation.mutate(editForm);
  };

  // Déterminer les colonnes à afficher selon le type d'entité
  const getColumns = () => {
    switch (entityType) {
      case 'vehicule':
        return ['id', 'nom', 'conso', 'autre'];
      case 'ville':
        return ['id', 'nom', 'description'];
      default:
        return ['id', 'nom', 'info'];
    }
  };

  const columns = getColumns();

  if (isLoading) return <div className="p-4">Chargement...</div>;
  if (isError) return <div className="p-4 text-red-500">Erreur lors du chargement des données</div>;

  return (
    <div>
      {/* En-tête du tableau */}
      <div className="grid grid-cols-12 bg-gray-100 p-3 font-medium">
        {columns.map(col => (
          <div key={col} className="col-span-2 capitalize">{col}</div>
        ))}
        <div className="col-span-2">Actions</div>
      </div>

      {/* Corps du tableau */}
      {data.items.map(item => (
        <div key={item.id} className="grid grid-cols-12 border-b p-3 items-center">
          {columns.map(col => (
            <div key={`${item.id}-${col}`} className="col-span-2">
              {editingId === item.id ? (
                <input
                  type="text"
                  name={col}
                  value={editForm[col] || ''}
                  onChange={handleEditChange}
                  className="w-full p-1 border rounded"
                />
              ) : (
                item[col]
              )}
            </div>
          ))}
          
          <div className="col-span-2 flex space-x-2">
            {editingId === item.id ? (
              <>
                <button 
                  onClick={handleEditSubmit}
                  className="px-2 py-1 bg-green-500 text-white rounded hover:bg-green-600 flex items-center gap-1"
                >
                  <FaSave /> Sauvegarder
                </button>
                <button 
                  onClick={() => setEditingId(null)}
                  className="px-2 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 flex items-center gap-1"
                >
                  <FaTimes /> Annuler
                </button>
              </>
            ) : (
              <>
                <button 
                  onClick={() => {
                    setEditingId(item.id);
                    setEditForm({ ...item });
                  }}
                  className="p-1 text-blue-500 hover:text-blue-700"
                  title="Modifier"
                >
                  <FaEdit className="text-lg" />
                </button>
                <button 
                  onClick={() => deleteMutation.mutate(item.id)}
                  className="p-1 text-red-500 hover:text-red-700"
                  title="Supprimer"
                >
                  <FaTrash className="text-lg" />
                </button>
              </>
            )}
          </div>
        </div>
      ))}

      {/* Pagination */}
      <div className="flex justify-between items-center p-3 bg-gray-50">
        <button
          onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
          className={`px-4 py-2 rounded ${currentPage === 1 ? 'bg-gray-200 cursor-not-allowed' : 'bg-blue-500 text-white hover:bg-blue-600'}`}
        >
          Précédent
        </button>
        <span>Page {currentPage} sur {Math.ceil(data.totalCount / itemsPerPage)}</span>
        <button
          onClick={() => setCurrentPage(prev => prev + 1)}
          disabled={currentPage >= Math.ceil(data.totalCount / itemsPerPage)}
          className={`px-4 py-2 rounded ${currentPage >= Math.ceil(data.totalCount / itemsPerPage) ? 'bg-gray-200 cursor-not-allowed' : 'bg-blue-500 text-white hover:bg-blue-600'}`}
        >
          Suivant
        </button>
      </div>
    </div>
  );
}