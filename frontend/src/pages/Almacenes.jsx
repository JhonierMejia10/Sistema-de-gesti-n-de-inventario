import React, { useState, useEffect } from 'react';
import api from '../utils/api';
import { Package, Plus, Edit2, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import Modal from '../components/Modal';

export default function Almacenes() {
    const [data, setData] = useState([]);
    const [ubicaciones, setUbicaciones] = useState([]);
    const [loading, setLoading] = useState(true);

    // Modal state
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [editingItem, setEditingItem] = useState(null);
    const [deletingItem, setDeletingItem] = useState(null);

    // Form state
    const [formData, setFormData] = useState({
        nombre: '',
        descripcion: '',
        ubicacion: '' // ID de la ubicación
    });

    const fetchData = async () => {
        setLoading(true);
        try {
            const [almacenesRes, ubicacionesRes] = await Promise.all([
                api.get('/api/v1/almacenes/'),
                api.get('/api/v1/ubicaciones/')
            ]);
            setData(almacenesRes.data.results || almacenesRes.data || []);
            setUbicaciones(ubicacionesRes.data.results || ubicacionesRes.data || []);
        } catch (error) {
            console.error('Error fetching almacenes or ubicaciones:', error);
            toast.error('Error al cargar datos');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const openAddModal = () => {
        setEditingItem(null);
        setFormData({ nombre: '', descripcion: '', ubicacion: '' });
        setIsModalOpen(true);
    };

    const openEditModal = (item) => {
        setEditingItem(item);
        // Si ubicacion es un objeto, tomamos su id
        const ubicacionId = typeof item.ubicacion === 'object' && item.ubicacion !== null
            ? item.ubicacion.id
            : (item.ubicacion || '');

        setFormData({
            nombre: item.nombre,
            descripcion: item.descripcion || '',
            ubicacion: ubicacionId
        });
        setIsModalOpen(true);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Formatear payload para Django
        const payload = {
            nombre: formData.nombre,
            descripcion: formData.descripcion,
        };
        if (formData.ubicacion) payload.ubicacion = formData.ubicacion;

        try {
            if (editingItem) {
                await api.put(`/api/v1/almacenes/${editingItem.id}/`, payload);
                toast.success('Almacén actualizado con éxito');
            } else {
                await api.post('/api/v1/almacenes/', payload);
                toast.success('Almacén creado con éxito');
            }
            setIsModalOpen(false);
            fetchData();
        } catch (error) {
            console.error('Error al guardar:', error);
            toast.error('Error al guardar el almacén');
        }
    };

    const confirmDelete = async () => {
        if (!deletingItem) return;
        try {
            await api.delete(`/api/v1/almacenes/${deletingItem.id}/`);
            toast.success('Almacén eliminado');
            setIsDeleteModalOpen(false);
            fetchData();
        } catch (error) {
            console.error('Error al eliminar:', error);
            toast.error('Error al eliminar el almacén');
        }
    };

    return (
        <div className="text-white space-y-6 animate-in fade-in duration-500">
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight mb-2">Almacenes</h1>
                    <p className="text-[#a1a1aa]">Gestiona los centros de distribución y bodegas.</p>
                </div>
                <button
                    onClick={openAddModal}
                    className="bg-[#10b981] hover:bg-[#059669] text-white px-4 py-2 rounded-lg font-medium subtle-transition flex items-center gap-2"
                >
                    <Plus className="w-4 h-4" strokeWidth={3} />
                    Nuevo Almacén
                </button>
            </div>

            <div className="bg-[var(--color-bg-card)] border border-[var(--color-border-subtle)] rounded-xl overflow-hidden">
                {loading ? (
                    <div className="p-8 text-center text-[#a1a1aa]">Cargando datos...</div>
                ) : data.length === 0 ? (
                    <div className="p-8 text-center text-[#a1a1aa]">No hay almacenes registrados.</div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead>
                                <tr className="border-b border-[#27272a] text-[#a1a1aa] font-medium">
                                    <th className="px-6 py-4">ID</th>
                                    <th className="px-6 py-4">Nombre</th>
                                    <th className="px-6 py-4">Ubicación</th>
                                    <th className="px-6 py-4 text-center">Acciones</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-[#27272a]">
                                {data.map((item, i) => (
                                    <tr key={item.id || i} className="hover:bg-[#1a1a1a] subtle-transition group">
                                        <td className="px-6 py-4 font-medium text-[#a1a1aa]">{item.id}</td>
                                        <td className="px-6 py-4 font-semibold text-white">{item.nombre || item.name}</td>
                                        <td className="px-6 py-4 text-[#a1a1aa]">
                                            {item.ubicacion
                                                ? (typeof item.ubicacion === 'object'
                                                    ? `${item.ubicacion.barrio ? item.ubicacion.barrio + ', ' : ''}${item.ubicacion.ciudad || ''}, ${item.ubicacion.pais || ''}`
                                                    : item.ubicacion)
                                                : (item.location || '-')}
                                        </td>
                                        <td className="px-6 py-4 text-center">
                                            <div className="flex justify-center items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                                <button
                                                    onClick={() => openEditModal(item)}
                                                    className="p-1.5 text-[#a1a1aa] hover:text-[#10b981] hover:bg-[#10b981]/10 rounded-md subtle-transition"
                                                    title="Editar"
                                                >
                                                    <Edit2 className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={() => { setDeletingItem(item); setIsDeleteModalOpen(true); }}
                                                    className="p-1.5 text-[#a1a1aa] hover:text-[#ef4444] hover:bg-[#ef4444]/10 rounded-md subtle-transition"
                                                    title="Eliminar"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Create / Edit Modal */}
            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={editingItem ? "Editar Almacén" : "Nuevo Almacén"}
            >
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-[#a1a1aa] mb-1">Nombre</label>
                        <input
                            type="text"
                            name="nombre"
                            required
                            value={formData.nombre}
                            onChange={handleChange}
                            className="w-full bg-[#1a1a1a] border border-[#27272a] rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#10b981] subtle-transition"
                            placeholder="Ej. Bodega Principal Sur"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-[#a1a1aa] mb-1">Ubicación</label>
                        <select
                            name="ubicacion"
                            value={formData.ubicacion}
                            onChange={handleChange}
                            className="w-full bg-[#1a1a1a] border border-[#27272a] rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#10b981] subtle-transition"
                        >
                            <option value="">-- Sin ubicación asignada --</option>
                            {ubicaciones.map(ubi => (
                                <option key={ubi.id} value={ubi.id}>
                                    {ubi.ciudad} {ubi.barrio ? `- ${ubi.barrio}` : ''} ({ubi.pais})
                                </option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-[#a1a1aa] mb-1">Descripción</label>
                        <textarea
                            name="descripcion"
                            value={formData.descripcion}
                            onChange={handleChange}
                            rows="3"
                            className="w-full bg-[#1a1a1a] border border-[#27272a] rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#10b981] subtle-transition resize-none"
                            placeholder="Detalles sobre este almacén..."
                        ></textarea>
                    </div>
                    <div className="pt-4 flex justify-end gap-3 border-t border-[#27272a]">
                        <button
                            type="button"
                            onClick={() => setIsModalOpen(false)}
                            className="px-4 py-2 text-sm font-medium text-white bg-[#27272a] hover:bg-[#3f3f46] rounded-lg subtle-transition"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className="px-4 py-2 text-sm font-medium text-white bg-[#10b981] hover:bg-[#059669] rounded-lg subtle-transition"
                        >
                            {editingItem ? 'Guardar Cambios' : 'Crear Almacén'}
                        </button>
                    </div>
                </form>
            </Modal>

            {/* Delete Confirmation Modal */}
            <Modal
                isOpen={isDeleteModalOpen}
                onClose={() => setIsDeleteModalOpen(false)}
                title="Confirmar Eliminación"
            >
                <div className="space-y-4">
                    <p className="text-[#a1a1aa]">
                        ¿Estás seguro de que deseas eliminar el almacén <strong className="text-white">{deletingItem?.nombre}</strong>?
                        Si hay productos enlazados a este almacén, esta acción podría fallar o desencadenar borrados en cascada según las políticas de tu base de datos.
                    </p>
                    <div className="pt-4 flex justify-end gap-3 border-t border-[#27272a]">
                        <button
                            type="button"
                            onClick={() => setIsDeleteModalOpen(false)}
                            className="px-4 py-2 text-sm font-medium text-white bg-[#27272a] hover:bg-[#3f3f46] rounded-lg subtle-transition"
                        >
                            Cancelar
                        </button>
                        <button
                            onClick={confirmDelete}
                            className="px-4 py-2 text-sm font-medium text-white bg-[#ef4444] hover:bg-[#b91c1c] rounded-lg subtle-transition"
                        >
                            Eliminar
                        </button>
                    </div>
                </div>
            </Modal>
        </div>
    );
}
