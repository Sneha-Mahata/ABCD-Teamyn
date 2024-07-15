import Navbar from "./components/Navbar";
import UploadImage from './components/UploadImage';

 const App = () => {
  return (
    <>
      <Navbar />
      <h1>Image Recommender</h1>
      <UploadImage />
    </>
  );
 };

 export default App;