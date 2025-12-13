'use client'

import { KACTOR_ORDERBY_OPTIONS } from '@/constants';
import React, { useState } from 'react'

interface OrderByOptionsProps {
  selectedOrderBy: string; // currently selected ordering value
  handleChange: (key: string, value: string) => void; // handler to update ordering
}

// Component to select ordering for Kactors (e.g., by name, age, popularity)
const OrderByOptions: React.FC<OrderByOptionsProps> = ({ selectedOrderBy, handleChange }) => {
  const [showDropdown, setShowDropdown] = useState<boolean>(false); // state to control dropdown visibility

  return (
    <div className='px-2 flex flex-wrap gap-3 items-center'>
      {/* Label for the dropdown */}
      <label htmlFor='ordering' className='font-semibold text-primary'>Order By</label>

      <div className='relative'>
        {/* Read-only input to display current selection */}
        <input
          type="text"
          name='ordering'
          placeholder="Order By..."
          readOnly
          className="
            w-full rounded-xl px-4 py-2
            border-2 border-accent 
            text-input-text
          bg-input-bg
          placeholder:text-pink-500
            focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
            hover:border-primary transition-colors duration-200
          "
          value={KACTOR_ORDERBY_OPTIONS.find(opt => opt.value === selectedOrderBy)?.name || ""}
          onFocus={() => setShowDropdown(true)} // show dropdown on focus
          onBlur={() => setTimeout(() => setShowDropdown(false), 150)} // hide dropdown on blur with slight delay
        />

        {/* Dropdown list */}
        {showDropdown && KACTOR_ORDERBY_OPTIONS && (
          <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-input-bg mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
            {KACTOR_ORDERBY_OPTIONS.map((orderBy) => (
              <li
                key={orderBy.name}
                className='cursor-pointer text-input-text hover:text-pink-500'
                onTouchStart={() => {
                  handleChange("ordering", orderBy.value); // update ordering on touch
                  setShowDropdown(false); // close dropdown
                }}
                onMouseDown={() => {
                  handleChange("ordering", orderBy.value); // update ordering on click
                  setShowDropdown(false); // close dropdown
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

export default OrderByOptions;
