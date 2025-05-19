import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, message } from 'antd';


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const EmissionsAdmin = () => {
  const [emissions, setEmissions] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [currentEmission, setCurrentEmission] = useState(null);
  const [form] = Form.useForm();
  const [editForm] = Form.useForm();

  useEffect(() => {
    fetchEmissions();
  }, []);

  const fetchEmissions = async () => {
    try {
      console.log('Fetching emissions...');
      const response = await fetch(`${API_BASE_URL}/distance/compare?distance_km=1`);
      if (!response.ok) throw new Error('Erreur lors de la récupération des données');
      const data = await response.json();
      console.log('Fetched emissions:');
      console.log(data);
      setEmissions(data);

      
    } catch (error) {
      message.error(error.message);
    }
  };

  const handleAdd = () => {
    form.resetFields();
    setIsModalVisible(true);
  };

  const handleEdit = (record) => {
    setCurrentEmission(record);
    editForm.setFieldsValue({
      mode_transport: record.mode_transport,
      emission_par_km: record.emission_par_km
    });
    setIsEditModalVisible(true);
  };

  const handleDelete = async (mode_transport) => {
    try {
      const response = await fetch(`${API_BASE_URL}/admin/emissions/${mode_transport}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (!response.ok) throw new Error('Erreur lors de la suppression');
      
      message.success('Mode de transport supprimé avec succès');
      fetchEmissions();
    } catch (error) {
      message.error(error.message);
    }
  };

  const handleAddSubmit = async (values) => {
    try {
      console.log(values.mode_transport);
      const response = await fetch(`${API_BASE_URL}/admin/emissions?mode_transport=${values.mode_transport}&emission_par_km=${values.emission_par_km}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },

      });
      
      if (!response.ok) throw new Error('Erreur lors de l\'ajout');
      
      message.success('Mode de transport ajouté avec succès');
      setIsModalVisible(false);
      fetchEmissions();
    } catch (error) {
      message.error(error.message);
    }
  };

  const handleEditSubmit = async (values) => {
    try {
      const response = await fetch(`${API_BASE_URL}/admin/emissions/${currentEmission.mode_transport}?new_value=${values.emission_par_km}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ new_value: values.emission_par_km })
      });
      
      if (!response.ok) throw new Error('Erreur lors de la modification');
      
      message.success('Mode de transport modifié avec succès');
      setIsEditModalVisible(false);
      fetchEmissions();
    } catch (error) {
      message.error(error.message);
    }
  };

  const columns = [
    {
      title: 'Mode de transport',
      dataIndex: 'mode_transport',
      key: 'mode_transport',
    },
    {
      title: 'Émission CO2 (kg/km)',
      dataIndex: 'total_emission',
      key: 'total_emission',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <>
          <Button type="link" onClick={() => handleEdit(record)}>
            Modifier
          </Button>
          <Button type="link" danger onClick={() => handleDelete(record.mode_transport)}>
            Supprimer
          </Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Button type="primary" onClick={handleAdd} style={{ marginBottom: 16 }}>
        Ajouter un mode de transport
      </Button>
      
      <Table 
        columns={columns} 
        dataSource={emissions} 
        rowKey="mode_transport" 
      />
      
      {/* Modal pour ajouter */}
      <Modal
        title="Ajouter un mode de transport"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        onOk={() => form.submit()}
        
      >
        <Form form={form} onFinish={handleAddSubmit}>
          <Form.Item
            name="mode_transport"
            label="Mode de transport"
            rules={[{ required: true, message: 'Ce champ est requis' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="emission_par_km"
            label="Émission CO2 (kg/km)"
            rules={[
              { required: true, message: 'Ce champ est requis' },
              { pattern: /^\d*\.?\d+$/, message: 'Doit être un nombre' }
            ]}
          >
            <Input />
          </Form.Item>
        </Form>
      </Modal>
      
      {/* Modal pour modifier */}
      <Modal
        title="Modifier un mode de transport"
        open={isEditModalVisible}
        onCancel={() => setIsEditModalVisible(false)}
        onOk={() => editForm.submit()}
      >
        <Form form={editForm} onFinish={handleEditSubmit}>
          <Form.Item
            name="mode_transport"
            label="Mode de transport"
          >
            <Input disabled />
          </Form.Item>
          <Form.Item
            name="emission_par_km"
            label="Émission CO2 (kg/km)"
            rules={[
              { required: true, message: 'Ce champ est requis' },
              { pattern: /^\d*\.?\d+$/, message: 'Doit être un nombre' }
            ]}
          >
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default EmissionsAdmin;