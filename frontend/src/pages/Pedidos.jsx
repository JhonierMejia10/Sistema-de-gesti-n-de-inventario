import React, { useState, useEffect } from 'react';
import api from '../utils/api';
import { Truck, Plus, Edit2, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import Modal from '../components/Modal';

export default function Pedidos() {
    const [data, setData] = useState([]);
    const [ordenes, setOrdenes] = useState([]);
    const [estados, setEstados] = useState([]);
    const [loading, setLoading] = useState(true);

    // Modal state
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [editingItem, setEditingItem] = useState(null);
    const [deletingItem, setDeletingItem] = useState(null);

    // Form state
    const [formData, setFormData] = useState({
        orden: '',
        estado: '',
        direccion_envio: '',
        observaciones: ''
    });

    const fetchData = async () => {
        setLoading(true);
        try {
            const [pedidosRes, ordenesRes, estadosRes] = await Promise.all([
                api.get('/api/v1/pedidos/'),
                api.get('/api/v1/ordenes-de-venta/'),
                api.get('/api/v1/estados-pedido') // Nota: no trae trailing slash en backend
            ]);
            setData(pedidosRes.data.results || pedidosRes.data || []);
            setOrdenes(ordenesRes.data.results || ordenesRes.data || []);
            setEstados(estadosRes.data.results || estadosRes.data || []);
        } catch (error) {
            console.error('Error fetching pedidos u dependencias:', error);
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
        setFormData({
            orden: ordenes.length > 0 ? ordenes[0].id : '',
            estado: estados.length > 0 ? estados[0].id : '',
            direccion_envio: '',
            observaciones: ''
        });
        setIsModalOpen(true);
    };

    const openEditModal = (item) => {
        setEditingItem(item);

        const getId = (val) => (typeof val === 'object' && val !== null ? val.id : (val || ''));

        setFormData({
            orden: getId(item.orden),
            estado: getId(item.estado),
            direccion_envio: item.direccion_envio || '',
            observaciones: item.observaciones || ''
        });
        setIsModalOpen(true);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validaciones requeridas por el modelo
        if (!formData.orden || !formData.estado || !formData.direccion_envio) {
            toast.error('Orden, Estado y Dirección son obligatorios.');
            return;
        }

        try {
            if (editingItem) {
                await api.put(`/api/v1/pedidos/${editingItem.id}/`, formData);
                toast.success('Pedido actualizado con éxito');
            } else {
                await api.post('/api/v1/pedidos/', formData);
                toast.success('Pedido creado con éxito');
            }
            setIsModalOpen(false);
            fetchData();
        } catch (error) {
            console.error('Error al guardar:', error);
            toast.error('Error al guardar el pedido');
        }
    };

    const confirmDelete = async () => {
        if (!deletingItem) return;
        try {
            await api.delete(`/api/v1/pedidos/${deletingItem.id}/`);
            toast.success('Pedido eliminado');
            setIsDeleteModalOpen(false);
            fetchData();
        } catch (error) {
            console.error('Error al eliminar:', error);
            toast.error('Error al eliminar el pedido');
        }
    };

    return (
        <div className="text-white space-y-6 animate-in fade-in duration-500">
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight mb-2">Pedidos (Logística)</h1>
                    <p className="text-[#a1a1aa]">Controla los envíos y su estado logístico.</p>
                </div>
                <button
                    onClick={openAddModal}
                    className="bg-[#10b981] hover:bg-[#059669] text-white px-4 py-2 rounded-lg font-medium subtle-transition flex items-center gap-2"
                >
                    <Plus className="w-4 h-4" strokeWidth={3} />
                    Nuevo Pedido
                </button>
            </div>

            <div className="bg-[var(--color-bg-card)] border border-[var(--color-border-subtle)] rounded-xl overflow-hidden">
                {loading ? (
                    <div className="p-8 text-center text-[#a1a1aa]">Cargando pedidos...</div>
                ) : data.length === 0 ? (
                    <div className="p-8 text-center text-[#a1a1aa]">No hay pedidos en curso.</div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead>
                                <tr className="border-b border-[#27272a] text-[#a1a1aa] font-medium">
                                    <th className="px-6 py-4">ID Pedido</th>
                                    <th className="px-6 py-4">Orden Venta</th>
                                    <th className="px-6 py-4">Dirección</th>
                                    <th className="px-6 py-4">Estado</th>
                                    <th className="px-6 py-4">Fecha</th>
                                    <th className="px-6 py-4 text-center">Acciones</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-[#27272a]">
                                {data.map((item, i) => (
                                    <tr key={item.id || i} className="hover:bg-[#1a1a1a] subtle-transition group">
                                        <td className="px-6 py-4 font-medium text-white flex items-center gap-2">
                                            <Truck className="w-4 h-4 text-[#10b981]" />
                                            #{item.id}
                                        </td>
                                        <td className="px-6 py-4 text-[#a1a1aa]">
                                            {item.orden
                                                ? (typeof item.orden === 'object' ? `Orden #${item.orden.id}` : `Orden #${item.orden}`)
                                                : '-'}
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="text-white max-w-[200px] truncate" title={item.direccion_envio}>
                                                {item.direccion_envio || '-'}
                                            </div>
                                            {item.observaciones && (
                                                <div className="text-[#a1a1aa] text-xs mt-0.5 max-w-[200px] truncate" title={item.observaciones}>
                                                    {item.observaciones}
                                                </div>
                                            )}
                                        </td>
                                        <td className="px-6 py-4 text-[#a1a1aa]">
                                            {item.estado
                                                ? (typeof item.estado === 'object' ? item.estado.nombre : `Estado ${item.estado}`)
                                                : '-'}
                                        </td>
                                        <td className="px-6 py-4 text-[#a1a1aa]">
                                            {item.fecha_creacion ? new Date(item.fecha_creacion).toLocaleDateString() : '-'}
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
                title={editingItem ? "Editar Pedido" : "Nuevo Pedido"}
            >
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-[#a1a1aa] mb-1">Orden de Venta Base</label>
                            <select
                                name="orden"
                                required
                                value={formData.orden}
                                onChange={handleChange}
                                disabled={editingItem !== null} // Generalmente no se cambia la orden una vez creado
                                className="w-full bg-[#1a1a1a] border border-[#27272a] rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#10b981] subtle-transition disabled:opacity-50"
                            >
                                <option value="" disabled>-- Seleccionar Orden --</option>
                                {ordenes.map(o => (
                                    <option key={o.id} value={o.id}>
                                        Orden #{o.id} - ${o.total}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-[#a1a1aa] mb-1">Estado Logístico</label>
                            <select
                                name="estado"
                                required
                                value={formData.estado}
                                onChange={handleChange}
                                className="w-full bg-[#1a1a1a] border border-[#27272a] rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#10b981] subtle-transition"
                            >
                                <option value="" disabled>-- Seleccionar Estado --</option>
                                {estados.map(est => (
                                    <option key={est.id} value={est.id}>{est.nombre}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-[#a1a1aa] mb-1">Dirección de Envío</label>
                        <input
                            type="text"
                            name="direccion_envio"
                            required
                            value={formData.direccion_envio}
                            onChange={handleChange}
                            className="w-full bg-[#1a1a1a] border border-[#27272a] rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#10b981] subtle-transition"
                            placeholder="Ej. Calle 123 #45-67, Ciudad"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-[#a1a1aa] mb-1">Observaciones (Opcional)</label>
                        <textarea
                            name="observaciones"
                            value={formData.observaciones}
                            onChange={handleChange}
                            rows="2"
                            className="w-full bg-[#1a1a1a] border border-[#27272a] rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#10b981] subtle-transition resize-none"
                            placeholder="Instrucciones para el repartidor..."
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
                            {editingItem ? 'Guardar Cambios' : 'Crear Pedido'}
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
                        ¿Estás seguro de que deseas eliminar el pedido logístico <strong className="text-white">#{deletingItem?.id}</strong>? Esta acción no se puede deshacer.
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
