import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

export const uploadAndCompare = async (fileA, fileB, sensitivity = 50) => {
  const formData = new FormData();
  formData.append('image_a', fileA);
  formData.append('image_b', fileB);
  formData.append('sensitivity', sensitivity);

  const response = await api.post('/api/compare', formData);

  return response.data;
};
