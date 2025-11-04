import React from 'react';
import { FaTimes } from 'react-icons/fa';

interface PillProps {
    fieldKey: string;  // renamed from 'key'
    value: string;
    resetFilterField: (key: string, value: string) => void;
}

const Pill: React.FC<PillProps> = ({ fieldKey, value, resetFilterField }) => {
    return (
        <>
            {value && (
                <span className="rounded-lg p-1 bg-primary flex flex-row gap-2">
                    <p>{value}</p>
                    <button onClick={() => resetFilterField(fieldKey, '')}>
                        <FaTimes />
                    </button>
                </span>
            )}
        </>
    );
}

export default Pill;
