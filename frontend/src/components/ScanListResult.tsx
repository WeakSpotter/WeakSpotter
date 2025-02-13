interface ScanListResultProps {
    scan: any; 
}

export default function ScanListResult({scan}: ScanListResultProps) {
    

    if (!scan) {
        return <div className="alert alerte-error">Scan Description not found</div>;
    }

    return (
        <>
    <div className="card bg-base-100 shadow-xl mt-5">
        <div className="card-body">
            <div className="flex justify-between items-center">
                <h2 className="card-title"> Title </h2>
                <h4>score</h4>
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div>
                    <p>
                        short description
                    </p>
                </div>
            </div>

        <div className="card-actions justify-end">
            <button
                    className="btn btn-primary"
                    onClick={() => {
                        // handleScan(scan.id);
                    }}
                >
                    More details
                </button>
            </div>
        </div>
    </div>
    </>
    )
}