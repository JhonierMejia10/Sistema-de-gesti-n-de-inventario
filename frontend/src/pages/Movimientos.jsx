import React, { useState, useEffect } from 'react';
import { MoreHorizontal, Plus, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import api from '../utils/api';

export default function Movimientos() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.get('/api/v1/movimientos/');
                setData(response.data.results || response.data || []);
            } catch (error) {
                console.error('Error fetching movimientos:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="text-white space-y-6 animate-in fade-in duration-500">
            <div className="mb-6">
                <h1 className="text-3xl font-bold tracking-tight mb-2">Movimientos</h1>
                <p className="text-[#a1a1aa]">Registro histórico de entradas y salidas</p>
            </div>

            <div className="bg-[var(--color-bg-card)] border border-[var(--color-border-subtle)] rounded-xl overflow-hidden">
                {loading ? (
                    <div className="p-8 text-center text-[#a1a1aa]">Cargando historial...</div>
                ) : data.length === 0 ? (
                    <div className="p-8 text-center text-[#a1a1aa]">No hay movimientos registrados.</div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead>
                                <tr className="border-b border-[#27272a] text-[#a1a1aa] font-medium">
                                    <th className="px-6 py-4">ID / Referencia</th>
                                    <th className="px-6 py-4">Fecha</th>
                                    <th className="px-6 py-4">Tipo</th>
                                    <th className="px-6 py-4">Producto</th>
                                    <th className="px-6 py-4 text-right">Cantidad</th>
                                    <th className="px-6 py-4 text-center">Usuario</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-[#27272a]">
                                {data.map((mov, i) => {
                                    const isEntrada = mov.tipo_movimiento === 'ENTRADA' || mov.type === 'IN';
                                    return (
                                        <tr key={i} className="hover:bg-[#1a1a1a] subtle-transition">
                                            <td className="px-6 py-4 font-semibold text-[#10b981] whitespace-nowrap">{mov.referencia || mov.id}</td>
                                            <td className="px-6 py-4 text-[#a1a1aa] font-medium">{mov.fecha || mov.date || '-'}</td>
                                            <td className="px-6 py-4">
                                                <div className={`flex items-center gap-1.5 px-2 py-1 rounded inline-flex text-xs font-medium border ${isEntrada
                                                    ? 'text-[#10b981] border-[#10b981]/30 bg-[#10b981]/10'
                                                    : 'text-[#ef4444] border-[#ef4444]/30 bg-[#ef4444]/10'
                                                    }`}>
                                                    {isEntrada ? <ArrowDownRight className="w-3.5 h-3.5" /> : <ArrowUpRight className="w-3.5 h-3.5" />}
                                                    {mov.tipo_movimiento || mov.type || 'MOVIMIENTO'}
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 font-medium">{mov.producto || mov.product || '-'}</td>
                                            <td className="px-6 py-4 font-bold text-right text-white">
                                                {isEntrada ? '+' : '-'}{mov.cantidad || mov.quantity || '0'}
                                            </td>
                                            <td className="px-6 py-4 text-center text-[#a1a1aa]">{mov.usuario || mov.user || '-'}</td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
