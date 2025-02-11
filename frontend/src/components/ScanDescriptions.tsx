import { useState, useEffect, useCallback } from "react";
import { useParams } from "react-router-dom";
import { api } from "../services/api";

export default function ScanDescriptions() {
    const { id } = useParams<{ id: string }>();
    const { scanid } = useParams<{ scanid: string }>();
    const [scanDescriptions, setScanDescriptions] = useState<any | null>(null);
    const [loading, setLoading] = useState(true);
    
    const loadScanDescriptions = useCallback(async () => {
        if (!id || !scanid) return;

        try {
            const scanDescriptionsRes = await api.getScanDescriptions(parseInt(scanid as string), parseInt(id));
            setScanDescriptions(scanDescriptionsRes.data);
        } catch (error) {
            console.error("Error loading scan descriptions:", error);
        } finally {
            setLoading(false);
        }
    }, [id]);

    useEffect(() => {
        loadScanDescriptions();
    }, [loadScanDescriptions]);


    if (!scanDescriptions) {
        return <div className="alert alerte-error">Scan Description not found</div>;
    }

    if (loading) {
        return <div></div>;
    }

    return (
        <div className="card bg-base-100 shadow-x1">
            <div className="card-body">
                <div className="grid grid-cols-2 gap-4"> 
                    <div>
                        <p>
                            <strong>Catgory: </strong> {scanDescriptions.category}
                        </p>
                        <p>
                            <strong>Short Description: </strong> {scanDescriptions.shortdescription}
                        </p>
                    </div>
                </div>    
            </div>
        </div>
    )
}