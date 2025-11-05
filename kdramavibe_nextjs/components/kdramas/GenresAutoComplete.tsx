'use client'

import { GENRES_OPTIONS } from '@/constants';
import React, { useEffect, useState } from 'react'

interface GenresAutoCompleteProps {
  selectedGenre: string; // currently selected genre
  handleChange: (key: string, value: string) => void; // handler to update selected genre
}

const GenresAutoComplete: React.FC<GenresAutoCompleteProps> = ({ selectedGenre, handleChange }) => {
  const [inputValue, setInputValue] = useState<string>(selectedGenre); // input field value
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false); // dropdown visibility

  // Filter genres based on input value
  const filtereGenres = GENRES_OPTIONS.filter((genre) => 
    genre.toLowerCase().includes(inputValue.toLowerCase())
  );

  // Update input value when selectedGenre changes from parent
  useEffect(() => {
    setInputValue(selectedGenre);
  }, [selectedGenre])

  return (
    <div className='w-full md:w-1/2 lg:w-1/4 relative p-2'>
      {/* Input field for genre */}
      <input 
        type="text" 
        name='genre' 
        placeholder="Type a genre..."
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
        onBlur={() => setTimeout(() => setShowSuggestions(false),150)} // delay to allow click selection
      /> 

      {/* Dropdown suggestions */}
      {showSuggestions && filtereGenres.length > 0 && (
        <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-[#1a001f] mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
          {filtereGenres.map((genre) => (
            <li 
              key={genre}
              className='cursor-pointer text-pink-200 hover:text-pink-400'
              onTouchStart={() => {
                setInputValue(genre);
                handleChange("genre", genre);
                setShowSuggestions(false);
              }}
              onMouseDown={() => {
                setInputValue(genre);
                handleChange("genre", genre);
                setShowSuggestions(false);
              }}
            >
              {genre}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default GenresAutoComplete
