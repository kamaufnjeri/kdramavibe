'use client'

import { GENDER_OPTIONS } from '@/constants';
import React, { useState } from 'react'

interface GendersSelectProps {
  selectedGender: string;
  handleChange: (key: string, value: string) => void;
}

const GendersSelect: React.FC<GendersSelectProps> = ({ selectedGender, handleChange }) => {
  const [showDropdown, setShowDropdown] = useState<boolean>(false);

  
  return (
    <div className='w-full md:w-1/2 lg:w-1/4 relative p-2'>
    <input type="text" name='gender' 
placeholder="Select gender..."
readOnly
  className="
    w-full rounded-xl px-4 py-2
    border-2 border-accent 
    text-pink-200 
    bg-[#1a001f]
  placeholder:text-pink-400
    focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
    hover:border-primary transition-colors duration-200
  "
    value={selectedGender}
    
    onFocus={() => setShowDropdown(true)}
    onBlur={() => setTimeout(() => setShowDropdown(false),150)}
     /> 
     {showDropdown && GENDER_OPTIONS && (
      <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-[#1a001f] mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
        {GENDER_OPTIONS.map((gender) => (
          <li key={gender.name}
          className='cursor-pointer text-pink-200 hover:text-pink-400'
          onTouchStart={() => {
            handleChange("gender", gender.value);
            setShowDropdown(false);
          }}
          onMouseDown={() => {
            handleChange("gender", gender.value);
            setShowDropdown(false);
          }}
          >{gender.name}</li>
        ))}
      </ul>
     )
     } 
    </div>
  )
}

export default GendersSelect;
