import React from 'react';
import { FaTimes } from 'react-icons/fa';

interface PillProps {
  fieldKey: string;  // The name of the filter field (renamed from 'key' to avoid React key conflicts)
  value: string;      // The current value of the filter field
  resetFilterField: (key: string, value: string) => void; // Function to reset the field
}

const Pill: React.FC<PillProps> = ({ fieldKey, value, resetFilterField }) => {
  return (
    <>
      {/* Only render the pill if there is a value */}
      {value && (
        <span className="rounded-lg p-1 bg-primary flex flex-row gap-2">
          {/* Display the value of the filter */}
          <p>{value}</p>

          {/* Button to clear the filter field */}
          <button onClick={() => resetFilterField(fieldKey, '')} className='cursor-pointer'>
            <FaTimes />
          </button>
        </span>
      )}
    </>
  );
};

export default Pill;
