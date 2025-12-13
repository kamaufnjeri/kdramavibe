'use client'

import { ORDERBY_OPTIONS } from '@/constants';
import React, { useState } from 'react'

interface OrderByOptionsProps {
  selectedOrderBy: string; // Currently selected ordering value
  handleChange: (key: string, value: string) => void; // Callback when selection changes
}

const OrderByOptions: React.FC<OrderByOptionsProps> = ({ selectedOrderBy, handleChange }) => {
  const [showDropdown, setShowDropdown] = useState<boolean>(false); // Dropdown visibility state

  return (
    <div className='px-2 flex flex-wrap gap-3 items-center'>
      {/* Label for the input */}
      <label htmlFor='ordering' className='font-semibold text-primary'>Order By</label>

      <div className='relative'>
        {/* Read-only input to display selected option */}
        <input
          type="text"
          name='ordering'
          placeholder="Order By..."
          readOnly
          value={ORDERBY_OPTIONS.find(opt => opt.value === selectedOrderBy)?.name || ""}
          className="
            w-full rounded-xl px-4 py-2
            border-2 border-accent 
            text-input-text
          bg-input-bg
          placeholder:text-pink-500
            focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
            hover:border-primary transition-colors duration-200
          "
          onFocus={() => setShowDropdown(true)} // Show dropdown on focus
          onBlur={() => setTimeout(() => setShowDropdown(false), 150)} // Hide dropdown on blur
        />

        {/* Dropdown list */}
        {showDropdown && ORDERBY_OPTIONS && (
          <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-input-bg mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
            {ORDERBY_OPTIONS.map((orderBy) => (
              <li
                key={orderBy.name} // Unique key
                className='cursor-pointer text-input-text hover:text-pink-500'
                onTouchStart={() => {
                  handleChange("ordering", orderBy.value); // Update selected ordering
                  setShowDropdown(false); // Close dropdown
                }}
                onMouseDown={() => {
                  handleChange("ordering", orderBy.value);
                  setShowDropdown(false);
                }}
              >
                {orderBy.name}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default OrderByOptions
