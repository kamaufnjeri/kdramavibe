export interface KdramasFilter {
    title: string;
    genre: string;
    year: string;
    ordering: string;
    page: string;

  }

  export interface KactorsFilter {
    name: string;
    age: string;
    gender: string;
    ordering: string;
    page: string;
  }

export interface Kdrama {
    slug: string;
    title: string;
    rating: string | null;
    no_of_votes: string | null;
    start_year: string | null;
    end_year: string | null;
    genres: string[];
    image_url: string | null; 
}

export interface Kactor {
    slug: string;
    name: string;
    age: string | null;
    gender: "female" | "male" | null;
    image_url: string | null; 
    no_of_votes: string | null;
    dramabeans_image_url: string | null;
}

 export interface KdramasResponse {
    total_count: number;
    total_pages: number;
    current_page: number;
    page_size: number;
    next: string | null;
    previous: string | null;
    results: Kdrama[];
  }

   export interface KactorsResponse {
    total_count: number;
    total_pages: number;
    current_page: number;
    page_size: number;
    next: string | null;
    previous: string | null;
    results: Kactor[];
  }

export interface KdramaCasts {
  role_name: string | null;
  kactor_name: string;
  kactor_slug: string;
  kactor_image_url: string | null;
  kactor_gender: "female" | "male";
}

export interface KdramaDetail {
  title: string; // required
  slug: string;  // required
  start_year?: string | null;
  end_year?: string | null;
  rating?: string | null;
  no_of_votes?: string | null;
  plot?: string | null;
  image_url?: string | null;
  wikipedia_url?: string | null;
  episodes?: string | null;
  seasons?: string | null;
  running_time?: string | null;
  country?: string | null;
  dramabeans_url?: string | null;
  writers?: string[] | null;
  directors?: string[] | null;
  languages?: string[] | null;
  networks?: string[] | null;
  alternate_titles?: string[] | null;
  genres?: string[] | null;

  kactors?: KdramaCasts[] | null;
}


export interface KactorDramas {
  kdrama_title: string;
  kdrama_slug: string;
  role_name?: string;
  year?: string | null;
}

export interface KactorDetail {
  name: string;
  alternate_names?: string[];
  description?: string;
  gender?: "male" | "female" | null;
  birthday?: string;
  birthplace?: string;
  age?: number;
  occupations?: string[];
  children?: string[] | number[];
  years_active?: string;
  agents?: string[];
  height?: string;
  partner_or_spouse?: string | null;
  wikipedia_url?: string;
  no_of_votes: string | null;
  dramabeans_image_url: string | null;
  dramabeans_url: string | null;

  image_url?: string;
  slug: string;
  kdramas?: KactorDramas[];
}
