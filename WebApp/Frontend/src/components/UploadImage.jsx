import React, { useState } from 'react';
import axios from 'axios';

const UploadImage = () => {
  const [file, setFile] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/recommend', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setRecommendations(response.data);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  return (
    <div>
      <h1>Image Similarity Recommendation</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload and Get Recommendations</button>
      </form>
      <div className="recommendations">
        {recommendations.map((rec, index) => (
          <img key={index} src={`http://127.0.0.1:5000/${rec}`} alt="recommendation" />
        ))}
      </div>
    </div>
  );
};

export default UploadImage;
