import { KactorsFilter, KactorsResponse } from "@/interfaces";
import api from "./apiConfig";
import { AxiosError } from "axios";

export const revalidate = 60 * 60 * 24 * 28; // 4 weeks

const getKactors = async (params: KactorsFilter): Promise<KactorsResponse> => {
  try {
    const res = await api.get<KactorsResponse>("kactors/", { params });
    return res.data; // ✅ Axios automatically throws for non-2xx, so this is safe
  } catch (err) {
    const error = err as AxiosError<{ message: string }>;

    if (error.response) {
      // Server responded with a status outside 2xx
      console.error("Status:", error.response.status);
      console.error("Data:", error.response.data);
      throw new Error(error.response.data?.message || "Error fetching kactors");
    } else if (error.request) {
      // Request was made but no response
      console.error("No response received:", error.message);
      throw new Error("No response from server");
    } else {
      // Something else
      console.error("Axios error:", error.message);
      throw new Error(error.message);
    }
  }
};

export default getKactors;
