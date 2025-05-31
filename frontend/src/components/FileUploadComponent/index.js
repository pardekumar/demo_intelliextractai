// FileUploadComponent.js
import React from "react";

const FileUploadComponent = ({ onFileUpload }) => {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    console.log();
    onFileUpload(file);
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
    </div>
  );
};

export default FileUploadComponent;
