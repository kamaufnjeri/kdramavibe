import Banner from "@/components/common/Banner";
import KdramasFilterSection from "@/components/kdramas/KdramasFilterSection";
import KdramasList from "@/components/kdramas/KdramasList";
import { KdramasFilter } from "@/interfaces";
import getKdramas from "@/lib/getKdramas";
import React from "react";

interface PageProps {
  searchParams?: Promise<KdramasFilter>
}


export default async function Home({ searchParams }: PageProps) {
  const { title = '', genre =  '', year = '', ordering = '', page = "1" } = await searchParams ?? {};
  const kdramasResponse = await getKdramas({ title, genre, year, ordering, page });

  return (
    
    <div>
      <Banner/>
     <KdramasFilterSection searchParams={{
      title,
      genre,
      year,
      ordering,
      page
     }}
  
     noOfPages={kdramasResponse.total_pages}
     />
     <KdramasList kdramas={kdramasResponse?.results}/>
    </div>
  );
}
