import { KdramasFilter, KdramasResponse } from "@/interfaces";
import api from "./apiConfig";
import { AxiosError } from "axios";
import { notFound } from "next/navigation";

/**
 * Revalidation time for cached kdramas data (in seconds).
 * Currently set to 4 weeks.
 */
export const revalidate = 60 * 60 * 24 * 28; // 4 weeks

/**
 * Fetches a list of K-dramas from the backend API using provided filter parameters.
 *
 * @param params - Filter parameters for the K-dramas request.
 * @returns A promise resolving to the KdramasResponse data.
 * @throws Error if the request fails or server responds with an error.
 */
const getKdramas = async (params: KdramasFilter): Promise<KdramasResponse> => {
  try {
    const res = await api.get<KdramasResponse>("kdramas/", { params });
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
      throw new Error(error.response.data?.message || "Error fetching kdramas");
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

export default getKdramas;
