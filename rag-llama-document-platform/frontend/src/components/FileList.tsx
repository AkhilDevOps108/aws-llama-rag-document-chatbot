import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface FileItem {
  name: string;
  size: number;
  uploaded_at: string;
}

const FileList: React.FC = () => {
  const [files, setFiles] = useState<FileItem[]>([]);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axios.get<FileItem[]>('http://localhost:8000/files');
        setFiles(response.data);
      } catch (error) {
        console.error('Error fetching files:', error);
      }
    };

    fetchFiles();
  }, []);

  return (
    <div className="file-list">
      <h2>Uploaded Documents</h2>
      <table>
        <thead>
          <tr>
            <th>File Name</th>
            <th>Size (bytes)</th>
            <th>Uploaded At</th>
          </tr>
        </thead>
        <tbody>
          {files.map((file, index) => (
            <tr key={index}>
              <td>{file.name}</td>
              <td>{file.size}</td>
              <td>{file.uploaded_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FileList;