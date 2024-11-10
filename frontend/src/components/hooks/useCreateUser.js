import { useState } from "react";
import axios from "axios";
import Swal from "sweetalert2";
import { API_URL } from "../../constants";
import { useNavigate } from 'react-router-dom';


const useCreateUser = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const createUser = async (name, password) => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/api/users`, {
        username: name,
        password: password
      });

      // Success case
      Swal.fire({
        icon: "success",
        title: "Success",
        text: response.data.message + ", logging in..",
        position: "top-end",
        toast: true,
        timer: 2000,
        showConfirmButton: false,
      });

      // localStorage.setItem('userId', response.data.user_id);
      
      navigate('/chat/' + response.data.user_id);
      return response.data;

    } catch (err) {
      // Determine the error message based on the error type
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message ||
                          (err.request ? "Network error. Please check your connection." : "An error occurred while creating the user");
      
      setError(errorMessage);
      
      Swal.fire({
        icon: "error",
        title: "Error",
        text: errorMessage,
        position: "top-end",
        toast: true,
        timer: 3000,
      });

      return null;

    } finally {
      setLoading(false);
    }
  };

  return { createUser, loading, error };
};

export default useCreateUser;
