'use client'

import { GENDER_OPTIONS } from '@/constants';
import React, { useState } from 'react'

interface GendersSelectProps {
  selectedGender: string;
  handleChange: (key: string, value: string) => void;
}

const GendersSelect: React.FC<GendersSelectProps> = ({ selectedGender, handleChange }) => {
  const [showDropdown, setShowDropdown] = useState<boolean>(false); // Track dropdown visibility

  return (
    <div className='w-full md:w-1/2 lg:w-1/4 relative p-2'>
      {/* Input field for gender selection */}
      <input 
        type="text" 
        name='gender' 
        placeholder="Select gender..."
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
        value={selectedGender}
        onFocus={() => setShowDropdown(true)} // Show dropdown when focused
        onBlur={() => setTimeout(() => setShowDropdown(false),150)} // Hide dropdown after blur with delay for click selection
      /> 

      {/* Dropdown list of gender options */}
      {showDropdown && GENDER_OPTIONS && (
        <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-input-bg mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
          {GENDER_OPTIONS.map((gender) => (
            <li 
              key={gender.name}
              className='cursor-pointer text-input-text hover:text-pink-500'
              onTouchStart={() => {
                handleChange("gender", gender.value); // Update selected gender on touch
                setShowDropdown(false); // Close dropdown
              }}
              onMouseDown={() => {
                handleChange("gender", gender.value); // Update selected gender on click
                setShowDropdown(false); // Close dropdown
              }}
            >
              {gender.name}
            </li>
          ))}
        </ul>
      )} 
    </div>
  )
}

export default GendersSelect;
