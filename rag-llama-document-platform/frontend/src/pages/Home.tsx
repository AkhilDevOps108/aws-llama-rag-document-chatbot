import React from 'react';
import Navbar from '../components/Navbar';
import UploadForm from '../components/UploadForm';
import FileList from '../components/FileList';

const Home: React.FC = () => {
  return (
    <div className="home">
      <Navbar />
      <main>
        <UploadForm />
        <FileList />
      </main>
    </div>
  );
};

export default Home;