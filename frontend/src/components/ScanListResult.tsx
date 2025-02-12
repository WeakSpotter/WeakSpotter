import { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import { api } from "../services/api";

export default function ScanResult() {
    const { id } = useParams<{ id: string }>();
    const { scanid } = useParams<{ scanid: string }>();
    const [scanResult, setScanResult] = useState<any | null>(null);
    const [loading, setLoading] = useState(true);
    
    const loadScanResult = useCallback(async () => {
        if (!id || !scanid) return;

        try {
            const scanResultRes = await api.getScanResult(parseInt(id));
            setScanResult(scanResultRes.data);
        } catch (error) {
            console.error("Error loading scan descriptions:", error);
        } finally {
            setLoading(false);
        }
    }, [id]);

    useEffect(() => {
        loadScanResult();
    }, [loadScanResult]);


    if (!scanResult) {
        return <div className="alert alerte-error">Scan Description not found</div>;
    }

    if (loading) {
        return <div></div>;
    }

    return (
        <>
        </>
    )
}