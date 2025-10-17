'use client'

import React, { useState } from 'react'

const YEARS: string[] = Array.from(
  { length: 51 },
  (_, i) => (new Date().getFullYear() - i).toString()
);

interface YearsSelectProps {
  selectedYear: string;
  handleChange: (key: string, value: string) => void;
}

const YearsSelect: React.FC<YearsSelectProps> = ({ selectedYear, handleChange }) => {
  const [showDropdown, setShowDropdown] = useState<boolean>(false);

  
  return (
    <div className='w-full md:w-1/2 lg:w-1/4 relative p-2'>
    <input type="text" name='year' 
placeholder="Select year..."
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
    value={selectedYear}
    
    onFocus={() => setShowDropdown(true)}
    onBlur={() => setTimeout(() => setShowDropdown(false),150)}
     /> 
     {showDropdown && YEARS && (
      <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-[#1a001f] mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
        {YEARS.map((year) => (
          <li key={year}
          className='cursor-pointer text-pink-200 hover:text-pink-400'
          onTouchStart={() => {
            handleChange("year", year);
            setShowDropdown(false);
          }}
          onMouseDown={() => {
            handleChange("year", year);
            setShowDropdown(false);
          }}
          >{year}</li>
        ))}
      </ul>
     )
     } 
    </div>
  )
}

export default YearsSelect;
