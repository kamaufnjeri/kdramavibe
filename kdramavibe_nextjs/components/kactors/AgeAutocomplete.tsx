'use client'

import React, { useState } from 'react'

interface AgesAutoCompleteProps {
  selectedAge: string;
  handleChange: (key: string, value: string) => void;
}

const AGES: number[] = Array.from({ length: 123 }, (_, i) => i);


const AgesAutoComplete: React.FC<AgesAutoCompleteProps> = ({ selectedAge, handleChange }) => {
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);

  const filtereAges = AGES.filter((age) => 
    age.toString().includes(selectedAge.toString())
  );



  return (
    <div className='w-full md:w-1/2 lg:w-1/4 relative p-2'>
    <input type="text" name='age' 
placeholder="Type an age..."
  className="
    w-full rounded-xl px-4 py-2
    border-2 border-accent 
    text-pink-200 
    bg-[#1a001f]
  placeholder:text-pink-400
    focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
    hover:border-primary transition-colors duration-200
  "
    value={selectedAge}
    onChange={(e) => {
     handleChange("age", e.target.value);
      setShowSuggestions(true);
    }}
    onFocus={() => setShowSuggestions(true)}
    onBlur={() => setTimeout(() => setShowSuggestions(false),150)}
     /> 
     {showSuggestions && filtereAges.length > 0 && (
      <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-[#1a001f] mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
        {filtereAges.map((age) => (
          <li key={age}
          className='cursor-pointer text-pink-200 hover:text-pink-400'
          onTouchStart={() => {
            handleChange("age", age.toString());
            setShowSuggestions(false);
          }}
          onMouseDown={() => {
            handleChange("age", age.toString());
            setShowSuggestions(false);
          }}
          >{age}</li>
        ))}
      </ul>
     )
     } 
    </div>
  )
}

export default AgesAutoComplete
