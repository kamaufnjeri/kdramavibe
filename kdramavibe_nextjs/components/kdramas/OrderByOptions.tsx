'use client'

import { ORDERBY_OPTIONS } from '@/constants';
import React, { useState } from 'react'


interface OrderByOptionsProps {
  selectedOrderBy: string;
  handleChange: (key: string, value: string) => void;
}

const OrderByOptions: React.FC<OrderByOptionsProps> = ({ selectedOrderBy, handleChange }) => {
  const [showDropdown, setShowDropdown] = useState<boolean>(false);

  
  return (
    <div className='px-2 flex flex-wrap gap-3 items-center'>
            <label htmlFor='ordering' className='font-semibold text-primary'>Order By</label>

    <div className='relative '>
    <input type="text" name='ordering' 
placeholder="Order By..."
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
value={ORDERBY_OPTIONS.find(opt => opt.value === selectedOrderBy)?.name || ""}
    
    onFocus={() => setShowDropdown(true)}
    onBlur={() => setTimeout(() => setShowDropdown(false),150)}
     /> 
     {showDropdown && ORDERBY_OPTIONS && (
      <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-[#1a001f] mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
        {ORDERBY_OPTIONS.map((orderBy) => (
          <li key={orderBy.name}
          className='cursor-pointer text-pink-200 hover:text-pink-400'
          onTouchStart={() => {
            handleChange("ordering", orderBy.value);
            setShowDropdown(false);
          }}
          onMouseDown={() => {
            handleChange("ordering", orderBy.value);
            setShowDropdown(false);
          }}
          >{orderBy.name}</li>
        ))}
      </ul>
     )
     } 
    </div>
        </div>

  )
}

export default OrderByOptions;
