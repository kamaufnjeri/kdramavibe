import { KactorDetail } from "@/interfaces";
import api from "./apiConfig";
import { AxiosError } from "axios";
import { notFound } from "next/navigation";

/**
 * Revalidation time for cached single K-actor data (in seconds).
 * Currently set to 4 weeks.
 */
export const revalidate = 60 * 60 * 24 * 28; // 4 weeks

/**
 * Fetches the details of a single K-actor by their slug.
 *
 * @param slug - Unique identifier for the K-actor.
 * @returns A promise resolving to the KactorDetail data.
 * @throws Error if the request fails or server responds with an error.
 */
const getSingleKactor = async (slug: string): Promise<KactorDetail> => {
  try {
    const res = await api.get<KactorDetail>(`kactors/${slug}/`);
    return res.data; // ✅ Axios automatically throws for non-2xx, so this is safe
  } catch (err) {
    const error = err as AxiosError<{ message: string }>;

    if (error.response) {
      if (error.response.status === 404) {
        // Trigger Next.js 404 page
        notFound();
      }
      // Server responded with a status outside 2xx
      console.error("Status:", error.response.status);
      console.error("Data:", error.response.data);
      throw new Error(error.response.data?.message || "Error fetching kactor");
    } else if (error.request) {
      // Request was made but no response
      console.error("No response received:", error.message);
      throw new Error("No response from server");
    } else {
      // Something else happened while setting up the request
      console.error("Axios error:", error.message);
      throw new Error(error.message);
    }
  }
};

export default getSingleKactor;

