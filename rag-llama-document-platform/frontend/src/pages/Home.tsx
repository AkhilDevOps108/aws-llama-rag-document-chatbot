import React from 'react';
import Navbar from '../components/Navbar';
import UploadForm from '../components/UploadForm';
import FileList from '../components/FileList';
import ChatInterface from '../components/ChatInterface';

const Home: React.FC = () => {
  return (
    <div className="home">
      <Navbar />
      <main>
        <UploadForm />
        <FileList />
        <ChatInterface />
      </main>
    </div>
  );
};

export default Home;
