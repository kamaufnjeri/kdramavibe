'use client'

import { GENRES_OPTIONS } from '@/constants';
import React, { useState } from 'react'

interface GenresAutoCompleteProps {
  selectedGenre: string;
  handleChange: (key: string, value: string) => void;
}

const GenresAutoComplete: React.FC<GenresAutoCompleteProps> = ({ selectedGenre, handleChange }) => {
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);

  const filtereGenres = GENRES_OPTIONS.filter((genre) => 
    genre.toLowerCase().includes(selectedGenre.toLowerCase())
  );



  return (
    <div className='w-full md:w-1/2 lg:w-1/4 relative p-2'>
    <input type="text" name='genre' 
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
    value={selectedGenre}
    onChange={(e) => {
     handleChange("genre", e.target.value);
      setShowSuggestions(true);
    }}
    onFocus={() => setShowSuggestions(true)}
    onBlur={() => setTimeout(() => setShowSuggestions(false),150)}
     /> 
     {showSuggestions && filtereGenres.length > 0 && (
      <ul className='absolute hover:ring-1 hover:ring-primary hover:outline-none hover:border-primary bg-[#1a001f] mt-2 border-2 border-accent rounded-xl px-4 py-2 z-10 w-full max-h-50 overflow-y-auto custom-scrollbar'>
        {filtereGenres.map((genre) => (
          <li key={genre}
          className='cursor-pointer text-pink-200 hover:text-pink-400'
          onTouchStart={() => {
            handleChange("genre", genre);
            setShowSuggestions(false);
          }}
          onMouseDown={() => {
            handleChange("genre", genre);
            setShowSuggestions(false);
          }}
          >{genre}</li>
        ))}
      </ul>
     )
     } 
    </div>
  )
}

export default GenresAutoComplete
