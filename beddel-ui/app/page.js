"use client";

import { useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";

export default function Home() {
  const [files, setFiles] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [download, setDownload] = useState({ url: null, filename: null, size: 0 });
  const [error, setError] = useState("");

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [],
    },
    onDrop: acceptedFiles => setFiles(acceptedFiles),
    multiple: true,
  });

  // cleanup object URL when component unmounts or new download arrives
  useEffect(() => {
    return () => {
      if (download.url) URL.revokeObjectURL(download.url);
    };
  }, [download.url]);

  function filenameFromDisposition(disposition) {
    if (!disposition) return null;
    // RFC 5987: filename*=UTF-8''encoded
    const star = disposition.match(/filename\*\s*=\s*UTF-8''([^;]+)/i);
    if (star && star[1]) {
      try { return decodeURIComponent(star[1]); } catch { return star[1]; }
    }
    // Basic: filename="name" or filename=name
    const basic = disposition.match(/filename\s*=\s*"?([^"]+)"?/i);
    if (basic && basic[1]) return basic[1];
    return null;
  }

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError("");
    setDownload({ url: null, filename: null, size: 0 });

    try {
      const formData = new FormData();
      formData.append("user_prompt", prompt);
      files.forEach(file => formData.append("files", file));

      const res = await fetch("http://localhost:8000/process", {
        method: "POST",
        body: formData,
      });

      const contentType = (res.headers.get("Content-Type") || "").toLowerCase();
      const dispo = res.headers.get("Content-Disposition") || "";

      // Try to read error payloads neatly
      if (!res.ok) {
        if (contentType.includes("application/json")) {
          const j = await res.json().catch(() => ({}));
          throw new Error(j?.error || `Server error (${res.status})`);
        } else {
          const txt = await res.text().catch(() => "");
          throw new Error(txt || `Server error (${res.status})`);
        }
      }

      // pick a sensible filename
      let filename = filenameFromDisposition(dispo);
      if (!filename) {
        if (contentType.includes("application/zip")) filename = "processed_files.zip";
        else if (contentType.includes("application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
          filename = "processed.docx";
        else filename = "download.bin"; // last resort
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setDownload({ url, filename, size: blob.size });

      // optional: auto-trigger download
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (e) {
      console.error(e);
      setError(e.message || "Something went wrong while processing your files.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="p-8 max-w-xl mx-auto text-center space-y-4">
      <h1 className="text-3xl font-bold">Beddel</h1>

      <textarea
        placeholder="Please describe your changes here"
        className="border rounded w-full p-2"
        rows={4}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <div
        {...getRootProps()}
        className="border-dashed border-2 rounded p-8 cursor-pointer"
      >
        <input {...getInputProps()} />
        <p>Drag and drop .docx files here, or click to browse</p>
      </div>

      <div className="space-y-2">
        {files.map((f) => (
          <div key={f.name} className="text-sm">{f.name}</div>
        ))}
      </div>

      <button
        onClick={handleSubmit}
        disabled={isSubmitting || files.length === 0 || !prompt.trim()}
        className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-60"
      >
        {isSubmitting ? "Processing..." : "Submit"}
      </button>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      {download.url && (
        <div className="mt-4">
          <a
            href={download.url}
            download={download.filename || "download"}
            className="text-blue-600 underline"
          >
            Download: {download.filename} {download.size ? `(${Math.ceil(download.size/1024)} KB)` : ""}
          </a>
        </div>
      )}
    </main>
  );
}
