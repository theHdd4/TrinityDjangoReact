import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/ui/card';
import { Plus, FolderOpen, Calendar, Pencil } from 'lucide-react';
import AnimatedLogo from '@/components/AnimatedLogo';
import LogoText from '@/components/LogoText';

interface Project {
  id: string;
  name: string;
  lastModified: Date;
  description?: string;
}

const Projects = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    // Load saved projects from localStorage
    const savedProjects = localStorage.getItem('trinity-projects');
    if (savedProjects) {
      const parsedProjects = JSON.parse(savedProjects);
      setProjects(parsedProjects.map((p: any) => ({
        ...p,
        lastModified: new Date(p.lastModified)
      })));
    }
  }, []);

  const createNewProject = () => {
    // Navigate to apps selection page
    navigate('/apps');
  };

  const openProject = (project: Project) => {
    // Set current project and navigate to main app
    localStorage.setItem('current-project', JSON.stringify(project));
    navigate('/');
  };

  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingName, setEditingName] = useState('');

  const startRename = (e: React.MouseEvent, project: Project) => {
    e.stopPropagation();
    setEditingId(project.id);
    setEditingName(project.name);
    setTimeout(() => inputRef.current?.focus(), 0);
  };

  const saveRename = () => {
    if (!editingId) return;
    const trimmed = editingName.trim();
    if (!trimmed) {
      setEditingId(null);
      return;
    }
    const updated = projects.map((p) =>
      p.id === editingId ? { ...p, name: trimmed } : p
    );
    setProjects(updated);
    localStorage.setItem('trinity-projects', JSON.stringify(updated));
    setEditingId(null);
  };

  return (
    <div className="min-h-screen bg-white flex flex-col">

      {/* Header */}
      <div className="relative z-10 p-8">
        <div className="flex items-center space-x-4">
          <AnimatedLogo className="w-12 h-12" />
          <LogoText />
        </div>
        <div className="mt-4">
          <h1 className="text-3xl font-light text-black">
            Trinity Projects
          </h1>
          <p className="text-black/60 text-sm">
            Access your quantum matrices
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex-1 px-8 pb-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {/* Create New Project Card */}
            <Card
              className="bg-trinity-bg-secondary border-gray-300 hover:border-trinity-yellow transition-all duration-300 cursor-pointer hover:shadow"
              onClick={createNewProject}
            >
              <div className="p-6 flex flex-col items-center justify-center h-48 space-y-4">
                <div className="w-16 h-16 rounded-full border-2 border-dashed border-trinity-yellow/40 flex items-center justify-center group-hover:border-trinity-yellow group-hover:bg-trinity-yellow/5 transition-all duration-300">
                  <Plus className="w-8 h-8 text-trinity-yellow/60 group-hover:text-trinity-yellow transition-colors duration-300" />
                </div>
                <div className="text-center">
                  <h3 className="text-black font-medium">Create New Project</h3>
                  <p className="text-black/50 text-sm mt-1">Initialize new matrix</p>
                </div>
              </div>
            </Card>

            {/* Existing Projects */}
            {projects.map((project) => (
              <Card
                key={project.id}
                className="bg-trinity-bg-secondary border-gray-300 hover:border-trinity-yellow transition-all duration-300 cursor-pointer hover:shadow"
                onClick={() => openProject(project)}
              >
                <div className="p-6 flex flex-col h-48">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-10 h-10 rounded-lg bg-trinity-yellow/10 flex items-center justify-center group-hover:bg-trinity-yellow/20 transition-colors duration-300">
                        <FolderOpen className="w-5 h-5 text-trinity-yellow" />
                      </div>
                      <button
                        type="button"
                        onClick={(e) => startRename(e, project)}
                        className="text-black/50 hover:text-black"
                        title="Rename project"
                      >
                        <Pencil className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="w-2 h-2 bg-trinity-green rounded-full animate-pulse opacity-60"></div>
                  </div>
                  
                  <div className="flex-1">
                    {editingId === project.id ? (
                      <input
                        ref={inputRef}
                        value={editingName}
                        onChange={(e) => setEditingName(e.target.value)}
                        onBlur={saveRename}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault();
                            saveRename();
                          }
                        }}
                        className="w-full border border-gray-300 rounded px-2 py-1 text-sm text-black"
                      />
                    ) : (
                      <h3 className="text-black font-medium mb-2 group-hover:text-black/80 transition-colors duration-300">
                        {project.name}
                      </h3>
                    )}
                    <p className="text-black/50 text-xs mb-4 line-clamp-2">
                      {project.description}
                    </p>
                  </div>

                  <div className="flex items-center space-x-2 text-black/40 text-xs">
                    <Calendar className="w-3 h-3" />
                    <span>{project.lastModified.toLocaleDateString()}</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Footer Message */}
          <div className="text-center mt-16">
            <p className="text-black/50 text-sm">
              "The Matrix has you..." - Begin your first project
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Projects;
