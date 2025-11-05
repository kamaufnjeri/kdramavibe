'use client'

import React, { useEffect, useState } from 'react'

interface AgesAutoCompleteProps {
  selectedAge: string;
  handleChange: (key: string, value: string) => void;
}

// Create an array of ages from 0 to 122
const AGES: number[] = Array.from({ length: 123 }, (_, i) => i);

const AgesAutoComplete: React.FC<AgesAutoCompleteProps> = ({ selectedAge, handleChange }) => {
  // State for the input field value
  const [inputValue, setInputValue] = useState<string>(selectedAge);
  // State to show/hide suggestions dropdown
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);

  // Filter ages based on the input value
  const filtereAges = AGES.filter((age) => 
    age.toString().includes(inputValue.toString())
  );

  // Update input value when selectedAge prop changes
  useEffect(() => {
    setInputValue(selectedAge);
  }, [selectedAge]);

  return (
    <div className='w-full md:w-1/2 lg:w-1/4 relative p-2'>
      {/* Age input field */}
      <input
        type="text"
        name='age'
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
        value={inputValue}
        onChange={(e) => {
          setInputValue(e.target.value);
          setShowSuggestions(true);
        }}
        onFocus={() => setShowSuggestions(true)}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
      /> 

      {/* Suggestions dropdown */}
      {showSuggestions && filtereAges.length > 0 && (
        <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-[#1a001f] mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
          {filtereAges.map((age) => (
            <li
              key={age}
              className='cursor-pointer text-pink-200 hover:text-pink-400'
              onTouchStart={() => {
                setInputValue(age.toString());
                handleChange("age", age.toString());
                setShowSuggestions(false);
              }}
              onMouseDown={() => {
                setInputValue(age.toString());
                handleChange("age", age.toString());
                setShowSuggestions(false);
              }}
            >
              {age}
            </li>
          ))}
        </ul>
      )} 
    </div>
  )
}

export default AgesAutoComplete
